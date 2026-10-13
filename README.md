<p align="center">
  <img src="assets/luna-logo.svg" alt="LUNA logo" width="700">
</p>

<p align="center"><strong>LIMEN UMBRAE NEXUS ARCANUM</strong></p>

LUNA is a modern visual game launcher for the PlayStation 2, built on [NHDDL](https://github.com/pcm720/nhddl). Designed to bring a polished,
console-like experience, LUNA combines game discovery, library management, and multiple launch engines into one lightweight, unified interface.

With support for [Neutrino](https://github.com/rickgaiser/neutrino) and [OPL](https://github.com/ps2homebrew/Open-PS2-Loader), LUNA gives you the freedom to choose how your PS2 games are launched,
while experimental PlayStation 1 integration through [PSXCore](https://github.com/dnunezx/PSXCore) brings another generation of games into the same library.

Browse your collection in
five library views, choose Neutrino or OPL for PS2 games, manage virtual memory
cards, and customize the interface around your library.

Experimental PS1 integration brings PlayStation games into the same library
through [PSXCore](https://github.com/dnunezx/PSXCore).

> **PSXCore is in early development. IGR and multi-disc swapping are not yet functional**

PSXCore is an in-house, open-source project developed specifically for LUNA as an alternative to POPStarter.
It was born from the need for a dedicated PlayStation 1 solution that could be actively maintained, updated, and improved over time.
Development has already seen major breakthroughs in game compatibility, with significant progress on games previously thought to be broken or incompatible, including DOOM, Skullmonkeys, Duke Nukem, Parasite Eve II, and many more.


## Library views

| View | Experience |
| --- | --- |
| **List** | A title list with a cover and spinning disc label. Choose Separate or Overlap artwork. |
| **Collections** | A PSBBN-inspired cover flow using square artwork. |
| **Orbit** | A rotating ring of covers with perspective, depth, and Random Scan. |
| **3D** | A 6 × 4 display of game cases with a selected-cover preview and PS1 jewel-case styling. |
| **Scroll** | A horizontal logo strip above a cover carousel. Missing logos fall back to title text. |

<table>
  <tr>
    <td align="center" width="50%"><strong>List</strong><br><img src="assets/previews/classic.gif" alt="List view with cover art and a rotating disc label" width="360"></td>
    <td align="center" width="50%"><strong>Collections</strong><br><img src="assets/previews/collection.gif" alt="Collections view moving through game artwork" width="360"></td>
  </tr>
  <tr>
    <td align="center"><strong>Orbit</strong><br><img src="assets/previews/orbit.gif" alt="Orbit view moving through a ring of game covers" width="360"></td>
  </tr>
</table>

The previews illustrate these views; individual details may differ in newer builds.

Press **Circle** to cycle through enabled views. List, Collections, Orbit,
and 3D are enabled by default; enable Scroll in **Options → Views**.
Favorites, the selected view, and the game-platform filter are remembered.

## Requirements

- **PlayStation 2:** hardware testing has been performed on a fat PS2.
- **Free McBoot memory card:** enough space for the complete `APP_LUNA` folder.
- **Internal ATA/exFAT HDD:** the intended setup for library and artwork
  performance, with an MBR or GPT partition table and an exFAT partition.
- **Compatible network adapter or HDD bridge:** hardware testing used a
  GameStar PS2 SATA HDD Adapter.
- **Optional artwork:** games can launch without it. Use
  [OrbitPS2 Manager — LUNA Edition](https://github.com/dnunezx/OrbitPS2-Manager-LUNA-edition)
  to prepare the library and artwork.

Other storage sources are selectable through **Start → Storage Devices**.
Artwork performance on slower devices can affect navigation.

## Installation

These steps use a memory card in slot 1 (`mc0:`), a working FMCB setup, and
a USB drive your PS2 can read.

1. Download the package ending in `-FMCB-mc0.zip` from
   [LUNA Releases](https://github.com/dnunezx/LUNA/releases).
2. Extract it and copy the complete `APP_LUNA` folder to the USB drive's root.
3. On the PS2, open uLaunchELF or wLaunchELF from FMCB. Copy `APP_LUNA` from
   `mass:/` to `mc0:/`.
4. Open FMCB Configurator, add a menu item named **LUNA**, and set its path to
   `mc0:/APP_LUNA/luna.elf`. Save the FMCB configuration.
5. Connect the prepared game drive and start LUNA from FMCB.

Keep the application folder intact:

```text
mc0:/APP_LUNA/
  luna.elf
  luna.yaml
  neutrino.elf
  config/
  modules/
```

A PSXCore-enabled installation also needs `psxcore-runtime-bootstrap.elf`
beside `neutrino.elf`. Use the matching runtime files supplied for your build.

For memory-card slot 2, use `mc1:/APP_LUNA/luna.elf` and change `return_path`
in `luna.yaml` to match. Memory-card installation is required for LUNA's
configured Neutrino in-game return path.

### Optional ambient music

If your release includes `Ambient-Music-Add-On`, copy its `ambient.wav` file
into `APP_LUNA`. It uses about 1.3 MB of additional card space. Enable
**Options → Global → Ambient sound**, then press **Start** to save.
LUNA also works without the music file.

## Preparing your library

Mount the drive in **OrbitPS2 Manager — LUNA Edition** and accept its prompt
to create missing library folders. Import your PS2 games and obtain artwork
through the manager. Keep games and artwork on the game drive.

```text
/CD/                         PS2 CD images
/DVD/                        PS2 DVD images
/VCD/                        PS1 VCD images
/ART/                        Cover and disc artwork
/ART/PSBBN/                  Square artwork
/ART/SCROLL/                 Scroll logos
/CHT/                        Raw PS2RD cheat files
/VMC/                        PS2 virtual memory cards
/LUNA/                       Library state and settings
```

An existing OPL library can retain its title-ID artwork conventions.
Connect storage before launching LUNA; live insertion and removal are not
supported by the Storage Devices menu.

### Experimental PS1 setup

**PSXCore is in early development.** PS1 discovery and launch preparation are
currently integrated for internal ATA drives.
This does not establish compatibility for every PS1 game or storage setup.

Place compatible PS1 `.VCD` images in `VCD/`. The game drive must also contain
the exact firmware files accepted by the bundled PSXCore version:

```text
/POPS/POPS.ELF
/POPS/IOPRP252.IMG
```

Sony's POPS runtime is proprietary and **is not included**. Supply these files
separately. LUNA checks their size and SHA-256 before handing the game to
PSXCore; missing or mismatched files produce an error in the frontend.

Press **L3** to choose Mix or PS1, select a game, and press **Cross**.
The default shared card pair is created when missing. Games using that pair
share its save space; cards are not automatically isolated per game.

## Controls

| Button | Library action |
| --- | --- |
| **Cross** | Launch the selected game. |
| **Circle** | Switch to the next enabled view. |
| **Triangle** | Open Options. |
| **Start** | Open the main menu. |
| **Select** | Switch between All and Favorites. |
| **L3** | Cycle Mix → PS2 → PS1 in PSXCore-enabled builds. |
| **Hold R1** | Open the quick menu. |
| **Square in List** | Add or remove the selected Favorite. |
| **Square in Orbit** | Start Random Scan; navigation cancels it. |
| **L2 / R2 in List or 3D** | Move between pages. |
| **Hold L2 / R2 in Collections** | Fast scan through covers. |

While holding **R1**, use **Cross** to toggle the Favorites filter,
**Circle** to toggle the selected Favorite, **Triangle** for Options,
**L3** for the platform filter, or **R3** for Orbit Random Scan.

### In-game return

LUNA offers IGR to Neutrino and OPL,  hold
**L1 + L2 + R1 + R2 + Start + Select** for roughly one second to return to
the configured LUNA ELF.
PSXCore's IGR is currently not working

## Game settings

Open **Triangle → Game** for the selected title, or **Global** for defaults.
Press **Start** to save changes.

- **PS2 game core:** Neutrino is the default. Select OPL globally or per game.
  OPL launch integration covers ATA/FAT32/exFAT, APA/HDL, USB, MX4SIO, iLink,
  MMCE, and UDPFS.
- **Compatibility and video:** choose the settings for the selected PS2 core.
  Neutrino includes 240p/288p, 480p/576p, and 1080i scaling options. Output
  changes do not automatically increase a game's internal rendering resolution.
- **Startup logo:** set the PS2 logo globally or override it for a game.
- **Cheats:** select entries from `CHT/<TITLE_ID>.cht`, enable cheats, and save.
  Cheats are off by default. This path uses raw PS2RD codes and the matching
  LUNA Neutrino runtime; encrypted cheat files are not supported.
- **Appearance:** choose backgrounds, glass tint, fonts, PS1 case style,
  List artwork layout, and Ambient Orbs colors and formations.


## Virtual memory cards

Open **Start → Virtual Memory Cards** to manage cards. PSXCore-enabled builds
offer separate PlayStation and PlayStation 2 managers.

### PlayStation 2

Create formatted 8 MiB cards or assign existing compatible raw OPL `.bin`
images from the game's drive. Open **Game → Virtual memory cards** to assign
slot 1 and slot 2, then press **Start** to save. Physical cards remain an option.

Supported local card locations include exFAT HDD, USB, MX4SIO, iLink, and
mounted APA/PFS metadata storage. Neutrino accepts compatible raw 8, 16, 32,
and 64 MiB images. APA/PFS cards require the matching runtime and have layout
and fragmentation limits; compatibility still needs physical-console testing.
UDPFS does not offer local file-card creation or selection.

### PlayStation

Use the **default shared cards** on the game drive, or create and assign a
**named pair** through the game's memory-card settings. Both slots follow the
selected pair. Press **Start** in game settings to save the assignment.

```text
/POPS/ps1emu/card0              Default shared slot 1
/POPS/ps1emu/card1              Default shared slot 2
/POPS/CARDS/<name>/card0.vmc     Named pair, slot 1
/POPS/CARDS/<name>/card1.vmc     Named pair, slot 2
```

Each card is 128 KB. The manager supports import, export, backups of both
cards, and recovery of interrupted card operations. Importing into a shared
card affects every game using it. These management features are part of the
experimental PS1 integration; real-game save/reload testing remains ongoing.



## Storage and built-in tools

**Start → Storage Devices** selects ATA/exFAT HDD, APA/HDLoader HDD, USB,
MX4SIO, MMCE, iLink, or UDPFS. Toggle sources and choose
**Apply changes & scan**, rescan one enabled source with **Square**, or rescan
all enabled devices. MX4SIO and MMCE cannot be selected together. UDPFS needs
Ethernet and a running server; its console-IP setting is the PS2's address.

**Start → File Explorer** opens a two-pane browser for storage and memory
cards. Copy or move marked items, create folders, rename files, and inspect
details. Transfers show progress and offer Skip, Keep Both, or Replace when
names conflict. Moves verify copied data before removing the source.

**Start → Language** selects English, Español, or Português (Brazilian
Portuguese). The preference applies immediately and is saved beside LUNA.
The main menu also offers **Exit LUNA** and **Shutdown**.

## Artwork and saved preferences

Artwork is optional. LUNA uses title IDs and these PNG naming conventions:

```text
/ART/<TITLE_ID>_COV.png         Cover artwork
/ART/<TITLE_ID>_ICO.png         Optional disc label
/ART/PSBBN/<TITLE_ID>.png       Square artwork for Collections and Orbit
/ART/SCROLL/<TITLE_ID>_LGO.png  Optional Scroll logo
```


Library state lives under `/LUNA` on the game drive, including cache,
last-launched title, Favorites, view selection, and game settings. Legacy
`/nhddl` state remains readable as a fallback. Storage and language preferences
are saved beside the LUNA executable. PS1 card selections live under
`/POPS/CARD_SELECTIONS` on the game drive.

## Source and credits

| Component | Role |
| --- | --- |
| [`nhddl/`](https://github.com/dnunezx/nhddl-luna) | LUNA frontend derived from NHDDL. |
| [`neutrino/`](https://github.com/dnunezx/neutrino-luna) | Default PS2 game runtime. |
| [`opl/`](https://github.com/dnunezx/Open-PS2-Loader) | Alternate PS2 launch integration. |
| [`psxcore/`](https://github.com/dnunezx/PSXCore) | Independently maintained, experimental PS1 dependency in early development. |

Initialize the pinned dependencies with `git submodule update --init --recursive`.
PSXCore is consumed unchanged; LUNA-specific integration belongs in LUNA.

Special thanks to **Ivan V ([pcm720](https://github.com/pcm720))** for NHDDL,
**Rick Gaiser ([Maximus32](https://github.com/ps2max32))** for Neutrino,
and the **Open PS2 Loader contributors**.

Thanks to **[CosmicScale](https://github.com/CosmicScale)** and the
**[PSBBN Definitive Project](https://github.com/CosmicScale/PSBBN-Definitive-Project)**
for design inspiration and assets, **[NathanNeurotic (Ripto)](https://github.com/NathanNeurotic)**
for help with ambient orbs, **[aap](https://github.com/aap/osdbits)** for OSDSYS
reverse engineering, and all LUNA beta testers.

See [AUTHORS.md](AUTHORS.md), [UPSTREAM.md](UPSTREAM.md), and
the preserved licenses in `LICENSES/` for attribution and source lineage.
Original LUNA code and modifications: **Danny Nunez (dnunezx), 2026**.
Games, Sony firmware, and proprietary POPS runtime files are not distributed
in this source repository.
