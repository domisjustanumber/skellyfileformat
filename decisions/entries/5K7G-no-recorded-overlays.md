# 5K7G — No recorded overlays

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. skellycam records no overlays. It removes the burned-in `camera.id…fr{N}` stamp from the frames.
2. The format has no overlay file and no overlay attachment. `.skov` is not part of the format.
3. The player draws the frame label from the sidecar.
4. Recorded overlay data from freemocap is later work. This spec will document it if it comes, for
   example as CBOR in CRC-framed records.

## Reason

- The stamp was a visual workaround for out-of-sync `<video>` playback
  ([skellycam commit c4b64f5](https://github.com/freemocap/skellycam/commit/c4b64f5f36ede13f12a8409cd9a2886666d7b5a3)). Only people read it. No code reads it from the pixels.
- The canvas player removes the drift, and the sidecar holds each value that the stamp shows.

## Evidence

- Plan rows S7 and D18 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.

## Alternatives rejected

- `.skov`: a prototype from the overlay study, not a standard.
- SVG: 11 times the size, not safe after a crash, and it stores drawings, not data.
