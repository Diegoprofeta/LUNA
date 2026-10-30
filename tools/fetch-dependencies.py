#!/usr/bin/env python3
# Original LUNA code: Danny Nunez (dnunezx) 2026
"""Fetch pinned build dependencies without replacing local work."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def git(path, *args):
    return subprocess.run(
        ["git", "-c", f"safe.directory={path.as_posix()}", "-C", str(path), *args],
        check=True, stdout=subprocess.PIPE, text=True,
    ).stdout.strip()


def checkout_root(path):
    if not (path / ".git").exists():
        raise ValueError(f"{path}: not an independent dependency checkout; left untouched")
    if Path(git(path, "rev-parse", "--show-toplevel")).resolve() != path.resolve():
        raise ValueError(f"{path}: unexpected Git root; left untouched")


def clean(path):
    if git(path, "status", "--porcelain", "--untracked-files=all"):
        raise ValueError(f"{path}: local changes found; preserve them before updating")


def nested(path, verify_only):
    if not (path / ".gitmodules").is_file():
        return
    for record in git(path, "ls-tree", "-r", "-z", "HEAD").split("\0"):
        if not record.startswith("160000 "):
            continue
        metadata, relative = record.split("\t", 1)
        revision = metadata.split()[2]
        child = (path / relative).resolve()
        if not child.is_relative_to(path.resolve()):
            raise ValueError(f"{path}: invalid nested dependency path")
        if not (child / ".git").exists():
            if verify_only:
                raise ValueError(f"{child}: nested dependency has not been downloaded")
            if child.exists() and any(child.iterdir()):
                raise ValueError(f"{child}: existing files found; left untouched")
            git(path, "submodule", "update", "--init", "--", relative)
        checkout_root(child)
        if git(child, "rev-parse", "HEAD") != revision:
            raise ValueError(f"{child}: nested dependency differs from its pin; left untouched")
        nested(child, verify_only)


def fetch(root, name, entry, update=False, verify_only=False):
    path = root / name
    revision = entry["revision"]
    if not path.exists():
        if verify_only:
            raise ValueError(f"{name}: missing dependency")
        scratch = root / "local" / "dependency-downloads"
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=f"{name}-", dir=scratch) as temporary:
            temporary = Path(temporary).resolve()
            if not temporary.is_relative_to(scratch.resolve()):
                raise ValueError("Temporary checkout escaped its download directory")
            candidate = temporary / "checkout"
            subprocess.run(["git", "clone", "--no-checkout", "--", entry["url"], str(candidate)], check=True)
            git(candidate, "fetch", "origin", revision)
            git(candidate, "checkout", "--detach", revision)
            candidate.rename(path)
    checkout_root(path)
    current = git(path, "rev-parse", "HEAD")
    if current != revision:
        if verify_only or not update:
            raise ValueError(f"{name}: at {current}, expected {revision}; use --update {name} after preserving local work")
        clean(path)
        git(path, "fetch", entry["url"], revision)
        git(path, "checkout", "--detach", revision)
    if entry.get("recursive"):
        nested(path, verify_only)
    print(f"{name}={git(path, 'rev-parse', 'HEAD')}", flush=True)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--manifest", type=Path, default=Path(__file__).with_name("dependencies.json"))
    parser.add_argument("--components", nargs="+")
    parser.add_argument("--update", nargs="+", default=[], help="Explicitly move clean checkouts to their manifest pins")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--revision", help="Print one manifest revision without downloading")
    parser.add_argument("--pin", nargs=2, metavar=("COMPONENT", "COMMIT"), help="Check out and record an upstream commit")
    parser.add_argument("--allow-rollback", action="store_true", help="Allow an explicit pin to a non-descendant commit")
    args = parser.parse_args()
    manifest = args.manifest.resolve()
    entries = json.loads(manifest.read_text(encoding="utf-8"))
    for name, entry in entries.items():
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", name):
            raise ValueError(f"Invalid dependency name: {name}")
        if not re.fullmatch(r"[0-9a-f]{40}", entry["revision"]):
            raise ValueError(f"{name}: a full commit ID is required")
        if not entry["url"].startswith("https://github.com/"):
            raise ValueError(f"{name}: expected a GitHub HTTPS source URL")
    if args.revision:
        print(entries[args.revision]["revision"])
        return
    if args.allow_rollback and not args.pin:
        parser.error("--allow-rollback requires --pin")
    if args.pin and (args.verify_only or args.update or args.components):
        parser.error("--pin cannot be combined with fetch selection or verification")
    root = args.root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    if args.pin:
        name, revision = args.pin
        if name not in entries or not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("Pin requires a known component and full commit ID")
        path = fetch(root, name, entries[name])
        clean(path)
        previous = entries[name]["revision"]
        git(path, "fetch", entries[name]["url"], revision)
        if not args.allow_rollback:
            git(path, "merge-base", "--is-ancestor", entries[name]["revision"], revision)
        git(path, "checkout", "--detach", revision)
        try:
            if entries[name].get("recursive"):
                nested(path, False)
            entries[name]["revision"] = revision
            temporary = manifest.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(entries, indent=2) + "\n", encoding="utf-8", newline="\n")
            os.replace(temporary, manifest)
        except Exception:
            git(path, "checkout", "--detach", previous)
            raise
        print(f"Pinned {name} to {revision}")
        return
    selected = args.components or args.update or list(entries)
    if set(selected + args.update) - entries.keys():
        raise ValueError("Unknown dependency requested")
    if args.verify_only and args.update:
        parser.error("--verify-only cannot be combined with --update")
    for name in selected:
        fetch(root, name, entries[name], name in args.update, args.verify_only)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as error:
        print(f"Dependency error: {error}", file=sys.stderr)
        sys.exit(1)
