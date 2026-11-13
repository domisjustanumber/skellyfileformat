# HD8Z — Opus is the audio codec, in `foxglove.CompressedAudio` messages, with the OpusHead fields in the channel metadata

**Status:** accepted, 2026-11-13 (user).

## Decision

1. Opus (RFC 6716) is the audio codec of the format. FLAC is withdrawn.
2. An audio packet is one MCAP Message with the schema `foxglove.CompressedAudio` and
   `format: "opus"`. The `data` field holds one complete raw Opus packet, with no Ogg, WebM or other
   container framing. The audio is mono or stereo.
3. The `metadata` map of the audio MCAP Channel holds the fields of the Opus identification header
   (`OpusHead`, RFC 7845 section 5.1): the channel count, the pre-skip, the input sample rate and the
   output gain. It also holds the whole `OpusHead` as base64. The spec gives the keys.
4. A reader discards the pre-skip samples at the start of the stream.
5. After a seek, a reader decodes from 80 ms before the target and discards that audio (the Opus
   seek pre-roll that Matroska `A_OPUS` gives).
6. skellycam records the microphone to its own MCAP file. skellysync writes its audio as Opus in
   MCAP. The spec gives the file layout of each.
7. The player decodes the Opus packets with the WebCodecs `AudioDecoder`.

This entry supersedes [ADR-CA03](CA03-flac-audio.md) in full. Item 7 restates its item 4 for
Opus. Item 6 replaces its items 2 and 3. Item 1 replaces its item 1. ADR-CA03 item 1 said that a
change to Opus needs a new entry; this is that entry.

## Reason

- The user prefers Opus.
- Opus is royalty-free: Xiph.Org, Broadcom and Microsoft grant no-charge patent licences, and the
  reference code is BSD (https://opus-codec.org/license/). AAC-LC, the other general codec in
  `foxglove.CompressedAudio`, needs a paid patent licence for encoder and decoder products. G.726 is
  8 kHz telephone audio.
- `foxglove.CompressedAudio` is the only open-source message schema found that defines Opus. Its
  fields have no sample rate, channel count or pre-skip. Every Opus container (Ogg, Matroska,
  WebCodecs) carries these in the `OpusHead`, so the format copies `OpusHead`, not new names.
- WebCodecs decodes Opus. The Audio panel of mrkbac/lichtblick PR #116 plays it.

## Consequences

- Opus is lossy. libopus adds an encoder delay (pre-skip of 312 samples at 48 kHz in PyAV 19.0.2).
  A reader that does not apply the pre-skip puts the audio 6.5 ms late.
- `foxglove.CompressedAudio` has no sample-rate field. A viewer that reads only the message fields
  can use a wrong rate (the PR #116 panel falls back to 16000 Hz mono).
- The microphone writer of skellycam changes from FLAC to Opus. The FLAC kill-test result does not
  apply to the Opus writer.

## Evidence

- Royalty status, schema fields, the encoder delays in PyAV 19.0.2, the review of PR #116 and the
  survey of other Opus schemas: skellycam `dom/research`,
  `research/skellycam_recording/docs/mcap_check_20261113.md` (local commit, not pushed).

## Alternatives rejected

- FLAC in a custom schema: lossless, but no standard schema carries it.
- `pcm-s16` in `foxglove.RawAudio`: a standard schema and lossless, but the user prefers Opus.
- AAC-LC: patent royalties. G.711 and G.726: telephone quality.
- Opus in `foxglove.RawAudio`: the PR #116 panel would select it by itself, but `RawAudio` is
  defined for PCM and G.711 only.

## Open work

[open-work.md](../open-work.md)
