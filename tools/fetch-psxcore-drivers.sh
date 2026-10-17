#!/bin/sh
# Fetch only the four public storage modules required by PSXCore's upstream build.
set -eu
destination="${1:?Supply the destination directory}"
revision=2bd309688537eff30fe8b218f7ec4d615f7b9824
base="https://raw.githubusercontent.com/NathanNeurotic/POPSLoader/$revision/bin/POPSLDR"
mkdir -p "$destination"
fetch_driver() {
  name="$1"
  expected="$2"
  if [ -f "$destination/$name" ] &&
     printf '%s  %s\n' "$expected" "$destination/$name" | sha256sum -c - >/dev/null 2>&1; then
    return
  fi
  curl --fail --location --silent --show-error --retry 3 \
    "$base/$name" -o "$destination/$name.tmp"
  printf '%s  %s\n' "$expected" "$destination/$name.tmp" | sha256sum -c -
  mv "$destination/$name.tmp" "$destination/$name"
}
fetch_driver usbd.irx.usbexfat 5ea4818ba1cf5207f6d7cadb4c13b5afa88c37c260750c21155b079a8c18f369
fetch_driver usbhdfsd.irx.usbexfat 70a369e47745e7f995fa771edbbfed086727b759fba915a7070c0fbcf061dd34
fetch_driver usbd.irx.ata 4e1d39365854747117a08f8a8d843937614590ea072cf2b70f6e4c2ebbf3c6ee
fetch_driver usbhdfsd.irx.ata 1cc865cd09997bd708e9e102c0f0f1f17f352b7844b282fcfa6a00f38609db9c
