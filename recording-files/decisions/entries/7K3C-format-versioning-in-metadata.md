# 7K3C — Format version = the skellycam release that last changed the format; written in each file's metadata

**Status:** superseded by [9DV4](9DV4-format-version-from-freemocap.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. The format version is the `major.minor` of the skellycam release that last changed the format.
   A change that an older reader cannot read needs a skellycam major version. An added field needs
   a skellycam minor version or a major version. A skellycam patch release does not change the
   format.
2. Each file of the format holds three values in its metadata ([ADR-SFK5](SFK5-mcap-container.md)
   item 4): `major`, `minor` and `prerelease`, each an unsigned integer that fits in 16 bits, written
   as a decimal string. `prerelease` is 0 for a released format and N for the Nth prerelease
   revision. The spec gives the record and the keys.
3. A reader refuses a file with a `major` that it does not know. A reader reads a file with a higher
   `minor` of a known `major`, and skips the fields that it does not know.
4. A conforming reader reads every released format version (`prerelease` = 0). A file with
   `prerelease` > 0 has no compatibility promise.
5. Each file holds a writer string, for example `skellycam 2.1.0`, for diagnostics only. A reader
   does not change its behaviour because of it. skellysync writes the format version that
   skellyfileformat gives.
6. The skellyfileformat package uses semantic versioning. Its `major.minor` is the format version
   that it implements. Its patch number counts library fixes that do not change the format.
7. The MCAP version of the file (the magic) is not the format version.

This entry supersedes [ADR-M4DF](M4DF-format-versioning.md) in full. Items 1, 3, 4 and 6 restate
its items 1, 3, 4 and 6. Items 2 and 5 restate its items 2 and 5 with "each file's metadata" in
place of "each sidecar header". Item 7 is new.

## Reason

- The reasons of ADR-M4DF stay: one number tells a reader if it can read a file and points to the
  skellycam release that made the change; files from prerelease builds must not bind later readers.
- The sidecar headers no longer exist ([ADR-SFK5](SFK5-mcap-container.md)). MCAP metadata holds
  only strings.

## Open work

[open-work.md](../open-work.md)
