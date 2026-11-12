# CA03 — FLAC audio: a separate `.audio.mka` in skellycam, a track in each camera MKV in skellysync

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. FLAC is the audio codec of the format. Opus is only a possible size option for later. A change to
   Opus needs a new entry.
2. skellycam records the microphone to a separate native `.audio.flac` file while it records. At
   finalisation it stream-copies the FLAC frames into `<rec>.audio.mka` and appends the `.skau`
   timing sidecar to it as an attachment.
3. skellysync writes one FLAC track into each camera MKV, in the same pass as the video.
4. The player decodes FLAC packets by byte offset with the WebCodecs `AudioDecoder`. It finds the
   packets in a packet table. The table is in the `.skau` (skellycam) or in the camera sidecar
   (skellysync).

## Reason

- FLAC is lossless, and a hard kill of the recorder loses no audio.
- The `.mka` file plays complete in VLC. VLC drops the end of a native `.flac` file.
- The player decodes FLAC by offset sample-exact in Electron 45.

## Evidence

- [audio_skellycam FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/audio_skellycam/FINDINGS.md): 0 ms lost for each hard kill of
  the native FLAC writer.
- [flac_skau FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/flac_skau/FINDINGS.md): the stream copy into `.mka` keeps the frames
  byte-identical (1,407 of 1,407); VLC drops the last 26.7 ms of a native `.flac`, and plays the
  `.mka` complete and sample-exact.
- [audio_skellysync FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/audio_skellysync/FINDINGS.md): the FLAC track in each camera MKV.
- Plan row D15 and section 2.8 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.

## Not repeated

- Do not give a native `.flac` file to a player as the final file. VLC drops its last 26.7 ms.
