# QDF0 — The form of a camera label, the range of `group_position` and the Input line of SFT-762

**Status:** absorbed into
[`spec/SPEC.md#7-csv-timing-sidecars-common-rules`](../../SPEC.md#7-csv-timing-sidecars-common-rules),
[`spec/SPEC.md#8-video-timing-sidecar`](../../SPEC.md#8-video-timing-sidecar),
[`spec/conformance.md#opening-a-folder-section-20`](../../conformance.md#opening-a-folder-section-20),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q190 to Q192 of round 16)).

## Decision

The user accepted these items. Each item gives its question number.

1. **The form of a camera label (Q190).** The form of SFF-720, which the refusal rule of SFF-753
   uses, is the pattern only: 6 to 8 lowercase hexadecimal characters, or `cam<N>`. A reader does
   not refuse a label that is not the start of the `camera_key` of its own camera. SFF-753 states
   this in one sentence.
2. **The range of `group_position` (Q191).** The range of `group_position` (0 to `group_size` − 1
   in the header table of section 8) is not a form check of SFF-748. A reader reads a sidecar with
   a `group_position` at or above `group_size` normally. The count of SFF-869 reports the extra
   file (`extra_files`). SFF-748 states this in one sentence.
3. **The Input line of SFT-762 (Q192).** The Input line of SFT-762 also names the sidecars that
   disagree on `group_size`. This is a text addition only. The Pass text does not change.

## Reason

- Item 1: the cases `one_label` of SFT-762 give camera 1 the label of camera 0. With item 1, these
  cases get `duplicate_label` (SFF-870), as the tests expect.
- Item 2: the third sidecars of SFT-761 and SFT-762 have `group_position` 2 and `group_size` 2.
  With item 2, these sidecars are not `bad_metadata`. They get the results that the tests expect:
  `missing_media` in SFT-761 and `extra_files` in SFT-762.
- Item 3: an Input line names each input of its test. The test already has the case
  `group_size_disagrees`.

## Consequences

- No test and no golden file changes. The case `bad_label` of G11 has the label `nothex`, which is
  not the pattern. Thus it stays `bad_label`. Each golden label is the first 6 characters of its
  `camera_key`. No golden case has a `group_position` at or above `group_size`.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
