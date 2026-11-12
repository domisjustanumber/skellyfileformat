# X7FT — Read old recordings, write only the new format

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. New skellycam and freemocap keep reading each recording format that the current code writes.
2. New skellycam and skellysync write only this format: JPEG in MKV with skellyfileformat sidecars,
   and FLAC audio.
3. A recording with no skellyfileformat sidecar is a legacy recording.
4. skellycam plays old H.264 recordings through a legacy `<video>` path. It also gives an explicit
   "upgrade recording" conversion, for the other old files and on request.
5. skellycam owns the converter. The converter uses `skellyfileformat[write]`.
6. This spec covers only the new format. skellycam defines how it reads legacy recordings.

## Reason

- Users keep their old recordings. A program that writes two formats doubles the test work.

## Evidence

- Plan rows D19, S10 and S10c, and section 2.9 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.
- Old audio is 9–74 ms early ([audio_skellycam FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/audio_skellycam/FINDINGS.md),
  section 4.1). This is the reason for open item S10b.

## Open work

See [open-work.md](../open-work.md).
