# W5AK — Details of the decisions Q83 to Q111: kept frames of a repair, repaired files, rebuild roles, `key_origin`, `player` marks of a folder with no take

**Status:** accepted, 2026-11-16 (user; questions Q112 to Q120 of round 3 of the review of the
golden folders, and item 9; commit to main; was proposed, 2026-11-16, with the details that
applying [ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md),
[ADR-XR63](XR63-reader-rules-of-the-golden-review.md) and
[ADR-2MQE](2MQE-tests-prerelease-serial-and-exports.md) to the spec needed).

## Decision

The user accepted these rules. Each item gives its question number.

1. **How a reader reads a repaired camera file (Q115).** A reader reads a repaired camera file as
   it reads an unfinished one: with no index and no normal end (SFF-740, SFF-794).
2. **The number of kept frames (Q112, Q113).** A camera repair keeps n frames. n is the smaller of
   two numbers: the rows before the first bad row, and the complete blocks. The repair cuts both
   files to n (SFF-795, SFF-797). The audio repair does not change: the equal cut is only for a
   camera pair (SFF-796).
3. **The usable frames of a repaired camera file (Q115).** Each row of a repaired camera file is a
   usable frame (SFF-754).
4. **The roles of a rebuild (Q116).** In a manifest rebuild, the fixed file name gives the role. The
   TOML gets the role `calibration` (SFF-731).
5. **A folder file of another take (Q117).** A folder file that holds another `take_uuid` stays
   with the take that lists it, or with the take whose `<rec>` its fixed name has. The rule "a
   folder file of this format with no take" applies only when the folder has no take (SFF-889).
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

## Reason

The user answered "otherwise agree" to the recommendations of round 3 of the review on
2026-11-16. The user gave no reason for these items.

## Open work

See [open-work.md](../open-work.md).
