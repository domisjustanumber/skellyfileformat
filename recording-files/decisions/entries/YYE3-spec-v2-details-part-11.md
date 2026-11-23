# YYE3 — Spec draft v2 details, part 11: manifest after a repair, torn bytes, legacy result

**Status:** absorbed into
[`spec/SPEC.md#7-csv-timing-sidecars-common-rules`](../../SPEC.md#7-csv-timing-sidecars-common-rules),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`spec/SPEC.md#layout-and-cases`](../../SPEC.md#layout-and-cases),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

This part holds items 26a, 28 and 29 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. Items 26 (the manifest `state` after a
repair) and 27 (a left-over journal in a finished take) are not proposals. The user decided them.
They are items 1 and 2 of the accepted entry
[ADR-JB3A](JB3A-repair-state-question-and-skellycam-lock.md). Item 26a is not from the review. The user
accepted items 26a, 28 and 29 on 2026-11-16.

26a. **Details of the manifest after a repair** (section 5, SFF-724, SFF-793, SFF-795; SFT-733;
    G6). It builds on
    [ADR-JB3A](JB3A-repair-state-question-and-skellycam-lock.md) item 1, which is accepted: the
    repair sets `state` to `finished`. When the repair of a take ends, the program that did the
    repair writes the manifest while it holds `.processing.lock`. It sets `writer` to its writer
    string. It computes the summary again (item 24). It adds the warning `camera_gap` for a
    repaired video sidecar with `gaps` more than 0. It changes no other member. A repair that stops
    before its end leaves `state` `recording`. The order of a repair is: the media files and their
    sidecars, then the manifest, then the fold of a left-over journal (SFF-844). So the fold uses
    the fit of the repaired sidecars. When the take has no manifest that a reader uses (item 25),
    the repair writes no manifest. Basis (1):
    [ADR-JB3A](JB3A-repair-state-question-and-skellycam-lock.md) item 1; (3).

28. **`torn_bytes` and footer lines** (SFF-745 to SFF-747, SFF-781, SFF-784, SFF-791, SFF-795,
    SFF-798, SFF-885; SFT-716, SFT-732, SFT-733; G1, G5, G6).
    - a. `torn_bytes` of a `files` item is an integer for each state other than `invalid` and
      `unsupported_version`. It is the sum of two numbers. The first is the number of bytes of the
      last line of the sidecar when that line has no LF, else 0. The second is the number of bytes
      of the media file after its last complete block or fragment when the last line of the
      sidecar is not an `# end` line, else 0. So it is 0 for a `finished` and for a `repaired`
      pair. For the `damaged` sidecar of G5, it does not count the row with the wrong CRC or the
      rows after it: they are complete lines.
    - b. A reader reads no data row after the first footer line. A complete footer line counts in
      no member. A torn footer line counts in `torn_bytes`.
    - c. A sidecar is `repaired` only when it has a `# repair` line and its last line is an `# end`
      line. With another last line it is `unfinished`, also when it has fit lines and a `# repair`
      line. A reader uses the fit lines only of a `finished` or `repaired` sidecar. So each sidecar
      of `interrupted_repair` of G6 is `unfinished`, with `fit` false and `missing_fit`.

    Basis (1): [ADR-ATW0](ATW0-spec-v2-details-part-6.md) item 9 and
    [ADR-G1YG](G1YG-writing-crash-reading-and-repair.md) items 5 and 8; (3).

29. **Legacy result of `pre_v1` and `unknown`** (SFF-876, SFF-877, SFF-880, SFF-885; SFT-764; G15).
    For `pre_v1`, `release_range` is null, `ambiguous` is false, and `eras` and `warnings` are
    `[]`, as for `unknown`. `calibration` is null for `pre_v1` and for `unknown`: the lookup of
    SFF-880 is only for `v1`. The note "freemocap pre-v1 layout, unsupported" is guidance for the
    program that shows the folder. It is not in the reader result. In a `legacy` folder, `takes` is
    `[]`. `other_files` follows the general rule: it lists each file of the root and of
    `synchronized_videos/`, not of their subfolders, as `not_in_format`, or as `invalid` with
    `code_in_file` for a pickle (SFF-884). Basis (1):
    [ADR-KW3G](KW3G-reader-result-for-the-folder.md) items 7 and 10, and
    [ADR-ATW0](ATW0-spec-v2-details-part-6.md) item 11 (a text for people is not in the result).

## Reason

- Item 26a: the manifest of G6 needs each member after a repair, not only `state`.
- Item 28: SFF-791 gives `torn_bytes` only for an unfinished pair. G1, G5 and G6 need each case.
- Item 29: G15 needs each member of `legacy` for each family.

## Evidence

skellyfileformat, `spec/SPEC.md`: SFF-793 gives the `state` after a repair and no other member of
the manifest. SFF-844 and SFF-845 give no order for the repair and the fold.

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): link repair._
