# 83Y4 — Recording manifest in the recording info JSON

**Status:** superseded by [5PP8](5PP8-whole-recording-scope.md), 2026-11-12 (commit to main; was accepted, 2026-11-12).

## Decision

1. skellycam extends its recording info JSON. For each camera, it lists the MKV file, the sidecar,
   the key and the Segment UID.

## Reason

- A reader can find the files of a recording and check that each sidecar belongs to its MKV
  without a scan of the folder.

## Evidence

- Plan row S8 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.

## Open work

See [open-work.md](../open-work.md).
