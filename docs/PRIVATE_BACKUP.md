# Private files: kept on two machines, and archived weekly

*T-636, 2026-11-25.* The project's private files never enter git: the design notes in `docs/private/`, the drafts
git ignores, the user's own cart dumps, each machine's keys. This page says how they are kept from being lost, and how
to bring them back. **No password, key or private path's contents are written here, and none ever should be.**

## 1. Two machines, the same files: Syncthing

The development laptop (**DAEMONS-M2cBook**) and the always-on server (**DAEMONS-roverbyteseer**) hold the same
private files, kept the same by [Syncthing](https://syncthing.net) over the tailnet only (no global discovery, no
relays, each machine listening only on its tailnet address).

- **What is shared** is exactly the `!/` lines of each repository's `.stignore` (DAEMONS and daemons-companion);
  everything else is ignored, so nothing git tracks is ever moved by Syncthing. `.stignore`, `.stfolder/` and
  `.stversions/` are themselves git-ignored.
- **Each machine's own state is not shared**: the companion's `.hub`, `.hub-sync`, `server/companion.sqlite` and
  `server/config.json`, EUDAIMONIA's `data/`, the `.claude/` settings.
- **Nothing is lost to a change or a deletion**: every file Syncthing replaces or deletes is kept in that repository's
  `.stversions/` on the other machine (staggered, for 90 days).
- **A file changed on both machines at once** is kept twice: the newer under its name, the other as
  `NAME.sync-conflict-<date>-<device>.EXT` beside it. Choose between them by hand for now; THE DASHBOARD's PRIVATE
  MERGES (E-24) will list them and merge them side by side.
- Syncthing's own page is at `http://127.0.0.1:8384` on each machine.

## 2. Weekly, a password-protected archive on roverbyteseer's drive

`tools/private_archive.sh` runs every Sunday at 03:15 on roverbyteseer (launch agent `ca.codemusic.private-archive`).
It packs everything Syncthing shares, plus the cart dumps, roverbyteseer's live EUDAIMONIA data and its key files,
into one 7-Zip archive encrypted with AES-256 (file names too), tests it, and keeps the newest twelve on the external
drive in `DAEMONS PRIVATE ARCHIVE/`, beside a copy of the restore script and this page.

The password is the one the user chose. It lives in roverbyteseer's keychain and nowhere else on disk. To put it
there (once, typed by the user, on roverbyteseer):

```sh
security add-generic-password -a "$USER" -s daemons-private-archive -T /usr/bin/security -U -w
```

**The archives are never pushed to GitHub**: this repository is public.

## 3. Bringing them back

On any Mac with `brew install sevenzip`:

```sh
tools/private_restore.sh "/Volumes/<drive>/DAEMONS PRIVATE ARCHIVE/daemons-private-<date>.7z"              # unpack and check
tools/private_restore.sh "/Volumes/<drive>/DAEMONS PRIVATE ARCHIVE/daemons-private-<date>.7z" --in-place   # and put back
```

It asks for the password, unpacks into a new folder, and checks every file against the archive's
`MANIFEST.sha256` before changing anything. `--in-place` then puts each file back under the home folder: missing
files are added, older ones replaced (each kept as `NAME.before-restore`), newer ones left alone. Paths in the archive
are relative to the home folder (`Projects/DAEMONS/docs/private/...`), so a restore lands the same on either machine.
