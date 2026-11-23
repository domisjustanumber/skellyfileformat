# 25VV — The format describes a whole synchronised recording; the spec fixes only its own names

**Status:** superseded by [41VF](41VF-whole-recording-scope-mcap.md), 2026-11-13 (commit to main; was accepted, 2026-11-12).

## Decision

1. **Scope.** skellyspecs describes how to record and how to open a collection of synchronised
   video and audio recordings: one recording (one take). It does not describe only each file. The
   spec covers:
   - each file: the MKV profile, the video timing sidecar, the audio timing sidecar and its packet
     table, the skellysync FLAC track, embedding and finalisation, the Segment UID and the live and
     final offsets, unfinalised and crashed files, and the file, attachment and MIME names;
   - the recording: which files make up one recording, the one clock that all files of a recording
     share, how a writer records the set, how a reader opens it (also when it is crashed or
     incomplete), the recording manifest, and how to find a file that is not in this format.
2. **Names.** The spec fixes only these names: the sidecar names, the attachment names and media
   types, the temporary-file names and the recording manifest name
   ([ADR-WD1R](../../recording-files/decisions/entries/WD1R-file-attachment-and-mime-names.md)). It does not fix the media file names or the
   folder layout. The writer's own spec defines them. A recording is the files in this format,
   directly in one folder, that share a `take_uuid`.
3. **Recording-level facts.** Each file's sidecar header holds the facts about its recording. The
   header is authoritative.
4. **Recording manifest.** The spec defines a recording manifest: a derived index of the files and
   the facts of one recording. A writer writes it at finalisation. A reader must be able to open a
   recording without it, for example after a crash. When the manifest and a header disagree, the
   header wins.
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
12. **Provisional parts.** Some parts of spec v0 are provisional ([open-work.md](../open-work.md)).
    Each provisional part must be closed before v2.0.0.
13. **Versions of dependencies.** Each one is pinned exactly, to a release that is at least 14 days
    old.

This entry supersedes [ADR-5PP8](5PP8-whole-recording-scope.md) in full. Items 1 and 3 to 13
restate its items 1 to 12, except that item 1 no longer lists "the folder layout and the file names"
for the recording. Item 2 is new: it gives the names that the spec fixes.

## Reason

- The reasons of ADR-5PP8 stay: the format must describe a way to record and open a synchronised
  recording; a lone or crashed file must tell which recording it belongs to; a derived manifest
  gives one file that opens a recording and cannot become the only copy of a fact.
- The user decided (spec draft question Q22) that media file names and folder names belong to the
  writer. They are part of the contract between skellycam and freemocap, which waits for phase 2 of
  the skellycam plan. A reader finds a recording by its sidecars and `take_uuid`, not by names, so
  the format does not need them.

## Evidence

- A field-by-field review of the manifest and what a player needs to open a recording
  ([manifest_field_review.md](https://github.com/domisjustanumber/skellycam/blob/a4b1565b2aa1afe3c3c73e03974740c2471d91b1/research/skellycam_recording/docs/manifest_field_review.md)):
  no part of opening a recording needs a media file name.

## Alternatives rejected

- The spec fixes the media file names and the `synchronized_videos/` folder (today's freemocap
  contract): it ties the format to a contract that belongs to skellycam and freemocap.
- The alternatives that ADR-5PP8 rejected stay rejected: recording facts only in the headers with no
  manifest; a manifest only; a spec-defined object inside skellycam's info JSON.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
