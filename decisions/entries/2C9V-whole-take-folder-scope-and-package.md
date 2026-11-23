# 2C9V — The format is the whole take folder; every file is fully specified; one shared package

**Status:** superseded by [YBT1](YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16))).

## Decision

1. **Scope.** skellyfileformat is the spec of one take folder and of each file in it. This includes
   the skellycam media files and their timing sidecars, and the files that freemocap writes: the
   manifest, the info JSONs, the calibration TOML, the tracking Parquet, the realtime journal, the
   Blender outputs, the annotated videos, the exports and the logs. Another program can use the spec
   to write a compatible folder, or to read the output of freemocap.
2. **Full definition.** The spec defines each file in full. It does not leave parts of a file to
   the code of the program that writes it.
3. **Files in formats of other projects.** For a file in a format that this project does not own
   (for example `.blend`, an MP4 annotated video, NPY, NPZ, a notebook, a log), the spec gives the
   name, the container and the codec, and the content mapping: for example the export columns, the
   array shapes and the axis order, the points that an annotated frame shows, and the objects of a
   Blender scene. For a log, the spec gives only the name and the text encoding. It does not
   re-specify the outside format. The contents of the `.blend` scene (the scene, the camera layout)
   are future freemocap work. freemocap defines them when it writes `.blend` files.
4. **Governance.** A change to any file of the folder needs a change of this spec first, and the
   user approves it. freemocap's `RECORDING_CONTRACT.md` points to this spec for the folder.
5. **The package.** The format code is in one shared package, skellyfileformat. It holds the spec,
   the conformance test list, the golden files, a Python reader and writer, and a JavaScript
   reader. An optional write layer, `skellyfileformat[write]`, holds the writer.
6. **Reference readers.** The Python reference reader reads every file of the folder. The
   JavaScript reader reads only what the skellycam player needs: the media files, their timing
   sidecars and the JSON files.
7. **No recorded overlays.** skellycam records no overlay and no burned-in text. The take has no
   overlay file. `.skov` is not part of the format. The player draws the frame label from the
   fields of the frame. The take holds 2D and 3D tracking data as data (see
   [ADR-P76Y](../../recording-files/decisions/entries/P76Y-tracking-parquet.md)), not as drawings.
8. **Spec first.** For each part of the format: write the spec text and the conformance test list;
   the user reviews them (gate 1); write the runnable tests and the golden files; the user reviews
   them (gate 2); then write the implementation.
9. **Normative documents.** `README.md`, `spec/SPEC.md` and `spec/conformance.md`.
10. **IDs.** A requirement has an ID `SFF-NNN`, and a test has an ID `SFT-NNN` that cites the
    requirements that it checks. An ID is not reused or renumbered. A removed item stays, marked
    withdrawn. `tools/check_spec_traceability.py` checks the links.
11. **Golden files.** They are committed with their SHA-256 sums and the script that made them. A
    change to a golden file needs an entry.
12. **Repository.** Public, on the account of the owner for now. Apache-2.0 for code and CC-BY-4.0
    for the spec text. Commits go to `main` directly until v2.0.0 is released.
13. **Provisional parts.** Some parts of the spec are provisional ([open-work.md](../open-work.md)).
    Each provisional part must be closed before v2.0.0.
14. **Versions of dependencies.** Each one is pinned exactly, to a release that is at least 14 days
    old.

This entry supersedes [ADR-TDB5](TDB5-whole-recording-no-manifest.md) and
[ADR-W4PF](W4PF-shared-package-and-no-overlays.md) in full. Items 8 to 14 restate TDB5 items 7 to
13. Item 1 replaces TDB5 items 1 and 5: the scope is the whole folder, and both info JSONs are in
it. TDB5 item 2 (no manifest) is withdrawn: [ADR-5XNA](../../recording-files/decisions/entries/5XNA-folder-layout-names-and-manifest.md)
adds a manifest. TDB5 item 3 (takes) is replaced by ADR-5XNA. TDB5 item 4 (canonical reader result)
is restated in [ADR-KW3G](../../recording-files/decisions/entries/KW3G-reader-result-for-the-folder.md). TDB5 item 6 (legacy stays out) is
replaced by [ADR-CZQ9](../../recording-files/decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md). Item 5 restates W4PF
items 1 and 2. Item 2 restates W4PF item 3 for each file of the folder. Item 7 restates W4PF items 5
to 7 and replaces its item 8 (tracking is later work). W4PF item 4 (the spec fixes no file or folder
names) is replaced by ADR-5XNA. Item 6 limits the JavaScript reader of W4PF item 2. Items 3 and 4
are new.

## Reason

- The user wants one spec that another program can use to make a compatible folder, or to read
  freemocap output (round 1, A1 (a)).
- A reader of the whole folder needs fixed rules for every file, not only for the media files.
- freemocap-ui gets 2D and 3D data from the freemocap Python server, so the JavaScript reader does
  not need Parquet or TOML.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  section "Grilling log": round 1 A1, round 2 Q3, Q4 and Q16 (local, not committed).

## Alternatives rejected

- The spec defines the media files and a frozen core of each freemocap file, and freemocap keeps
  the rest (plan option A1 (b)): the user wants every file in full.
- The spec covers only the folder rules and points to the freemocap documents (A1 (c)): another
  program could not implement the folder from the spec alone.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
