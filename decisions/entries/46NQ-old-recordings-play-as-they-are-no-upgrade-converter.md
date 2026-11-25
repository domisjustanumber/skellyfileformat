# 46NQ — Old recordings play as they are: no `<video>` path and no "upgrade recording" converter

**Status:** absorbed into [`recording-files/README.md#scope-normative`](../../recording-files/README.md#scope-normative), [`recording-files/README.md#compatibility-promise-normative`](../../recording-files/README.md#compatibility-promise-normative), [`recording-files/README.md#versioning-normative`](../../recording-files/README.md#versioning-normative), [`recording-files/README.md#implementations`](../../recording-files/README.md#implementations), [`README.md#licenses`](../../README.md#licenses), [`recording-files/AGENTS.md#1-purpose`](../../recording-files/AGENTS.md#1-purpose), [`recording-files/AGENTS.md#2-test`](../../recording-files/AGENTS.md#2-test), [`recording-files/AGENTS.md#3-project-rules`](../../recording-files/AGENTS.md#3-project-rules), [`AGENTS.md#6-git-rules`](../../AGENTS.md#6-git-rules), [`AGENTS.md#8-private-data`](../../AGENTS.md#8-private-data), [`recording-files/SPEC.md`](../../recording-files/SPEC.md#skellyspecs-recording-format-specification), [`recording-files/parts/parquet-descriptor.md#structure-rules-and-writer-rules`](../../recording-files/parts/parquet-descriptor.md#structure-rules-and-writer-rules), [`recording-files/legacy-annex.md`](../../recording-files/legacy-annex.md#legacy-annex-freemocap-v1x-recording-folders-informative), [`recording-files/conformance.md`](../../recording-files/conformance.md#skellyspecs-recording-format-conformance-tests), [`recording-files/golden/README.md#golden-folders`](../../recording-files/golden/README.md#golden-folders), 2026-11-25 (commit on dom/v1-player-rules; was accepted, 2026-11-25 (user; answer Q805 of the owner session of 2026-11-25)).

## Decision

This entry supersedes [ADR-YBT1](YBT1-spec-only-test-adapter-and-labels.md) in full. It changes
the rules of YBT1 about the old recordings in skellycam.

**Changed rules.**

1. skellycam plays old recordings as they are. It converts no old recording, and it has no legacy
   `<video>` path for old H.264 recordings. Its player reads the camera files of a v1 folder by
   SPEC.md SFF-896 to SFF-903.
2. skellycam has no "upgrade recording" converter. Item 1 of YBT1 loses "the 'upgrade recording'
   converter" from the list of what skellycam owns. The rules of CZQ9 items 3 and 4, which YBT1
   restated through section 21 and the legacy annex, are removed.
3. The conversion writer of SPEC.md section 1 and the conversion of `TakeWriter` in the test adapter
   stay. This entry changes no requirement and no test.

**Kept rules.** Each other rule of YBT1 stays, also its restatements of the entries that it
superseded. The headings of the status of this entry state them, as they stated them for YBT1.
[Legacy annex section 8](../../recording-files/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap)
and [Implementations](../../recording-files/README.md#implementations) state the changed rules.

## Reason

- The owner of skellycam ruled on 2026-11-24 that old recordings must not be converted and play as
  they are (skellycam ADR-X5MZ). He cancelled the "upgrade recording" converter (skellycam
  ADR-0C4Y, Q705). The v1 player of skellycam replaces the old `<video>` player (skellycam Q800).
- The legacy annex and the README of recording-files still stated the old rules.

## Alternatives rejected

- Keep the old text as a rule of the programs: it would contradict the programs.
