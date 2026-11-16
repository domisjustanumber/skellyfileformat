# 92TM — Audio: Opus in fragmented MP4 with 1 s fragments, and one CSV timing sidecar

**Status:** accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16).

## Decision

1. **Codec and container.** The microphone audio is Opus (RFC 6716) in a fragmented MP4 file,
   `synchronized_videos/<rec>.audio.m4a`, written live. FLAC, WAV and the MCAP audio messages are
   not written. The file plays in standard players. Exact sync is judged in the skellycam player; a
   small offset in VLC is accepted.
2. **Encoder.** libopus, through PyAV, with the version that the exact `av` pin gives. A release
   check makes sure that the Opus encoder is libopus. The FFmpeg native Opus encoder is not used.
3. **Encoder settings.** The channels of the microphone device, at most 2; a writer downmixes a
   device with more. 48 kHz. 20 ms packets (960 samples). Application `audio`. VBR at 128 kbit/s
   for mono and 256 kbit/s for stereo, complexity 10. Output gain 0. The standard Opus pre-skip.
4. **Fragments.** The movie header is empty (`empty_moov`), each fragment uses
   `default_base_moof`, a fragment holds 1 s of audio, and the writer flushes each packet. A crash
   loses less than 1 s of audio (16 process kills: 54 to 991 ms; 0 torn bytes).
5. **One CSV timing sidecar**, `<rec>.audio.csv`. It holds the host time of the audio callbacks and
   the sample counts, and, at a clean end, the drift fit:
   t = t0 + (n − n0) × 10^9 / f_eff. The microphone name is in the info JSON `audio` block, not in
   the CSV.
6. **Gaps.** When the device drops samples, the writer inserts that number of samples of silence
   and flags the row in the CSV. So the sample index of the file is the device time.
7. **Reader timing (normative).** A reader maps an audio sample to take time only through the CSV
   fit, never through the start time and the nominal rate. It applies each sample offset that the
   CSV states.
8. **Crashed audio, reader rules.** The usable length is the smaller of the cover of the CSV rows
   and the length of the audio indexed in the file. A reader ignores an index entry whose bytes go
   past the end of the file. When the CSV has no fit footer, the reader fits the rows.
9. **Clean-up of a crashed file.** Cut the file after the last complete fragment (a `moof` and its
   `mdat`). Remove a zero-filled tail only when the box walk finds an incomplete box. Write the fit
   and end lines of the CSV from its rows. Do not remux.
10. **Decoding.** A reader drops the pre-skip samples at the start of the stream. It does not apply
    an output gain. The player decodes with the WebCodecs `AudioDecoder`. The seek pre-roll (80 ms
    before the target) and the other player methods are informative guidance in the spec.
11. **Latency.** The optional, provisional `audio_latency_ns` is the time from the sound at the
    microphone to its ADC time. It is in the header of the audio CSV. It stays provisional until
    the microphone latency test.
12. **Lichtblick** is not a viewer of this format. Its audio checks are withdrawn.

This entry supersedes [ADR-D9N1](D9N1-opus-audio-settings-and-timing.md),
[ADR-WD9A](WD9A-lichtblick-reference-viewer.md) and [ADR-10JC](10JC-lichtblick-audio-checks.md) in
full. Item 3 restates D9N1 items 4 and 5. Item 10 restates D9N1 items 7, 8 and 10 and
[ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) item 10, with the pre-roll as guidance.
Item 11 restates [ADR-752H](752H-timing-fields.md) item 6 and
[ADR-5G42](5G42-gate1-names.md) item 3, with the CSV header in place of the channel metadata. Item 1
replaces D9N1 items 1, 2 and 9 and WD9A item 3. D9N1 items 3 and 6 (MCAP metadata and timestamps)
are withdrawn: the file holds the Opus header, and the CSV holds the timing. T24G item 11 is
withdrawn: a standard demuxer gives the packets. Item 12 withdraws WD9A items 1, 2 and 4 and all of
10JC. Items 2, 4 to 9 are new.

## Reason

- Size matters, and a loss of up to 1–2 s in a crash and a clean-up step are accepted. Opus with
  1 s fragments is about 54 MB/h mono and 108 MB/h stereo. WAV is 345.6 MB/h mono.
- With per-packet fragments, open time grows with the fragment count (VLC about 6.5 s per hour).
  1 s fragments open fast at any length.
- In the skellycam player harness, a crashed fMP4 Opus file seeks sample-exactly, and the CSV fit
  keeps audio in sync to within 0.24 ms over 59 minutes. Without the fit, the error reaches 36 ms.
- The MKA alternative needs a duration repair, and the planned player cannot index it.
- libopus is the reference encoder of the standard. It had releases in 2025-12 and 2026-01.

## Evidence

skellycam `dom/research`, `research/skellycam_recording/recording_upgrade/results/` (local, not
committed):
- `audio_single_file/opus_crash/FINDINGS.md`, §2, §3 and §7 (kills, seeks, repair, 1 s fragments,
  stereo);
- `audio_single_file/skellycam_playback/FINDINGS.md` (sync in the player harness);
- `audio_single_file/opus/FINDINGS.md` and `audio_single_file/FINDINGS.md` (WAV, FLAC, Opus);
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 5
  Q2, Q3; round 6; round 7 items 1, 2.

## Alternatives rejected

- WAV: no loss and no repair, but 6.4 times the size.
- FLAC: a 5-byte repair after each crash, and at most half the size of WAV.
- Opus with one fragment for each packet: the open time grows by about 6.5 s per hour in VLC.
- Opus in MKA: a duration repair after each crash, and the planned player cannot index it.
- Ogg Opus: VLC drops 80 ms.

## Open work

[open-work.md](../open-work.md)
