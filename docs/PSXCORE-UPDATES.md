# Updating PSXCore with LUNA

PSXCore is an independently maintained submodule. LUNA owns its indexed
library, selection, artwork, frontend settings, argument preparation, and
frontend shutdown. PSXCore owns storage reopening, disc/request validation,
runtime adaptation, and game saves. PSXCore is reference-only: never modify its
source here. Consume clean upstream revisions; report required core changes to
the user for maintenance upstream. Do not work around this boundary with SDK
changes or injected runtime patches.

## Update and build

From the LUNA workspace in PowerShell:

```powershell
.\tools\update-psxcore.ps1 -Development
```

This fetches the current remote default-branch HEAD, refuses a dirty PSXCore
checkout or a non-forward update, checks out the exact commit, and runs
`tools/build-luna-psxcore.sh` in `ps2max/dev:v20260228`. Frontend edits remain
in place. Use `-Hardware` for a console build, and omit `-Development` for a
build without the local development launcher. `-BuildImage` selects another
compatible PS2SDK image.

Both the PSXCore library linked into LUNA and its standalone runtime ELF are
built from the same clean source checkout. The combined build never fetches;
updating is an explicit separate operation. Repeated builds of a recorded
commit therefore do not silently advance to newer source.

The emulator output directory is `nhddl/build-psxcore`; hardware output is
`nhddl/build-psxcore-hardware`. Each completed build publishes:

- `luna.elf` and `luna_unc.elf`.
- `psxcore-runtime-bootstrap.elf` and its SHA-256.
- `psxcore-build.txt`: exact core/frontend/SDK revisions, frontend dirty state,
  build options, runtime origin, container image identity, compiler version,
  UTC build time, and verification status. SDK Git revision is `unavailable`
  when the image omits its Git metadata; the container identity is recorded.
- `psxcore-build.sha256`: hashes of the frontend ELFs, linked core library,
  and staged runtime ELF. Run `sha256sum -c psxcore-build.sha256` in the output
  directory inside the container to check the set.

A failed combined build removes the previous completion manifest. A failed
update build leaves the fetched core checked out for inspection and reports
the previous revision. It does not commit, push, or discard source changes.
After verification, record the new submodule pointer with the LUNA changes.
Keep the runtime ELF and its manifest together when staging a build for use.

To explicitly rebuild an earlier commit:

```powershell
.\tools\update-psxcore.ps1 -Revision <full-commit> -Development
```

## Launch contract checked at bb6c5be

LUNA's adapter in `nhddl/src/psxcore_launch.c` and `psxcore_transfer.c` stages
the standalone ELF and transports ordinary `argc`/`argv`. It does not duplicate
PSXCore request structures or inject runtime patches.

The current file backend accepts `--file massN:/path/Game.VCD` or
`--file-request massN:/path/REQUEST.BIN`. Direct-file selection also supports
`--pcsx2` and `--license`; those overrides cannot accompany a request that
already supplies them. `--init-cards` explicitly provisions missing cards;
the core does not infer a frontend's provisioning policy. Synthetic probing is a
development operation, not gameplay verification.

The pinned backend supports ATA and USB endpoints with FAT32/exFAT. LUNA's game
library still selects internal ATA images. The core resets the
IOP and reopens storage itself. The selected VCD must remain accessible by
relative path and measured identity after that reset. Firmware defaults to
`/POPS/POPS.ELF` and `/POPS/IOPRP252.IMG` on the selected volume. Isolated cards
are routed to `/POPS/SAVES/<save_key>/card0` and `card1`.

LUNA discovers case-insensitive VCD filenames on ATA and reads bounded disc
metadata for artwork IDs without placing PS1 entries in the PS2 title cache.
L3 cycles PS2, PS1, and Mix, intersecting favorites. Selected PS1 games bypass
PS2 launch arguments, cheats, and VMC settings. LUNA defaults unassigned PS1
games to automatic private cards and groups verified multi-disc IDs into a
volume-bound pair. Existing manual choices remain overrides. Automatic private
launches pass `--init-cards` for missing cards; existing-save conflicts need a
source choice before grouping. Shared launches instead pass
`--shared-set`, both volume IDs, and the selected save endpoint. LUNA uses the
public shared-store API and card formatter for offline management, compiling
the unchanged upstream `src/shared_store.c` alongside the frontend. Settings
and launch preflight show cancellable disc-identity progress. PSXCore validates
the disc, volumes, cards, and enrollment again after reset. See
[PlayStation memory cards](PS1-MEMORY-CARDS.md) for usage and storage layout.

Request mode accepts legacy v3/v4 requests and the checked 608-byte v5 contract
with explicit disc/save endpoints and persistent volume identities. If
library launching needs that mode, construct and validate it through PSXCore's
public functions rather than reproducing its layout in LUNA. The older
no-argument HostFS/native-partition path remains a separate reference path.

Review `runtime/file_storage.c`, `include/psxcore_file.h`, and the public API
changes on each update. The standalone integration document still describes
mostly the older native-partition path; the current CLI implementation is the
source of truth for file launches.

## Accepting an update

Build success establishes compile/link compatibility. Run the local ELF and
argument-boundary checks against the newly produced runtime, then verify a
selected game, controls/audio, and saving followed by a cold reload using
copies of user save cards. Exercise mixed PS1/PS2 library behavior as those
controls are connected. Console acceptance requires a separate hardware run.
Record results locally, outside tracked source.

An external reference ELF may only be supplied with the development option.
Its manifest says `external-reference-unverified`; it cannot establish that
the current PSXCore source works. A normal paired build says
`matching-checkout`. Neither label implies gameplay or save acceptance.
