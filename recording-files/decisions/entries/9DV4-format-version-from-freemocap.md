# 9DV4 — Format version = the freemocap release that last changed the folder; written in each file

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. The format version is the `major.minor` of the freemocap release that last changed any file of
   the take folder. A change that an older reader cannot read needs a freemocap major version. An
   added field needs a freemocap minor version or a major version. A freemocap patch release does
   not change the format.
2. The skellyfileformat package and skellycam release at the same `major.minor` when the format
   changes. A change of the Parquet format therefore also needs a skellycam release.
3. Each file of the format records the format version under which it was written: `major`, `minor`
   and `prerelease`, each an unsigned integer that fits in 16 bits. `prerelease` is 0 for a
   released format and N for the Nth prerelease revision. The spec gives the field of each file.
4. A reader refuses a file with a `major` that it does not know. A reader reads a file with a
   higher `minor` of a known `major`, and skips the fields that it does not know.
5. A conforming reader reads every released format version (`prerelease` = 0). A file with
   `prerelease` > 0 has no compatibility promise.
6. Each file holds a writer string, for example `skellycam 2.1.0`, for diagnostics only. A reader
   does not change its behaviour because of it. skellysync writes the format version that
   skellyfileformat gives.
7. The skellyfileformat package uses semantic versioning. Its `major.minor` is the format version
   that it implements. Its patch number counts library fixes that do not change the format.
8. The version of a container (the Matroska `DocTypeVersion`, the MP4 brands, the Parquet format
   version) is not the format version.
9. freemocap 2.x and skellycam 2.x are released at the same time. skellycam 2.0.0 prereleases can
   write prerelease files until then.

This entry supersedes [ADR-7K3C](7K3C-format-versioning-in-metadata.md) in full. Items 4 to 7
restate its items 3 to 6. Item 1 replaces its item 1 (the skellycam release). Item 3 restates its
item 2 for each file of the folder, in place of the MCAP metadata. Item 8 restates its item 7 for the
new containers. Items 2 and 9 are new.

## Reason

- freemocap writes most files of the folder ([ADR-2C9V](../../../decisions/entries/2C9V-whole-take-folder-scope-and-package.md)).
  A Parquet change must not need a skellycam number of its own.
- One number in step across the three projects tells a user which programs read a take.
- The reasons of ADR-7K3C stay: one number tells a reader if it can read a file; files from
  prerelease builds must not bind later readers.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  "Grilling log": round 1 A2 and D5; round 2 Q2 (local, not committed).

## Alternatives rejected

- The skellycam release: a freemocap file change would force a skellycam number.
- The skellyfileformat package release on its own: the user chose freemocap, with the package and
  skellycam in step.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
