# 7JJJ — The repair of an audio pair, the header values of a refused sidecar, and the rules of W5AK that stay

**Status:** absorbed into
[`spec/SPEC.md#5-the-recording-manifest`](../../spec/SPEC.md#5-the-recording-manifest),
[`spec/SPEC.md#8-video-timing-sidecar`](../../spec/SPEC.md#8-video-timing-sidecar),
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../spec/SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#13-capture-info-json`](../../spec/SPEC.md#13-capture-info-json),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/conformance.md#capture-info-processing-info-and-calibration-sections-13-to-15`](../../spec/conformance.md#capture-info-processing-info-and-calibration-sections-13-to-15),
[`spec/conformance.md#opening-a-folder-section-20`](../../spec/conformance.md#opening-a-folder-section-20),
[`spec/conformance.md#legacy-folders-section-21`](../../spec/conformance.md#legacy-folders-section-21),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; questions Q146 and Q149 of round 7 of the review of the
golden folders; commit to main)).

## Decision

The user accepted items 2 and 11. Item 2 reverses Q113 in part. So this entry supersedes
[ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) in full. Items 1 to 10 keep the numbers of
W5AK. Each of them except items 2 and 5 restates a rule of W5AK unchanged. Item 5 also holds the
addition of [ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 13 (corrected on 2026-11-17). Each item gives its question
number.

1. **How a reader reads a repaired camera file (Q115).** A reader reads a repaired camera file as
   it reads an unfinished one: with no index and no normal end (SFF-740, SFF-794).
2. **The kept rows of a repair (Q112, Q113, Q146).** A camera repair keeps n frames. n is the
   smaller of two numbers: the rows before the first bad row, and the complete blocks. The repair
   cuts both files to n (SFF-795, SFF-797). A repair cuts the audio sidecar to the blocks that pass
   [ADR-783H](783H-text-corrections-of-the-second-golden-review.md) item 9 (Q145): each sample of
   the block is in a complete fragment. The manifest duration of the audio comes from the audio
   that is kept. The audio file is still cut at its last complete fragment (SFF-796). The case
   `repaired` of G6 is made again.
3. **The usable frames of a repaired camera file (Q115).** Each row of a repaired camera file is a
   usable frame (SFF-754).
4. **The roles of a rebuild (Q116).** In a manifest rebuild, the fixed file name gives the role. The
   TOML gets the role `calibration` (SFF-731).
5. **A folder file of another take (Q117).** A folder file that holds another `take_uuid` stays
   with the take that lists it, or with the take whose `<rec>` its fixed name has. The rule "a
   folder file of this format with no take" applies in a folder with no take. In a folder with a
   take, it applies to a folder file that no manifest lists and whose name has the `<rec>` of no
   take (SFF-889; [ADR-158N](158N-details-for-the-decisions-of-round-3.md) item 13, Q133, corrected on 2026-11-17).
6. **The warning `prerelease` of an `unsupported_version` file (Q118).** The file gets the warning
   `prerelease` only when the reader can read `format_prerelease` and the value is above 0
   (SFF-891).
7. **The check of `key_origin` (Q119).** A `key_origin` that is not one of the three values makes
   the capture info JSON `invalid`, with the reason `bad_schema`. Null is allowed only when
   `camera_key` is 0 (SFF-803).
8. **The scope `player` and a folder with no take (Q120).** Only when the folder has no take, a
   `player` reader reads only the format mark of each TOML, Parquet and journal of the root: the
   TOML `[metadata]` table, the key-value metadata of the Parquet footer and the journal header
   (SFF-892).
9. **New test inputs.** The test inputs that a test makes at test time for SFT-736, SFT-762 and
   SFT-764 are accepted.
10. **A repaired pair whose counts differ (Q114).** A reader refuses a repaired camera pair whose
    rows and blocks differ, as it refuses a finished pair: state `invalid`, with the reason of
    SFF-759.
11. **The header values of a refused sidecar (Q149).** The result shows `camera_key` and
    `camera_label` of a refused sidecar only when the reader can read the header line and the
    value has the correct form. A value of the wrong form is null, as in the case `bad_label` of
    G11 (SFF-885).

## Reason

The user answered "agree to all" to the recommendations of round 7 on 2026-11-17. The user gave no
reason. Item 2 closes the rest of GAP-6 of the second review of the golden results: before it, the
repaired audio sidecar of G6 kept its 21 rows (100,800 samples), but the cut audio file held 47,688
samples. So the summary had `duration_s` 2.1 for 0.99 s of audio, and `records` held `fitted_ns`
past the usable length.

## Consequences

- G6 `repaired`: the audio sidecar keeps 9 rows, its `# end` line has `samples=43200`, and the
  manifest summary has `duration_s` 0.9 for the audio (SFF-728). In G6 `interrupted_repair`, the
  audio sidecar also has the 9 kept rows: the repair cut it before it stopped.
- [ADR-W5AK](W5AK-details-for-the-decisions-q83-to-q111.md) is superseded. Its citations in other
  files stay. Its item numbers are the item numbers of this entry.

## Alternatives rejected

- Item 2: the repair keeps each row before the first bad row, and the audio duration comes from
  those rows (Q113, W5AK item 2).
- Item 11: the header value also when its form is wrong.

## Open work

See [open-work.md](../open-work.md).
