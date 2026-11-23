# 1HH0 — The lock and the journal; no automatic change at start-up; privacy kinds; era chains

**Status:** absorbed into
[`spec/SPEC.md#12-writing-crashed-files-and-repair`](../../SPEC.md#12-writing-crashed-files-and-repair),
[`spec/SPEC.md#16-tracking-parquet`](../../SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#17-realtime-journal`](../../SPEC.md#17-realtime-journal),
[`spec/SPEC.md#21-legacy-folders`](../../SPEC.md#21-legacy-folders),
[`spec/SPEC.md#22-privacy-and-safety`](../../SPEC.md#22-privacy-and-safety),
[`spec/SPEC.md#23-the-reader-result`](../../SPEC.md#23-the-reader-result),
[`spec/conformance.md#tracking-parquet-the-reader-and-the-models-section-16`](../../conformance.md#tracking-parquet-the-reader-and-the-models-section-16),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

1. **The lock and the journal.** An append to the journal needs no lock. `.processing.lock` covers
   only whole-file writes: the manifest, the info JSONs, the calibration TOML, the Parquet and the
   exports. The journal is a live append-only file, like a camera file (SPEC.md SFF-789, SFT-730).
   Reason: freemocap appends to the journal during the whole take, and skellycam needs the lock to
   write the manifest at the end of the take.
2. **Start-up with an unfinished take.** The words of the user: "on startup, if files are found in
   recording state, freemocap or skellycam prompt the user if they want to repair the file." No
   program folds a journal or changes a file automatically at start-up. A program that finds an
   unfinished take asks the user the question of SPEC.md SFF-793. When the user agrees, the program
   repairs the files, and freemocap folds a left-over journal as part of that repair. When the user
   does not agree, nothing changes, and a reader still reads the files in place (SFF-793, SFF-844,
   SFF-845, SFT-733, SFT-751, SFT-758). This item changes the last sentence of
   [ADR-Q9X2](Q9X2-realtime-tracking-journal.md) item 5: "At start-up, freemocap folds each journal
   that it finds". Reason: after a crash the manifest `state` stays `recording`, and a repair
   changes the files of the user, so the user decides
   ([ADR-G1YG](G1YG-writing-crash-reading-and-repair.md) item 7).
3. **Privacy kinds.** In the `fields` table of the manifest `privacy` (SFF-881), `/recording_name`
   and the summary `user_name` have the kind `user_entered_name`. The summary `model` has the kind
   `device_name`. Reason: [ADR-DM9S](DM9S-spec-v2-details-part-7.md) item 15b gave no kind for these
   three fields, and the user confirmed the kinds of the spec text.
4. **Legacy eras.** The wording of the era chain rule of SFF-878 is confirmed: "two or more
   chains", and an era row that no other row builds on is a chain of one row. Reason: the user
   confirmed the text that the spec has.
5. **The reader and a model in the descriptor.** SPEC.md has the new requirement SFF-893, with a
   cross-reference from section 16, and conformance.md has the new test SFT-770. They state the
   reader rule of [ADR-W5JC](W5JC-nested-model-types-in-the-descriptor-part.md) item 3 and point to
   `spec/parts/parquet-descriptor.md`. Reason: the rule was only in the part, and no requirement
   and no test stated it.

## Reason

Each item gives its reason. The user decided items 1 to 4 on 2026-11-16, after a review of the
details that the entries of that day applied. Item 5 adds IDs for a decided rule. It changes no
rule.

## Consequences

- A crashed take stays unfinished until the user agrees to a repair. Its realtime results stay in
  the journal until then.
- freemocap has no automatic fold at start-up.

## Alternatives rejected

- The journal under the lock: skellycam cannot then write the manifest at the end of the take.
- An automatic fold at start-up: it changes the files of the user with no agreement.

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._
