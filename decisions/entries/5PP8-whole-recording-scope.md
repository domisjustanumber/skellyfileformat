# 5PP8 — The format describes a whole synchronised recording

**Status:** accepted, 2026-11-12 (user).

## Decision

1. **Scope.** skellyfileformat describes how to record and how to open a collection of synchronised
   video and audio recordings: one recording (one take). It does not describe only each file. The
   spec covers:
   - each file: the MKV profile, the video timing sidecar, the `.skau` and its packet table, the
     skellysync FLAC track, embedding and finalisation, the Segment UID and the live and final
     offsets, unfinalised and crashed files, and the file, attachment and MIME names;
   - the recording: which files make up one recording, the folder layout and the file names, the
     one clock that all files of a recording share, how a writer records the set, how a reader opens
     it (also when it is crashed or incomplete), the recording manifest, and how to find a file that
     is not in this format.
2. **Recording-level facts.** Each file's sidecar header holds the facts about its recording. The
   header is authoritative.
3. **Recording manifest.** The spec defines a recording manifest: a derived index of the files and
   the facts of one recording. A writer writes it at finalisation. A reader must be able to open a
   recording without it, for example after a crash. When the manifest and a header disagree, the
   header wins. The spec draft gives its fields and the header fields (gate 1).
4. **skellycam's recording info JSON** is not the recording manifest. It stays a skellycam file,
   and skellycam's own spec defines it: skellycam's settings and the contract with freemocap.
5. **Legacy recordings** stay in skellycam. The spec covers only the new format.
6. **Spec first.** For each part of the format: write the spec text and the conformance test list;
   the user reviews them (gate 1); write the runnable tests and the golden files; the user reviews
   them (gate 2); then write the implementation.
7. **Normative documents.** `README.md`, `spec/SPEC.md` and `spec/conformance.md`.
8. **IDs.** A requirement has an ID `SFF-NNN`, and a test has an ID `SFT-NNN` that cites the
   requirements that it checks. An ID is not reused or renumbered. A removed item stays, marked
   withdrawn. `tools/check_spec_traceability.py` checks the links.
9. **Golden files.** They are committed with their SHA-256 sums and the script that made them. A
   change to a golden file needs an entry.
10. **Repository.** Public, on the account of the owner for now. Apache-2.0 for code and CC-BY-4.0
    for the spec text. Commits go to `main` directly until v2.0.0 is released.
11. **Provisional parts.** Some parts of spec v0 are provisional ([open-work.md](../open-work.md)).
    Each provisional part must be closed before v2.0.0.
12. **Versions of dependencies.** Each one is pinned exactly, to a release that is at least 14 days
    old.

This entry supersedes [ADR-CD4G](CD4G-spec-first-and-repository-rules.md) in full: items 6 to 12
restate its rules that stay, and items 1 to 5 replace its scope. It also supersedes
[ADR-83Y4](83Y4-recording-manifest.md): the recording manifest is now part of the spec (item 3),
and skellycam's info JSON is skellycam's own file (item 4).

## Reason

- The user's goal: skellyfileformat must describe a way to record and to open a collection of
  synchronised recordings, not only each file.
- The user's rule: when a synchronised recording cannot be opened or played without the manifest,
  the manifest is part of the spec, with only the fields that the new format needs.
- A lone file, a copied part of a folder and a crashed recording must still tell which recording
  they belong to. So the headers hold the recording facts, and they are authoritative.
- Crash recovery must rebuild a manifest from the files anyway. A derived manifest gives one file
  that opens a recording, and it cannot become the only copy of a fact.
- skellysync writes the format and writes no skellycam info JSON. skellycam's settings change for
  reasons that are not format changes.

## Evidence

- Who reads which field of each file that skellycam writes today
  ([recording_folder_files.md](https://github.com/domisjustanumber/skellycam/blob/cb10dd14682d9aede0de87570dbbf61e3cc282e0/research/skellycam_recording/docs/recording_folder_files.md)).
- A field-by-field review of the manifest and what a player needs to open a recording
  ([manifest_field_review.md](https://github.com/domisjustanumber/skellycam/blob/a4b1565b2aa1afe3c3c73e03974740c2471d91b1/research/skellycam_recording/docs/manifest_field_review.md)).
  It lists the candidate header fields and manifest fields for the spec draft.
- These files are on the `dom/research` branch of the skellycam fork. That branch is not
  force-pushed, so the permalinks stay valid.

## Alternatives rejected

- Recording facts only in each header, with no manifest: a reader then has no single file that
  opens a recording.
- A manifest only, with no recording facts in the headers: a lone or crashed file cannot tell which
  recording it belongs to.
- A spec-defined object inside skellycam's info JSON: two documents then own one file.

## Open work

See [open-work.md](../open-work.md).
