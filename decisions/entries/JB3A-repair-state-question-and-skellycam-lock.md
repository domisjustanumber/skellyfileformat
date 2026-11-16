# JB3A — The manifest `state` after a repair; one question for one take; the lock of skellycam

**Status:** accepted, 2026-11-16 (user; review of the repair and lock details).

## Decision

1. **The manifest `state` after a repair.** The repair sets `state` of the manifest to `finished`.
   Each repaired file still reports the state `repaired`, from its `# repair` line. The manifest
   `state` has no third value (SPEC.md section 5, SFF-793; SFT-733). Reason: the timing sidecar is
   the home of the fact of the repair, so the manifest does not copy it
   ([ADR-N6HS](N6HS-info-jsons-and-calibration.md) item 2).
2. **A left-over journal in a finished take.** freemocap asks the user the question of SFF-793
   before it folds a journal that is left over in a take whose manifest already has `state`
   `finished`. It folds only when the user agrees (SFF-793, SFF-845). SFT-758 gets this input: a
   take with `state` `finished` and a journal with no end record, one time for each answer.
   Reason: a fold changes the files of the user, as a repair does
   ([ADR-1HH0](1HH0-lock-startup-repair-and-reader-model-check.md) item 2).
3. **Which program asks.** skellycam asks about a take that it recorded on its own. When freemocap
   runs, freemocap asks one time for the whole take: for the media files and the journal together
   (SFF-793; SFT-733, SFT-758). SFF-793 said "a take that it owns" before. Reason: the user gets
   one question for one take.
4. **The lock for the whole-file writes of skellycam.** skellycam holds `.processing.lock` for each
   whole-file write that it makes: the manifest and the capture info JSON (SFF-789, SFF-801;
   SFT-730, SFT-735). Reason: the lock covers each whole-file write
   ([ADR-1HH0](1HH0-lock-startup-repair-and-reader-model-check.md) item 1), and the capture info
   JSON is one of them.

## Reason

The user decided each item on 2026-11-16. Items 1 and 2 close the two points that
[ADR-1HH0](1HH0-lock-startup-repair-and-reader-model-check.md) item 2 left open. Items 3 and 4
make SFF-793 and SFF-789 exact. The reason of item 3 is from the words of the user. An agent wrote
the reasons of items 1, 2 and 4.

The user decided only the text of item 1 for the manifest after a repair. The other details (the
program that writes the manifest, the summary, the order of the repair and the fold, a repair that
stops early) are a proposal: [ADR-YYE3](YYE3-spec-v2-details-part-11.md) item 26a.

## Alternatives rejected

- A third value `repaired` of the manifest `state`: the `# repair` line of each sidecar already
  holds this fact.
- A fold of a left-over journal of a finished take with no question: it changes the files of the
  user with no agreement.

## Open work

See [open-work.md](../open-work.md).
