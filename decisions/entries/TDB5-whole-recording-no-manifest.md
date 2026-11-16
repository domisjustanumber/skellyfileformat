# TDB5 — The whole recording without a manifest; takes grouped by `take_uuid`; a canonical reader result

**Status:** superseded by [2C9V](2C9V-whole-take-folder-scope-and-package.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. **Scope.** skellyfileformat describes how to record and how to open one recording (one take): a
   set of synchronised MCAP files, one for each device ([ADR-DK8S](DK8S-mcap-profile-files-and-names.md)).
   The spec covers each file (channels, schemas, timing fields, metadata, unfinished and crashed
   files) and the recording (which files make it up, the one clock that they share, how a writer
   records the set, how a reader opens it, also when it is crashed or incomplete, and how to find a
   file that is not in this format).
2. **No recording manifest.** There is no manifest file. Each file's metadata holds the facts of its
   take, and it is the only source of them.
3. **Takes.** A writer puts one take in each folder. A reader looks at the files directly in one
   folder. It groups the files of the format by `take_uuid` and reports each take. A file that the
   writer did not finish belongs to its take, and the reader reports it as unfinished. There is no
   stale-file rule.
4. **Canonical reader result.** The spec defines one JSON result of opening a folder: the state and
   the reason of each file, the state of each take, the warning codes and the per-camera results.
   The Python reader, the JavaScript reader and the golden files are compared with it.
5. **skellycam's recording info JSON** is not part of the format. It stays a skellycam file.
6. **Legacy recordings** stay in skellycam. The spec covers only the new format.
7. **Spec first.** For each part of the format: write the spec text and the conformance test list;
   the user reviews them (gate 1); write the runnable tests and the golden files; the user reviews
   them (gate 2); then write the implementation.
8. **Normative documents.** `README.md`, `spec/SPEC.md` and `spec/conformance.md`.
9. **IDs.** A requirement has an ID `SFF-NNN`, and a test has an ID `SFT-NNN` that cites the
   requirements that it checks. An ID is not reused or renumbered. A removed item stays, marked
   withdrawn. `tools/check_spec_traceability.py` checks the links.
10. **Golden files.** They are committed with their SHA-256 sums and the script that made them. A
    change to a golden file needs an entry.
11. **Repository.** Public, on the account of the owner for now. Apache-2.0 for code and CC-BY-4.0
    for the spec text. Commits go to `main` directly until v2.0.0 is released.
12. **Provisional parts.** Some parts of the spec are provisional ([open-work.md](../open-work.md)).
    Each provisional part must be closed before v2.0.0.
13. **Versions of dependencies.** Each one is pinned exactly, to a release that is at least 14 days
    old.

This entry supersedes [ADR-41VF](41VF-whole-recording-scope-mcap.md) in full. Items 5 to 13 restate
its items 5 to 13. Item 1 restates its item 1 for one file per device. Item 2 withdraws its item 4
(the manifest) and makes its item 3 (file metadata is authoritative) the only source. Item 3
replaces the folder part of its item 2. The names of its item 2 are in
[ADR-DK8S](DK8S-mcap-profile-files-and-names.md). Item 4 is new.

## Reason

- Each file already holds the facts of its take, and a player opens the summary of every file to
  play (about 5 ms each). A manifest only copied facts, and it needed rules for a manifest that
  disagrees with the files and for stale files.
- A defined result makes the readers and the golden files comparable byte for byte.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md`
  (Q23, Q24, Q25; local commit, not pushed).

## Alternatives rejected

- Keep a derived manifest: it duplicates the file metadata and adds disagreement rules.

## Open work

[open-work.md](../open-work.md)
