# E68K — The forgiving camera match, the order of a repair, the SFT-717 forms, a sidecar alone with no readable `take_uuid`, the files of G5 and G6

**Status:** absorbed into
[`spec/SPEC.md#8-video-timing-sidecar`](../../SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#13-capture-info-json`](../../SPEC.md#13-capture-info-json),
[`spec/SPEC.md#20-opening-a-folder`](../../SPEC.md#20-opening-a-folder),
[`spec/SPEC.md#appendix-a-golden-folders`](../../SPEC.md#appendix-a-golden-folders),
[`spec/conformance.md#timing-sidecars-sections-7-8-and-10`](../../conformance.md#timing-sidecars-sections-7-8-and-10),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; questions Q104, Q108, Q122, Q123 and Q124 of round 3 of
the review of the golden folders)).

## Decision

The user accepted these rules. Each item gives its question number.

1. **The forgiving camera match (Q104).** A remembered camera is a candidate when its `vendor_id`
   and its `product_id` are equal to those of the new camera, and are not null. When one of the two
   is null in the new camera or in the remembered camera ([ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 1, Q138;
   corrected on 2026-11-17), the remembered camera is a candidate when `model` is equal. A program never compares
   `os_name`. The prompt shows the live preview, `user_name`, `camera_label` and `model` (SFF-752).
2. **The `device` names (Q104).** `device.model` is the product text that the camera reports
   about itself: the USB product string. `device.os_name` is the name that the capture API lists
   for the camera (section 13).
3. **The order of a repair (Q108).** A repair does each step for the whole take before the next
   step: (1) it cuts each media file; (2) it cuts each sidecar; (3) it appends the footer lines
   in three passes, each across all sidecars: the fit lines, then the `# repair` lines, then the
   `# end` lines; (4) it writes the manifest. An interrupted repair leaves the manifest in the state
   `recording`. A repair that stops in step 3 can leave some sidecars `repaired` and the others
   `unfinished`. The program asks again, and a new repair finishes the rest. The case
   `interrupted_repair` of G06 stopped in the `# repair` pass, so each of its sidecars is
   `unfinished` (SFF-793, SFF-798). (The words "the whole take unfinished, never half repaired"
   and "the fit lines and `# end`" are corrected on 2026-11-17: [ADR-158N](158N-details-for-the-decisions-of-round-3.md) items 3 and 12, Q132 and Q131.) This order replaces the pair-by-pair order.
4. **A serial that the key does not use (Q122).** When `device.serial` is present but the writer
   does not use it for the key, the file records no reason. SFT-717 passes when a `computed` key is
   equal to the hash of one of the forms 1 to 3, built from the `device` values of the file
   (SFF-752).
5. **A timing sidecar alone whose `take_uuid` the reader cannot read (Q123).** The sidecar is in
   `other_files` as `invalid`, with the reason for bad header metadata. The folder gets the warning
   for a file that belongs to no take. The user accepted the intent: the spec uses the reason code
   and the warning name that SPEC.md already has for these two things (SFF-865).
6. **The files of G5 and G6 (Q124).** Besides the device pairs, G5 and G6 hold the manifest and the
   capture info JSON. They hold no Parquet and no TOML. Appendix A says so.

## Reason

The user answered "otherwise agree" to the recommendations of round 3 of the review on
2026-11-16. The user gave no reason for these items. Item 3 closes the conflict of the
pair-by-pair order with the case `interrupted_repair` of G06
([ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md), "Reason").

## Alternatives rejected

- Item 3: the pair-by-pair order that the user decided first on 2026-11-16 (for each pair: the
  media file, the sidecar, the fit lines and `# end`; then the manifest). It did not agree with the
  case `interrupted_repair` of G06.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
