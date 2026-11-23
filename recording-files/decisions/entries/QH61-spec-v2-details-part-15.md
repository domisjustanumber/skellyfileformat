# QH61 — Spec draft v2 details, part 15: tests that run at gate 2, tests with no Pass text

**Status:** superseded by [YBT1](../../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-16 (commit to main; was accepted, 2026-11-16)).

## Decision

This part holds items 46 and 47 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. The user accepted
them on 2026-11-16, with the recommended option of each CHOICE. Each alternative stays as a record.

46. **Which tests run at gate 2** (conformance.md, "How to read a test";
    [ADR-G21H](G21H-gate-2-tests-location-and-interfaces.md) item 4). In this repository:
    - "skellycam" in an Input line is the package writer `TakeWriter` with synthetic input. "The
      converter" is `TakeWriter` in a conversion. The repair is `repair_take`.
    - A test, or a Pass sentence, is **external** when it needs a run of freemocap, a run of the
      Blender addon, capture hardware or an answer of a user. conformance.md marks it
      `(external: <program>)`. The repository of that program runs it. This repository does not.
    - For an external writer test, this repository runs the **golden part**: each Pass sentence
      that a file of a golden folder can show. A test whose only inputs are golden files is not
      external. Examples are SFT-746, SFT-748, SFT-750 and SFT-753. The test makes the Parquet of
      the G12 vector of SFT-748 with the functions of the golden generator.
    - External, with a golden part: SFT-705 (the names in G3), SFT-737 (G3), SFT-738 and SFT-739
      (G14), SFT-751, SFT-756 and SFT-758 (G13).
    - External, with no golden part: SFT-741, SFT-742, SFT-743 (item 23), SFT-745 and SFT-755.
    - External in part: SFT-703 (the export and the BVH), SFT-708 and SFT-730 (freemocap),
      SFT-711 (the frame count of Blender), SFT-712 (the MJPEG camera), SFT-733 (the question to
      the user) and SFT-749 (the run with one camera).

    Basis (1): [ADR-G21H](G21H-gate-2-tests-location-and-interfaces.md) items 2 and 4; (3).

47. **Tests for requirements with no Pass text.** No new ID is necessary.
    - SFF-714: SFT-703 says that the rule has no case in version 2.0, because each field has
      minor 0. The first minor version that adds a field adds the vector.
    - SFF-719: SFT-705. A `TakeWriter` that gets a folder with a file of this format of another
      take refuses to start.
    - SFF-853: SFT-768, which adds this ID to its Checks. The test adds to a copy of G3 an empty
      file (0 bytes) at the path of an annotated video, and its manifest item. The item is
      `present`, and the other members of the result do not change.
    - SFF-859: SFT-743 (external). A trace shows that the exporter holds `exports/.exports.lock`
      from before its first write in `.staging-*` until after it writes the inventory.
    - SFF-868: SFT-710. The test renames one camera pair of `no_manifest` of G7 to another `<rec>`.
      The take has `take_fact_mismatch`, and `recording_name` is the value of item 34.
    - SFF-889: SFT-768. A folder with only the capture info JSON of G3 is `unreadable`. The file
      is in `other_files` as `invalid`, with `take_fact_mismatch`, and the folder has
      `orphan_file`.
    - SFF-709: SFT-703, with new vectors in `higher_minor` of G10: an unknown key in `[metadata]`
      and in one camera table of the TOML, and the flag bit 7 (128) in one row of one video
      sidecar. A new case `higher_minor_journal` is a copy of G13 whose journal header has `2.1`
      and whose journal has one good record of the unknown type 200. That record counts in
      `records`. The TOML and journal vectors are tests of the Python reader only.
    - SFF-727: SFT-708. The test calls `add_warning` with `control_mismatch` and with
      `awb_not_settled`. The manifest holds each with `source` `skellycam`, its `camera_key` and
      its `detail`. The detection of the two conditions is external (skellycam).

    Basis (1): the pattern of [ADR-72QQ](72QQ-spec-v2-details-part-8.md) item 18; (3).

## Reason

- Item 46: the gate 2 run must not need freemocap, Blender, a camera or a user.
- Item 47: each requirement needs a test with a Pass text that checks it.

## Evidence

skellyfileformat at fe7deba, `spec/conformance.md`: the Input lines of the tests that item 46
names. The classes of item 46 come from these lines. No test was run.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
