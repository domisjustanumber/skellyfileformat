# 0YV1 — The fitted time is in the sidecar, and the player uses it

**Status:** superseded by [FF01](FF01-fit-and-breakpoints-in-metadata.md), 2026-11-13 (commit to main; was accepted, 2026-11-12).

## Decision

1. At finalisation, the writer computes the fitted time of each frame. It writes the fitted time and
   its flags into the record of that frame in the video timing sidecar.
2. The player uses the fitted time.
3. Before finalisation, a file has no fitted time. The player then uses the arrival time.
4. The fitted time is in the sidecar. It is not only in a timestamp CSV file.

## Reason

- A reader that has only the MKV file gets the player time from the file itself.
- A CSV file is specific to skellycam, and it can become separated from the video file.

## Evidence

- Plan row S2 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.
