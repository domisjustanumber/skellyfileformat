# YT1F — Stage 1a: the converter, the Blender check, inputs on copies of G1 and checks with no reader

**Status:** absorbed into
[`AGENTS.md#4-project-rules`](../../AGENTS.md#4-project-rules),
[`spec/conformance.md#the-stage-of-each-test`](../../spec/conformance.md#the-stage-of-each-test),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q183 to Q186 of round 14
and Q187 to Q189 of round 15)).

## Decision

The user accepted these items. Each item gives its question number. They add to the stages of
[ADR-CPM2](CPM2-stages-of-the-implementation.md), and they change none of its items.

1. **SFT-711 (Q183).** SFT-711 stays in stage 1a. Its external part is a check that a person runs
   by hand one time in stage 1a: Blender, at the pinned version, counts the same number of frames
   in the camera file. The check is about Blender when it opens the video. It is not about the
   Blender addon.
2. **The converter (Q184).** The skellycam converter is in stage 1a. The converter is the writer in
   conversion mode, which changes an old recording to this format. The use of conversion mode by
   skellysync stays in stage 1b.
3. **Inputs on a copy of G1 (Q185).** Some reader rules of stage 1a have tests only on copies of
   G3. G3 holds a Parquet and a calibration TOML, so these cases are in stage 2. These tests get
   the same inputs on a copy of G1, so that they run in stage 1a: SFT-761 (4 cases), SFT-762 (9),
   SFT-707, SFT-709 (3), SFT-736 (3) and SFT-744. The cases on copies of G3 stay in stage 2. These
   are additions to the tests. They are part of the review of stage 1 by the user.
4. **Checks with no reader (Q186).** A check on golden files that runs no reader has the stage of
   the kind of file that it inspects. Thus the check of the processing info JSON (`golden_part` of
   SFT-737) is in stage 1a (Q178, [ADR-CPM2](CPM2-stages-of-the-implementation.md) item 11). The
   checks of the Parquet, the calibration TOML and the journal stay in stage 2. The section "The
   stage of each test" of `spec/conformance.md` states the rule.
5. **The split of SFT-737 (Q187).** `golden_part` of SFT-737 checks the processing info JSON alone,
   in stage 1a. The comparison of that file with the Parquet is the test function
   `golden_part_against_the_parquet`, in stage 2.
6. **The check of the manifest of G3 (Q188).** `check_on_golden[G03/take]` of SFT-708 is in stage
   1a, by item 4. It opens the manifest, the capture info JSON, the sidecars, the camera files and
   the hashed bytes of the processing info JSON. It opens no TOML and no Parquet.
7. **The Input lines (Q189).** The `Input:` line of each of the six tests of item 3 also names its
   inputs on a copy of G1. This is a text addition only. The Pass text does not change.

A fact that the user recorded (not a decision): the stage 1a reader needs a TOML parser. It reads
the calibration TOML of a legacy folder (G15) to tell the legacy eras apart.

## Reason

- Item 1: the check is about Blender when it opens the video. It needs no addon and no freemocap
  run.
- Item 2: the converter is the package writer `TakeWriter` in a conversion. Its cases in SFT-705
  and SFT-717 need no file of a later stage.
- Item 3: these are reader rules of stage 1a. Without the copies of G1, no stage 1a test checks
  them.
- Item 4: a check with no reader inspects only files. The kind of file gives the stage.
- Items 5 and 6: they apply item 4.
- Item 7: an Input line names each input of its test.

## Consequences

- The application of item 4 to each check:
  - A check that inspects files of two stages has the later stage (item 5).
  - A check of the name of a file inspects that file. Thus `golden_part` of SFT-705 (the names in
    G3, also of the TOML and the Parquet) stays in stage 2.
  - The check `check_on_golden[results]` of SFT-703 inspects the committed results, so it is in
    stage 1a, as `committed_results` of SFT-768 and SFT-769.
- The case `g9` of SFT-762 reads the golden cases of G9. It has no copy of G1, so 8 of its 9 cases
  have a copy of G1.
- SFT-736 also gets the case `confirmed_key`, in stage 1a. It reads the case `confirmed_key` of G1,
  which its Input line names.

## Open work

See [open-work.md](../open-work.md).
