# PlayStation memory cards

PSXCore-enabled LUNA builds offer **Start → Virtual Memory Cards → PlayStation**.
The PlayStation 2 section retains the existing PS2 card manager and slot picker.

A PlayStation card set contains **two raw 128 KB cards**. PSXCore shares the
complete pair; slots cannot independently select different sets. Up to 32 disc
content identities can be enrolled in one set.

## Automatic cards

New and unassigned PS1 games default to **Automatic**. Launch the game normally:
LUNA checks existing private cards and requests creation of missing cards without
an extra button prompt. It never formats an existing card.

Verified multi-disc games use one pair for all matching discs on the game drive.
The first launch checks installed discs in that regional group. A single existing
private pair is copied to the group, preserving its saves. Different existing
pairs require a choice of which saves to use. LUNA makes verified backups and
keeps every original private pair; it does not combine their contents. Cancelling
the choice leaves the group uncreated. A later disc with separate saves can use
the existing group or keep its private cards. Existing group cards are never
automatically replaced by a later disc's private saves.

Unrecognized disc IDs use private cards. Filenames do not determine grouping;
different regions and listed editions have separate identities. The initial
table covers 110 regional sets / 301 IDs across 28 selected multi-disc titles,
including Final Fantasy VII–IX, Metal Gear Solid, Chrono Cross, The Legend of
Dragoon, Grandia, Xenogears, and Resident Evil 2. Sharing between unrelated games
remains a manual option. Automatic card grouping does not implement in-game disc
swapping; that is a separate runtime feature.

## Change behavior or manage saves

Open a PS1 game's **Virtual memory cards** page. **Card behavior** offers
**Automatic (recommended)**, **Private cards for this disc**, and **Choose shared
cards**. The shared picker also offers **Create new set** for blank cards or a
copy of the selected disc's private pair. Slot actions and **Manage cards**
prepare automatic cards before opening their management menu.

Existing saved private/shared assignments retain their previous manual behavior.
Select Automatic and press Start to opt those discs into automatic grouping.
Switching behavior preserves cards; it does not copy group saves back into the
private pair. Automatic assignments store the policy; the actual group is
resolved from the verified disc identity on each launch.

If settings cannot be loaded, the page remains navigable and shows the reason.
Press Cross for **Retry / Back**. Card changes and launching stay blocked until
the disc identity and saved assignment have been checked successfully. Holding
Triangle while opening settings does not cancel preparation; release it before
pressing it again to cancel.
Selecting a set enrolls the disc immediately; **Start** saves its assignment.
**Square** launches with the pending selection. Returning without saving keeps
the previous assignment, although an explicitly created set or enrollment remains.

PS1 game discovery and launching still use the internal ATA drive. Shared cards
can be stored on enabled ATA or USB storage supported by the pinned core. LUNA
creates a persistent drive identity when creating or first assigning a shared
set. Missing drives, duplicate drive IDs, and missing enrollment block launching;
LUNA never substitutes private cards for an unavailable shared selection.

## Manage cards

The global manager lists named shared sets. **Manage cards** in game settings
also provides access to private pairs. Open a slot to import or export a raw
card. Export creates a new file; it does not overwrite existing files.

**Back up both cards** retains both cards, ownership/shared metadata, and existing
previous-card copies in a dated folder. **Restore backup** uses a completed LUNA
backup folder and restores both cards while preserving the current enrollment.
Imports replace one slot. Both operations create a new backup of the current
pair before staging replacements. Every game using a shared set sees the changes.

**Rename set** changes its display name without changing its identity or cards.
**Enrolled games** can remove a disc's enrollment without removing its save data.
Manual shared assignments then block launch until re-enrolled or changed.
Automatic policy enrolls a matching disc again when it next needs the group.

## Storage layout

- `/POPS/SAVES/<set-key>/card0`, `card1`, and `shared.set`: shared pair and metadata.
- `/POPS/SAVES/LUNA_AUTO_<regional-first-disc-ID>/`: automatic multi-disc pair.
- `/POPS/SAVES/<first-32-disc-hash-characters>/`: existing private saves and owner.
- `/POPS/PSXCORE.VOLUME`: persistent storage identity.
- `/POPS/SETTINGS/<full-disc-sha256>.vmc`: checked LUNA card assignment on the game drive.
- `/POPS/TITLES/<full-disc-sha256>.txt`: optional game labels on the card drive.
- `/POPS/BACKUPS/<set-key>/<date-and-sequence>/`: verified backup copies.

Assignments follow disc content, including a renamed VCD. LUNA rediscovers shared
storage by its identity, rather than persisting `massN:` enumeration. A changed
disc image is a different identity and defaults to private cards.

Incomplete `.new`/`.bak` operations and shared-metadata recovery files are
preserved and block use. There is no automatic recovery or power-loss durability
guarantee. Copy the entire affected folder before undertaking manual recovery.
Only raw images with the core's expected size and header are accepted; container
formats, individual-save editing, and physical PS1 cards are outside this manager.

## Disc-group references

The explicit serial facts in `nhddl/src/ps1_disc_groups.inc` were checked against
[DuckStation's disc-set catalog](https://github.com/stenzek/duckstation/blob/master/data/resources/discsets.yaml)
(blob `37c325be1e7a6a6c9c4a8b3abd5db0565afb8d2d`, checked 2026-10-10) and the
[PSBBN title database](https://github.com/CosmicScale/PSBBN-Definitive-Project/blob/d2628ad3e3a3a58bd03fdfedd8845c74e1eaa124/scripts/assets/database/TitlesDB_PS1.csv).
LUNA uses its own selected factual mapping and policy implementation; it does not
ship the downloaded catalogs, emulator code, or cross-game grouping list.
