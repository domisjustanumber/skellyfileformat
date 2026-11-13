# 752H — Timing fields: arrival in `log_time`, sample time in `timestamp`; no legacy time; encoder skips as log messages

**Status:** accepted, 2026-11-13 (user).

## Decision

1. **Video.** For each frame:
   - `log_time` is the arrival time on the host clock;
   - `publish_time` is equal to `log_time`;
   - the `timestamp` field of `foxglove.CompressedImage` is the sample time that the capture driver
     gives, on the host clock. It is unset when the driver gives none;
   - `sequence` is the frame number of the camera or the source, modulo 2^32.
2. **Audio.** For each Opus packet:
   - `log_time` is the arrival time of the callback block on the host clock;
   - `publish_time` is equal to `log_time`;
   - the `timestamp` field of `foxglove.CompressedAudio` is the host-clock time of the first decoded
     sample of the packet ([ADR-QDZ7](QDZ7-opus-settings-and-timing.md));
   - `sequence` is the packet index.
3. All files of a take use one host clock. The `freemocap.recording` metadata names it with
   `clock_id`, with the values of spec v0 section 5.3.
4. There is no legacy time. A conversion writer writes an old per-frame timestamp as the arrival
   time.
5. There is no encoder-skip flag. When the JPEG encoder fails on a frame, the writer writes a
   `foxglove.Log` message on the camera's log topic, with level `WARNING`,
   `name` = `skellyfileformat.encode_skip` and the time of the frame. A gap in `sequence` shows
   that frames are missing; the log message tells why.
6. `audio_latency_ns` is the time from the sound at the microphone to its ADC time. The time of
   sample n is t0 + n × 10^9 / f − L, where L is `audio_latency_ns`. This item is provisional until
   the microphone latency test (A3 of the skellycam plan).
7. The nominal rate is a rational `num/den`. Each of `num` and `den` is an integer from 1 to 2^20.
   A reader refuses other values with the reason `bad_rate`.

## Reason

- Lichtblick and other MCAP tools place messages by `log_time`. With arrival in `log_time` for
  video and audio, both carry similar latencies.
- MCAP requires `publish_time` = `log_time` when no other time applies.
- A protobuf message field has presence, so "no sample time" is an unset field, not a magic value.
- The legacy time had no reader; the encoder-skip reason is rare and diagnostic.
- The bounds on the rate keep each period calculation inside 64-bit integers.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md`
  (Q3, Q5, Q6, Q9, Q11; local commit, not pushed).

## Alternatives rejected

- Sample time in `log_time`: the sample time is absent for some drivers, and tools would place
  frames by different times for different cameras.
- A per-frame companion schema for the legacy time and the encoder-skip flag: one more custom
  schema for data that no reader uses to place frames.

## Open work

[open-work.md](../open-work.md)
