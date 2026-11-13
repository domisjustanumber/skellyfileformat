# QDZ7 — Opus encoder settings, packet timestamps and pre-skip handling

**Status:** superseded by [D9N1](D9N1-opus-audio-settings-and-timing.md), 2026-11-13 (commit to main; was accepted, 2026-11-13).

## Decision

1. **Encoder settings.**
   - Channels: those of the microphone device, at most 2. A writer downmixes a device with more.
   - 48 kHz, 20 ms packets (960 samples).
   - Application `audio` (not `voip`).
   - VBR at 128 kbit/s for mono and 256 kbit/s for stereo, complexity 10.
2. **Timestamps.** The `timestamp` of a packet (and the base of its `log_time`) is the host-clock
   time of its first decoded sample, with the encoder's priming samples included. So packet 0
   starts `pre_skip` samples before the first real sample.
3. **Decoding.** A reader decodes the raw packets with no Opus header given to the decoder (in
   WebCodecs: no `description`). The reader drops the first `pre_skip` decoded samples of the stream
   itself.

These items add to [ADR-HD8Z](HD8Z-opus-audio.md). They change none of its rules.

## Reason

- Size does not matter: Opus is under 0.5 % of a take. The bitrate is chosen for near-transparent
  audio and clean onsets of sync clicks. `voip` shapes the sound for speech.
- In Chrome 134, with no `description`, decoded clicks land on the exact sample against the packet
  timestamps. With the `OpusHead` as `description`, Chrome drops the pre-skip but does not move the
  timestamps, so the audio comes out 6.5 ms early, again after every configure.
- PyAV 19.0.2 does not apply the pre-skip either, so every reader drops it the same way.

## Evidence

- skellycam `dom/research` (local commits, not pushed):
  - `research/skellycam_recording/recording_upgrade/results/mcap_electron/FINDINGS.md` task 3;
  - `research/skellycam_recording/recording_upgrade/results/mcap_kill/FINDINGS.md`;
  - `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md` (Q8, Q14).

## Alternatives rejected

- Give the `OpusHead` to WebCodecs as `description`: timestamps 6.5 ms early.

## Open work

[open-work.md](../open-work.md)
