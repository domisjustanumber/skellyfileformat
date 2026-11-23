# 41VF — The format describes a whole synchronised recording of MCAP files; file metadata is authoritative

**Status:** superseded by [TDB5](TDB5-whole-recording-no-manifest.md), 2026-11-13 (commit to main; was accepted, 2026-11-13).

## Decision

1. **Scope.** skellyfileformat describes how to record and how to open a collection of synchronised
   video and audio recordings: one recording (one take). It does not describe only each file. The
   spec covers:
   - each file: the MCAP profile ([ADR-SFK5](../../recording-files/decisions/entries/SFK5-mcap-container.md)) with its channels, schemas,
     timing fields and metadata; the Opus audio ([ADR-HD8Z](../../recording-files/decisions/entries/HD8Z-opus-audio.md)); unfinished and
     crashed files;
   - the recording: which files make up one recording, the one clock that all files of a recording
     share, how a writer records the set, how a reader opens it (also when it is crashed or
     incomplete), the recording manifest, and how to find a file that is not in this format.
2. **Names.** The spec fixes only these names: the metadata record names and keys, the channel
   topics, the recording manifest name ([ADR-SFK5](../../recording-files/decisions/entries/SFK5-mcap-container.md) item 8) and the
   temporary-file names. The schema names are the names that the schema publisher gives. The spec
   does not fix the media file names or the folder layout. The writer's own spec defines them. A
   recording is the files in this format, directly in one folder, that share a `take_uuid`.
3. **Recording-level facts.** Each file's metadata holds the facts about its recording. The file
   metadata is authoritative.
4. **Recording manifest.** The spec defines a recording manifest: a derived index of the files and
   the facts of one recording. A writer writes it at finalisation. A reader must be able to open a
   recording without it, for example after a crash. When the manifest and a file disagree, the file
   wins.
5. **skellycam's recording info JSON** is not the recording manifest. It stays a skellycam file,
   and skellycam's own spec defines it: skellycam's settings and the contract with freemocap.
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

This entry supersedes [ADR-25VV](25VV-whole-recording-scope-names.md) in full. Items 4 to 13
restate its items 4 to 13. Items 1 to 3 restate its items 1 to 3 for MCAP: the per-file list, the
fixed names and "file metadata" in place of "sidecar header".

## Reason

- The reasons of ADR-25VV stay: the format must describe a way to record and open a synchronised
  recording; a lone or crashed file must tell which recording it belongs to; a derived manifest
  gives one file that opens a recording and cannot become the only copy of a fact; media file names
  belong to the writer.
- The files are MCAP files ([ADR-SFK5](../../recording-files/decisions/entries/SFK5-mcap-container.md)), so the per-file parts and the
  fixed names change.

## Alternatives rejected

- The alternatives that ADR-25VV rejected stay rejected: the spec fixes the media file names and
  the folder; recording facts only in the files with no manifest; a manifest only; a spec-defined
  object inside skellycam's info JSON.
- One MCAP file for the whole take: open as a profile choice, not decided here
  ([open-work.md](../open-work.md)).

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
