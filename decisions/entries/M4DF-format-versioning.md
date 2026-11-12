# M4DF — Format version, header fields and package version

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. The format version is the `major.minor` of the skellycam release that last changed the format.
   A change that an older reader cannot read needs a skellycam major version. An added field needs
   a skellycam minor version or a major version. A skellycam patch release does not change the
   format.
2. Each sidecar header (the video timing sidecar and the `.skau`) holds three unsigned 16-bit
   fields: `major`, `minor` and `prerelease`. `prerelease` is 0 for a released format and N for the
   Nth prerelease revision.
3. A reader refuses a file with a `major` that it does not know. A reader reads a file with a higher
   `minor` of a known `major`, and skips the fields that it does not know.
4. A conforming reader reads every released format version (`prerelease` = 0). A file with
   `prerelease` > 0 has no compatibility promise.
5. Each sidecar holds a writer string, for example `skellycam 2.1.0`, for diagnostics only. A reader
   does not change its behaviour because of it. skellysync writes the format version that
   skellyfileformat gives.
6. The skellyfileformat package uses semantic versioning. Its `major.minor` is the format version
   that it implements. Its patch number counts library fixes that do not change the format.

## Reason

- One number tells a reader if it can read a file, and it points to the skellycam release that made
  the change.
- skellycam is in prerelease now. Files from prerelease builds must not bind later readers.

## Evidence

- Plan row D21 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.
