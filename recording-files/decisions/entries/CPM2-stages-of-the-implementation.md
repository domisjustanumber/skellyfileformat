# CPM2 — The stages of the implementation

**Status:** superseded by [YBT1](../../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q168 to Q180 of rounds 11
and 12, and Q181 of round 13))).

## Decision

The user accepted these items. Each item gives its question number. The user started the questions
with: "This work must be broken into stages". The four stages are: 1 Recording, 2 Realtime
capture, 3 Posthoc capture, 4 Blender.

1. **Gate 2 for each stage (Q168).** The user approves gate 2 stage by stage. The review now covers
   only the tests and the golden folders of stage 1. The user reviews the others just before their
   stage starts. The spec and the test list stay whole documents. Only the approval and the
   implementation are staged. This changes item 2 of
   [ADR-Z641](Z641-program-guidance-gate-2-scope-and-no-push.md), which is corrected in place. Its
   other rules stay: an approval does not cover the provisional points that wait for a desk test or a
   hardware test, and the implementation writes only their provisional behaviour.
2. **The order in a stage (Q169).** In each stage, the order of Q167 ([ADR-Z641](Z641-program-guidance-gate-2-scope-and-no-push.md) item 4) applies: the
   Python reader, then the Python writer, then the JavaScript reader. The JavaScript reader is
   built only in stage 1.
3. **Stage 1a and stage 1b (Q170).** Stage 1a is the recording and playback of skellycam. It
   starts after the approval of stage 1. Stage 1b is the skellysync folders (SPEC.md section 19,
   G17). It starts after the five skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO.
   Stage 1a does not wait for stage 1b.
4. **The calibration TOML (Q171).** The TOML is in stage 2. Stage 1 lists the file but does not
   read it, except for what the scope `player` and the format mark need (item 10).
5. **Legacy folders (Q172).** All legacy recognition is in stage 1. No later stage adds to it.
6. **Repair (Q173).** The media repair is in stage 1: the media files, the sidecars, the fit lines
   and the manifest. The fold of a left-over journal is in stage 2, and it is work of freemocap.
   skellycam gets no more repair work in stage 2. A stage 1 repair does not change a journal.
7. **The end of a stage (Q174).** A stage ends when its conformance tests pass and the program has
   adopted it. skellycam records and plays with the package before stage 2 starts. freemocap runs
   a realtime capture with the package before stage 3 starts.
8. **Exports (Q175).** Exports (section 18.3) are the last part of stage 3. They do not block
   stage 4. Annotated videos and logs come first in stage 3.
9. **Stages 3 and 4 (Q176).** Stages 3 and 4 are work in freemocap and in the Blender addon. The
   part of this repository: accept their output as golden files when the exporter and the addon are
   ported, and keep the spec text correct. The package is complete at the end of stage 2. All
   Parquet reading is in stage 2, for realtime and posthoc runs.
10. **The reader in stage 1 (Q177).** In stage 1, the reader is complete in the scope `player` for
    every folder, so the JavaScript reader needs no work after stage 1. In the scope `full`, a
    stage 1 reader stops with a clear "not in this version" error on a folder that holds a
    calibration TOML, a Parquet or a journal. The format gets no new state for this. The tests that
    need the scope `full` on such a folder pass in stage 2.
11. **The processing info JSON (Q178).** Stage 1 reads and validates the processing info JSON. The
    `take_uuid` mismatch case of G9 in the scope `player` needs it.
12. **The stage 1 repair and later files (Q179).** The stage 1 repair refuses, with a clear message,
    a take that holds a calibration TOML or a Parquet, because the manifest summary needs values
    from them. Stage 2 adds the full repair, with a new test and a golden case. The user reviews them
    at the gate of stage 2.
13. **Code in NPY and NPZ files (Q180).** The check of `.npy` and `.npz` headers for code (SFF-884)
    is in stage 1.
14. **A legacy calibration TOML (Q181).** The "not in this version" error of item 10 applies only
    to a calibration file of this format (SPEC.md section 15). An old-style calibration TOML in a
    legacy folder does not cause the error. The stage 1 reader reads a legacy folder in the scope
    `full` (item 5, SFT-764).

The stage of each test and each golden folder follows from these items. A table in
`spec/conformance.md` gives it, and the tests get a pytest mark for each stage.

## Reason

- Item 1: the user can approve and use the recording parts before the processing parts are
  reviewed. The format stays one spec, so the staging changes no rule of the format.
- Items 2, 9 and 10: the JavaScript reader reads only the scope `player` (SFF-892). When stage 1
  is complete in that scope, the JavaScript reader is complete.
- Item 10: SFF-892 has no "not implemented" state in the scope `full`, and the format must not get
  one for a stage of one implementation. A clear error is not a result, so no result is wrong.
- Item 11: the committed `player` result of G9 `take_uuid` shows a mismatch that only the processing
  info JSON gives (SFF-889, SFF-892).
- Item 12: SFF-728 makes the repair compute the summary again, with values from the TOML and the
  Parquet. A stage 1 package cannot read them, and G5 and G6 hold neither file.
- Item 13: the check reads only a header, and it does not depend on section 18.3. With it, G16 is
  complete in stage 1.

## Consequences

- Many tests that run the scope `full` on G3 or on a copy of G3 move from stage 1 to stage 2.
- The two tests of the package in the staged build (the "not in this version" error and the
  refusal of the stage 1 repair) are not in `spec/conformance.md`. They are open work.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
