# D9N1 — Opus audio: messages, channel metadata, encoder settings, timing and decoding

**Status:** accepted, 2026-11-13 (user).

## Decision

1. Opus (RFC 6716) is the audio codec of the format. FLAC is withdrawn.
2. An audio packet is one MCAP Message with the schema `foxglove.CompressedAudio` and
   `format: "opus"`. The `data` field holds one complete raw Opus packet, with no Ogg, WebM or other
   container framing. The audio is mono or stereo.
3. The `metadata` map of the audio Channel holds the channel count, the pre-skip and the output gain
   of the Opus identification header (`OpusHead`, RFC 7845 section 5.1), and the whole `OpusHead` as
   base64. Its `sample_rate` is the decode rate, 48000. It is not the input sample rate of
   `OpusHead`. The spec gives the keys.
4. A writer writes an output gain of 0. A reader compares the output gain of the metadata with
   `OpusHead`.
5. **Encoder settings.** The channels of the microphone device, at most 2; a writer downmixes a
   device with more. 48 kHz, 20 ms packets (960 samples). Application `audio`. VBR at 128 kbit/s for
   mono and 256 kbit/s for stereo, complexity 10.
6. **Timestamps.** The `timestamp` of a packet is the host-clock time of its first decoded sample,
   with the encoder's priming samples included. So packet 0 starts `pre_skip` samples before the
   first real sample. The `log_time` of a packet is the arrival time of the callback block that
   completed it ([ADR-752H](752H-timing-fields.md)).
7. **Decoding.** A reader decodes the raw packets with no Opus header given to the decoder (in
   WebCodecs: no `description`). The reader drops the first `pre_skip` decoded samples of the stream
   itself.
8. After a seek, a reader decodes from 80 ms before the target and discards that audio (the Opus
   seek pre-roll that Matroska `A_OPUS` gives).
9. skellycam records the microphone to its own MCAP file. skellysync writes its audio as Opus in
   MCAP. The spec gives the file layout of each.
10. The player decodes the Opus packets with the WebCodecs `AudioDecoder`.

This entry supersedes [ADR-HD8Z](HD8Z-opus-audio.md) and
[ADR-QDZ7](QDZ7-opus-settings-and-timing.md) in full. Items 1, 2, 8, 9 and 10 restate HD8Z items 1,
2, 5, 6 and 7. Item 3 restates HD8Z item 3, with the decode rate in place of the input sample rate.
Item 7 restates HD8Z item 4 and QDZ7 item 3. Item 5 restates QDZ7 item 1. Item 6 restates QDZ7 item
2, with the arrival time as the `log_time` in place of "the base of its `log_time`". Item 4 is new.

## Reason

- The `log_time` of a camera frame is its arrival time. The same rule for audio keeps the two
  alike, and it agrees with ADR-752H item 2. The QDZ7 text disagreed with it.
- The `OpusHead` input sample rate is only a record of the source (RFC 7845 section 5.1). A decoder
  gives 48 kHz. A 44.1 kHz microphone would have written 44100, and a reader could use the wrong
  rate.
- RFC 7845 says that players should apply the output gain. WebCodecs and PyAV decode with no header,
  so they do not. A gain of 0 gives the same audio in each reader.
- From ADR-HD8Z: the user prefers Opus; Opus is royalty-free; `foxglove.CompressedAudio` is the only
  open-source schema found that defines Opus, and it has no rate, channel or pre-skip fields, so the
  format copies `OpusHead`.
- From ADR-QDZ7: Opus is under 0.5 % of a take, so the bitrate is for clean onsets of sync clicks.
  With no `description`, Chrome 134 places decoded clicks on the exact sample. With `OpusHead` as
  `description`, Chrome drops the pre-skip but does not move the timestamps (6.5 ms early). PyAV
  19.0.2 does not apply the pre-skip either.

## Consequences

- Opus is lossy. libopus adds an encoder delay (pre-skip of 312 samples at 48 kHz in PyAV 19.0.2).
- A viewer that reads only the message fields can use a wrong rate (the mrkbac/lichtblick PR #116
  panel falls back to 16000 Hz mono).

## Evidence

- skellycam `dom/research` (local commits, not pushed), under `research/skellycam_recording/`:
  - `docs/spec_v1_review_20261113.md` (S6, S7) and the answers of the user in it;
  - `docs/mcap_check_20261113.md`: royalty status, schema fields, encoder delays, PR #116;
  - `recording_upgrade/results/mcap_electron/FINDINGS.md` task 3;
  - `recording_upgrade/results/mcap_kill/FINDINGS.md`;
  - `docs/mcap_profile_decisions_20261113.md` (Q8, Q14).

## Alternatives rejected

- `log_time` = `timestamp` for audio (as in the desk tests): camera and audio files would use
  `log_time` differently.
- `sample_rate` as the `OpusHead` input rate, with readers that apply the output gain.
- Give the `OpusHead` to WebCodecs as `description`: timestamps 6.5 ms early.
- FLAC in a custom schema; `pcm-s16` in `foxglove.RawAudio`; AAC-LC (royalties); G.711 and G.726
  (telephone quality); Opus in `foxglove.RawAudio` (defined for PCM and G.711 only).

## Open work

[open-work.md](../open-work.md)
