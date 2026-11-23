# 2MQE — Test wording, golden conventions, `format_prerelease` after external review, the usable serial, exports out of gate 2

**Status:** absorbed into
[`README.md#versioning-normative`](../../README.md#versioning-normative),
[`spec/SPEC.md#3-versioning`](../../SPEC.md#3-versioning),
[`spec/SPEC.md#8-video-timing-sidecar`](../../SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#183-exports`](../../SPEC.md#183-exports),
[`spec/SPEC.md#appendix-a-golden-folders`](../../SPEC.md#appendix-a-golden-folders),
[`spec/SPEC.md#layout-and-cases`](../../SPEC.md#layout-and-cases),
[`spec/conformance.md#timing-sidecars-sections-7-8-and-10`](../../conformance.md#timing-sidecars-sections-7-8-and-10),
[`spec/conformance.md#tracking-parquet-section-16`](../../conformance.md#tracking-parquet-section-16),
[`spec/conformance.md#privacy-and-safety-section-22`](../../conformance.md#privacy-and-safety-section-22),
[`golden/README.md#golden-folders`](../../golden/README.md#golden-folders),
[`golden/README.md#layout`](../../golden/README.md#layout),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q97 to Q103, Q105, Q107 and Q111 of the review
of the golden folders)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **SFT-767 and the pickle (Q97a).** The test makes, at run time in a temporary folder, a pickle
   that creates a marker file if a program loads it. The test passes when no marker file is
   created. The committed pickle of G16 stays harmless.
2. **The preamble of Appendix A (Q97b).** Each file that holds `format_prerelease` has the warning
   `prerelease`, not each file.
3. **A rotated camera in G3 (Q98).** Camera 1 of G3 gets `display_rotation` 90: the input of
   SFT-749. G3 and its copies (G7, G8, G9 and parts of G10) are made again.
4. **SFT-747 (Q99a).** The truth file of G3 holds a SHA-256 of the raw values that the generator
   meant to write to the Parquet. The test checks the four Parquet readers against it.
5. **SFT-748 (Q99b).** A small Parquet for the G12 vector (two rows with equal fitted times) is
   committed in G12 as fixed bytes.
6. **SFT-720 (Q100).** The bitrate must be 0.5 to 1.2 times the setting (128 kbit/s for each
   channel). The Pass text gives this tolerance.
7. **The other choices of the golden folders (Q101).** The other items of the choices lists
   (`golden/CAPTURE_VECTORS_CHOICES.md`, `G03_CHOICES.md`, `G15_CHOICES.md`, `G16_CHOICES.md`,
   `G07_G09_CHOICES.md` and `G10_G13_G14_CHOICES.md`) are accepted as conventions of the golden
   folders, as for G1 ([ADR-94YQ](94YQ-golden-g1-review-decisions.md) item 5). They are not
   format rules.
8. **`format_prerelease` (Q102).** `format_prerelease` stays 1 until the user sends the draft to
   external review. After that, each revised draft that goes to reviewers adds 1. The released 2.0
   writes 0. A reader treats each value above 0 in the same way: the warning `prerelease`.
   `README.md` gets the same rule (SFF-710, SFF-891).
9. **The usable serial (Q103).** The detail of a usable serial is accepted as SPEC.md has it: only
   the characters 0x21 to 0x7F, no `,`, not one repeated character, and the list of known
   placeholders. The list does not change in major version 2. The paragraph is not provisional
   now (SFF-752).
10. **A new camera with the key of a remembered camera (Q105).** When the computed key of a new
    camera is equal to the key of a remembered camera, and the user says that it is not that
    camera, the camera gets an assigned key: form 4, `key_origin` `assigned` (SFF-752).
11. **`port_path` (Q107).** The sources of `port_path` on each operating system stay provisional
    until the cross-platform test scripts at the end of this work run on Linux and macOS (SFF-752).
12. **Exports (Q111).** Exports are not in gate 2. Section 18.3 is provisional. G3 holds no export.
    SFT-743 has no golden part until the freemocap exporter is ported.

## Reason

The user answered "otherwise agree" to the recommendations of the review on 2026-11-16. The user
gave no reason for these items. Q96 was withdrawn, with no change.

## Consequences

- The golden generator makes G3 and its copies again (item 3), and adds the Parquet of item 5
  to G12. This entry is the decision entry that `AGENTS.md` section 4 needs for these changes of
  the golden files.
- Items 8, 9 and 10 close points of open-work.md. Item 11 keeps the point of `port_path` open.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
