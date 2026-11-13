# skellyfileformat specification

Status: **draft v1 (MCAP profile), for review at gate 1** ([AGENTS.md section 4](../AGENTS.md#4-project-rules)).
No format version is released yet. Draft v0 (the MKV and sidecar design) was withdrawn before gate 1
([ADR-SFK5](../decisions/entries/SFK5-mcap-container.md)). Its IDs stay in this file, marked
withdrawn. A requirement marked `(provisional)` names the open item that it waits for
([open-work.md](../decisions/open-work.md)).

This specification is normative. The license of the spec text is CC-BY-4.0 ([LICENSE](LICENSE)).

## 1. Scope and terms

This spec describes one **recording** (one take): a set of synchronised MCAP files, one for each
device, that share one clock. The format is a profile of MCAP
([ADR-DK8S](../decisions/entries/DK8S-mcap-profile-files-and-names.md)). The spec gives the
channels, the schemas, the meaning of each field and metadata key, the clocks, the rules for
unfinished and repaired files, and how a reader opens a recording. Another program can implement
the format from this spec and the MCAP specification alone.

The spec does not describe these:

- recordings that older programs wrote, for example H.264 MP4 files, MKV files, timestamp CSV files
  and WAV audio (section 13 tells how a reader recognises a file that is not in this format);
- skellycam's recording info JSON, which is a skellycam file;
- the names of files and folders. The writer's own spec defines them;
- overlays. The format has none;
- the transport that a player uses to read the files;
- raw, lossless or Bayer video, and chunk compression. A later version can add them.

Terms:

| Term | Meaning |
|---|---|
| recording, take | The files of one synchronised capture. Their `freemocap.recording` metadata holds the same `take_uuid`. |
| camera file | An MCAP file of this format with one image channel (section 5). |
| audio file | An MCAP file of this format with one audio channel (section 6). |
| device file | A camera file or an audio file. |
| MCAP terms | Header, Footer, Schema, Channel, Message, Chunk, Message Index, Chunk Index, Metadata, Metadata Index, Statistics, Data End, Summary and Summary Offset have the meanings of the MCAP specification. |
| finished file | A device file that the writer closed normally: it has a Data End record, a Summary and a Footer (section 9). |
| unfinished file | A device file with no valid Footer at its end, for example after a crash (section 9). |
| repaired file | An unfinished file that a repair changed into a finished file (section 9). |
| writer | A program that writes files in this format. A writer with live capture is a **capture writer** (skellycam). A writer that writes from other files is a **conversion writer** (the skellycam converter, skellysync). |
| reader | A program that reads files in this format. A player is a reader. |
| host clock | The monotonic clock of the computer that recorded the take (section 7). |
| arrival time | The host-clock time at which the writer received a frame or an audio block. |
| sample time | The host-clock time that the capture driver or the source gives for a frame. |
| fitted time | The writer's estimate, on the host clock, of the regular frame lattice of a camera (section 7). It is not corrected for latency. |
| player time | The time that a reader uses to place a frame (section 7). |
| position | The place of a frame in its camera file: 0, 1, 2 and so on, in file order. It is the recording frame number. |
| sequence | The value of the MCAP Message `sequence` field. For a frame, the frame number that the camera or the source gives. For an audio packet, the packet index. |
| nominal rate | The requested or configured frame rate of a camera, as a rational number. |
| fit segment | A part of a camera file in which the fitted time is a straight line of the sequence (section 7). |
| breakpoint | A frame whose sequence is not the sequence of the frame before it plus 1 (section 7). |

## 2. Conventions

- The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have the meanings of RFC 2119 and
  RFC 8174, when they are in capital letters.
- A requirement starts on a new line with its ID in bold, for example `**SFF-008**`. The ID has
  three digits. A requirement has one ID. An ID is not reused or renumbered.
- Each section has a block of 50 IDs. Section 2 uses SFF-001 to SFF-049. Section N (N ≥ 3) uses the
  block that starts at (N − 2) × 50, for example section 5 uses SFF-150 to SFF-199. A new
  requirement gets the next free ID in the block of its section. The tests in
  [conformance.md](conformance.md) use the same blocks.
- A removed requirement keeps its line, with `(withdrawn)` after its ID. The withdrawn lines of a
  section come first in that section.
- A provisional requirement has `(provisional)` after its ID and names the open item that it waits
  for. A provisional requirement must be closed before v2.0.0.
- `(writer)` or `(reader)` after an ID tells which program the requirement applies to.
- Each requirement has one or more tests in [conformance.md](conformance.md).
  `tools/check_spec_traceability.py` checks this.
- ⌊a / b⌋ is integer division rounded down, for a ≥ 0 and b > 0.

**SFF-001** (withdrawn) Draft v0.

**SFF-002** (withdrawn) Draft v0.

**SFF-003** (withdrawn) Draft v0.

**SFF-004** (withdrawn) Draft v0.

**SFF-005** (withdrawn) Draft v0.

**SFF-006** (withdrawn) Draft v0.

**SFF-007** (withdrawn) Draft v0.

**SFF-008** (writer, reader) Each device file is an MCAP file as the MCAP specification defines it
(https://mcap.dev/spec), with the magic `0x89 M C A P 0x30 \r \n` at its start and, when finished,
at its end. A writer uses only the records, fields and rules of that specification.

**SFF-009** (writer, reader) Each value in a Metadata record and in a Channel `metadata` map is a
UTF-8 string. An integer value is written in decimal, with a `-` sign when it is negative, with no
`+` sign, no leading zeros (except the value `0`) and no spaces. A reader refuses a file whose
integer value has another form (reason `bad_metadata`).

**SFF-010** (writer, reader) A value that holds a list or an object is UTF-8 JSON (RFC 8259). In it,
each integer that can be outside the range −2^53 to 2^53 is a JSON string in the form of SFF-009.
Other integers are JSON numbers.

**SFF-011** (writer, reader) Each time is an integer number of nanoseconds on the host clock of the
take (section 7). An MCAP `log_time` or `publish_time` holds it as `uint64`. A protobuf
`google.protobuf.Timestamp` holds it as `seconds` × 10^9 + `nanos`, with `nanos` from 0 to
999,999,999.

**SFF-012** (reader) A JavaScript reader keeps each 64-bit integer exact (for example with
`BigInt`). It makes a JavaScript number from a time only after it subtracts the take start
(`take_start_host_ns`, section 15). It reports a difference with a magnitude of 2^53 or more as an
error, not as an inexact number.

**SFF-013** (writer, reader) The text form of a 16-byte UID (`take_uuid`) is 32 lowercase
hexadecimal characters, with no dashes.

## 3. Versioning

The rules of the README section [Versioning](../README.md#versioning-normative) apply
([ADR-7K3C](../decisions/entries/7K3C-format-versioning-in-metadata.md)).

**SFF-050** (withdrawn) Draft v0.

**SFF-051** (withdrawn) Draft v0.

**SFF-052** (withdrawn) Draft v0.

**SFF-053** (withdrawn) Draft v0.

**SFF-054** (withdrawn) Draft v0.

**SFF-055** (withdrawn) Draft v0.

**SFF-056** (withdrawn) Draft v0.

**SFF-057** (withdrawn) Draft v0.

**SFF-058** (withdrawn) Draft v0.

**SFF-059** (writer) Each device file has one Metadata record with the name `freemocap.format`. It has
the keys `major`, `minor` and `prerelease`. Each value is an integer from 0 to 65,535 (SFF-009).

**SFF-060** (reader) A reader MUST refuse a file with a `major` that it does not know (state
`unsupported_version`). It does not report the file as legacy.

**SFF-061** (reader) A reader MUST read a file with a higher `minor` of a `major` that it knows. It
ignores the Metadata records, metadata keys, channels, topics, schemas and Log names that it does
not know.

**SFF-062** (writer) A writer writes only the latest format version. Before v2.0.0 is released, a
writer writes `major` = 2, `minor` = 0 and `prerelease` = N, where N is the prerelease revision. A
released writer writes `prerelease` = 0.

**SFF-063** (reader) A reader MAY refuse a file with `prerelease` > 0.

**SFF-064** (writer, reader) The MCAP Header `library` holds the writer string, for example
`skellycam 2.1.3`. A reader MUST NOT change its behaviour because of it.

**SFF-065** (reader) The MCAP version in the magic is not the format version. A reader does not use
it as the format version.

**SFF-066** (reader) A reader uses a key or a rule only when the `minor` of the file is equal to or
higher than the minor version that added it. In version 2.0, every key and rule of this spec has
minor 0.

## 4. The MCAP profile

**SFF-100** (withdrawn) Draft v0.

**SFF-101** (withdrawn) Draft v0.

**SFF-102** (withdrawn) Draft v0.

**SFF-103** (withdrawn) Draft v0.

**SFF-104** (withdrawn) Draft v0.

**SFF-105** (withdrawn) Draft v0.

**SFF-106** (withdrawn) Draft v0.

**SFF-107** (withdrawn) Draft v0.

**SFF-108** (withdrawn) Draft v0.

**SFF-109** (withdrawn) Draft v0.

**SFF-110** (withdrawn) Draft v0.

**SFF-111** (withdrawn) Draft v0.

**SFF-112** (withdrawn) Draft v0.

**SFF-113** (withdrawn) Draft v0.

**SFF-114** (writer) A take has one camera file for each camera and at most one audio file.

**SFF-115** (writer) The MCAP Header `profile` is `freemocap`.

**SFF-116** (writer) Each Channel has `message_encoding` = `protobuf`. Each Schema has `encoding` =
`protobuf`, the name of one of the messages of the table below, and as `data` a serialised
`google.protobuf.FileDescriptorSet` that defines that message with these field numbers.

| Schema name | Fields used by this spec (name = field number: type) |
|---|---|
| `foxglove.CompressedImage` | `timestamp` = 1: `google.protobuf.Timestamp`; `data` = 2: bytes; `format` = 3: string; `frame_id` = 4: string |
| `foxglove.CompressedAudio` | `timestamp` = 1: `google.protobuf.Timestamp`; `data` = 2: bytes; `format` = 3: string |
| `foxglove.Log` | `timestamp` = 1: `google.protobuf.Timestamp`; `level` = 2: enum (`WARNING` = 3); `message` = 3: string; `name` = 4: string |

**SFF-117** (writer) A camera file has the channel `/cameras/<camera_label>/image` (schema
`foxglove.CompressedImage`) and MAY have the channel `/cameras/<camera_label>/log` (schema
`foxglove.Log`). An audio file has the channel `/microphones/<label>/audio` (schema
`foxglove.CompressedAudio`). A writer writes no other channel.

**SFF-118** (writer) Each Message is in a Chunk. Each Chunk holds the Messages of one channel only,
in the order that the writer wrote them. Each Chunk has `compression` = "" (none) and a non-zero
`uncompressed_crc`, and is followed by its Message Index records.

**SFF-119** (writer) Each Chunk of the image channel holds exactly `frames_per_chunk` Messages
(section 5), except that the last Chunk of that channel can hold fewer. A writer writes
`frames_per_chunk` = 1.

**SFF-120** (reader) A reader handles any `frames_per_chunk` of 1 or more. The image Chunks, in
order of their offset in the file, hold the positions in order. The frame at position p is in image
Chunk ⌊p / `frames_per_chunk`⌋, as Message p − ⌊p / `frames_per_chunk`⌋ × `frames_per_chunk` of that
Chunk.

**SFF-121** (writer) Each Chunk of the audio channel holds exactly 5 Messages, except that the last
Chunk of that channel can hold fewer.

**SFF-122** (writer) In one channel, the writer writes the Messages in order of position (image) or
of packet index (audio). The `log_time` of a Message is not less than the `log_time` of the Message
before it in the same channel.

**SFF-123** (writer) A writer writes the `freemocap.format` and `freemocap.recording` Metadata
records after the Header and before the first Chunk. It writes the `freemocap.timing` Metadata
record of a camera file after the last Chunk and before the Data End record.

**SFF-124** (writer) A writer writes no Attachment record.

## 5. Camera files

The `metadata` map of the image Channel holds these keys:

| Key | Value |
|---|---|
| `camera_label` | The label of the camera. The same label is in the topic. |
| `camera_key` | Optional. A stable key of the camera: an integer from 1 to 2^64 − 1. |
| `nominal_rate` | `<num>/<den>`: the nominal rate in frames per second, for example `30/1` |
| `display_rotation` | `0`, `90`, `180` or `270` |
| `frames_per_chunk` | An integer, 1 or more |
| `group_position` | Optional. The order of the camera in the take: an integer from 0 to 65,534. |

**SFF-150** (withdrawn) Draft v0.

**SFF-151** (withdrawn) Draft v0.

**SFF-152** (withdrawn) Draft v0.

**SFF-153** (withdrawn) Draft v0.

**SFF-154** (withdrawn) Draft v0.

**SFF-155** (withdrawn) Draft v0.

**SFF-156** (withdrawn) Draft v0.

**SFF-157** (withdrawn) Draft v0.

**SFF-158** (withdrawn) Draft v0.

**SFF-159** (withdrawn) Draft v0.

**SFF-160** (withdrawn) Draft v0.

**SFF-161** (withdrawn) Draft v0.

**SFF-162** (withdrawn) Draft v0.

**SFF-163** (withdrawn) Draft v0.

**SFF-164** (withdrawn) Draft v0.

**SFF-165** (withdrawn) Draft v0.

**SFF-166** (withdrawn) Draft v0.

**SFF-167** (withdrawn) Draft v0.

**SFF-168** (withdrawn) Draft v0.

**SFF-169** (withdrawn) Draft v0.

**SFF-170** (withdrawn) Draft v0.

**SFF-171** (withdrawn) Draft v0.

**SFF-172** (withdrawn) Draft v0.

**SFF-173** (withdrawn) Draft v0.

**SFF-174** (withdrawn) Draft v0.

**SFF-175** (withdrawn) Draft v0.

**SFF-176** (withdrawn) Draft v0.

**SFF-177** (withdrawn) Draft v0.

**SFF-178** (withdrawn) Draft v0.

**SFF-179** (withdrawn) Draft v0.

**SFF-180** (withdrawn) Draft v0.

**SFF-181** (writer) A writer writes the keys of the table of section 5 in the `metadata` map of the
image Channel.

**SFF-182** (writer) `camera_label` has 1 to 16 characters from the set `A`–`Z`, `a`–`z`, `0`–`9`,
`_` and `-`. The camera files of one take have different labels. A writer refuses to start a take
with two cameras that have the same label.

**SFF-183** (writer) A writer SHOULD write `camera_key`. Its value is the first 8 bytes, as a
little-endian unsigned 64-bit integer, of the SHA-256 of a UTF-8 identity string. For a USB camera
with a serial number, the string is `usb:<vid>:<pid>:<serial>`, with `<vid>` and `<pid>` as 4
lowercase hexadecimal digits and `<serial>` as the device reports it. For other cameras, the writer
defines the string, which starts with a kind name and a colon, for example `path:`. When the value
is 0, the writer writes no `camera_key`.

**SFF-184** (writer, reader) In `nominal_rate`, `<num>` and `<den>` are each an integer from 1 to
2^20. A reader refuses a file with another value (reason `bad_rate`).

**SFF-185** (writer) `display_rotation` is the clockwise rotation, in degrees, that a reader applies
to the stored pixels to show the frame upright. A writer stores each frame as the camera or the
source gave it, and it does not rotate the pixels
([ADR-68Z6](../decisions/entries/68Z6-rotation-in-metadata-only.md)).

**SFF-186** (reader) A reader that shows or processes frames applies `display_rotation`. A reader
refuses a value that is not 0, 90, 180 or 270 (reason `bad_rotation`).

**SFF-187** (writer) Each image Message holds a `foxglove.CompressedImage` with `format` = `jpeg`,
`frame_id` = the `camera_label`, and as `data` one complete JPEG image, from its SOI marker to its
EOI marker, as the camera or the encoder gave it.

**SFF-188** (writer) For each image Message: `log_time` is the arrival time of the frame;
`publish_time` is equal to `log_time`; `sequence` is the frame number that the camera or the source
gives, modulo 2^32; the `timestamp` field holds the sample time, and it is not set when the driver
gives no sample time ([ADR-752H](../decisions/entries/752H-timing-fields.md)).

**SFF-189** (reader) A reader uses the `timestamp` field as the sample time only when the field is
set. When it is not set, the frame has no sample time. A reader MUST NOT use an unset `timestamp` as
the time 0.

**SFF-190** (writer) When the JPEG encoder fails on a frame, the writer writes one `foxglove.Log`
Message on the log channel, with `level` = `WARNING`, `name` = `skellyfileformat.encode_skip`, and
as `log_time` and `timestamp` the arrival time of the frame that it did not write.

**SFF-191** (reader) A Log Message does not change the positions of the frames. A reader counts the
`skellyfileformat.encode_skip` Messages of each camera and reports the count (section 15).

**SFF-192** (writer, reader) A writer writes the `group_position` of a camera only when the user or
the writer gave the cameras an order. A reader orders the camera files of a take by
`group_position`, with unset values last, then by the bytes of `camera_label`.

## 6. Audio files

The `metadata` map of the audio Channel holds these keys
([ADR-HD8Z](../decisions/entries/HD8Z-opus-audio.md),
[ADR-QDZ7](../decisions/entries/QDZ7-opus-settings-and-timing.md)):

| Key | Value |
|---|---|
| `label` | The label of the microphone, with the rules of `camera_label`. The same label is in the topic. |
| `sample_rate` | `48000` |
| `channels` | `1` or `2` |
| `pre_skip` | The pre-skip of the Opus stream: the number of samples at 48 kHz that a reader drops at the start |
| `output_gain` | The output gain of the Opus header, as a signed Q7.8 integer (RFC 7845) |
| `opus_head` | The Opus identification header of RFC 7845 section 5.1, in base64 (RFC 4648 section 4, with padding) |
| `audio_latency_ns` | Optional (provisional). The time from the sound at the microphone to its ADC time, in nanoseconds |

**SFF-200** (withdrawn) Draft v0.

**SFF-201** (withdrawn) Draft v0.

**SFF-202** (withdrawn) Draft v0.

**SFF-203** (withdrawn) Draft v0.

**SFF-204** (withdrawn) Draft v0.

**SFF-205** (withdrawn) Draft v0.

**SFF-206** (withdrawn) Draft v0.

**SFF-207** (withdrawn) Draft v0.

**SFF-208** (withdrawn) Draft v0.

**SFF-209** (writer) A writer writes the keys of the table of section 6 in the `metadata` map of the
audio Channel. The `channels` and `pre_skip` values are equal to the channel count and the pre-skip
in `opus_head`, and the mapping family in `opus_head` is 0.

**SFF-210** (writer) A capture writer encodes the audio with Opus (RFC 6716) at 48 kHz, with the
channels of the microphone device and at most 2. It downmixes a device with more channels. It uses
the application `audio`, 20 ms packets, variable bit rate at 128,000 bit/s for one channel and
256,000 bit/s for two channels, and complexity 10.

**SFF-211** (writer) Each audio Message holds a `foxglove.CompressedAudio` with `format` = `opus` and
as `data` one complete raw Opus packet of 20 ms (960 samples at 48 kHz), with no Ogg, WebM or other
container framing.

**SFF-212** (writer) For each audio Message: `log_time` is the arrival time of the audio callback
block that completed the packet; `publish_time` is equal to `log_time`; `sequence` is the packet
index (0, 1, 2 and so on), modulo 2^32; the `timestamp` field holds the host-clock time of the first
decoded sample of the packet. The decoded samples include the encoder's priming samples, so packet 0
starts `pre_skip` samples before the first sample of the microphone.

**SFF-213** (provisional: audio clock drift test A4) A capture writer computes the `timestamp` of
each packet from a fit of the host-clock times of the callback blocks against the sample index. The
`timestamp` values of consecutive packets differ by 20 ms ± the drift of the microphone clock.

**SFF-214** (reader) A reader decodes the raw packets with no Opus header given to the decoder (in
WebCodecs: no `description`). It drops the first `pre_skip` decoded samples of the stream. Decoded
sample i of packet k, counted before the drop, is at the time `timestamp`(k) + ⌊i × 10^9 / 48000⌋.

**SFF-215** (reader) To start decoding at a packet k after a seek, a reader decodes from packet
k − 4 (80 ms before) with a new decoder state, and discards the audio before packet k.

**SFF-216** (provisional: microphone latency test A3) When `audio_latency_ns` (L) is present, the
sound in a sample happened at the time of that sample minus L. When it is absent, a reader uses 0.

**SFF-217** (reader) When `channels` or `pre_skip` is not equal to the value in `opus_head`, the
reader uses the value in `opus_head` and reports the warning `opus_head_mismatch`.

## 7. Clocks, times and the fit

The `clock_id` key of the `freemocap.recording` record names the host clock of the take:

| `clock_id` | Clock |
|---|---|
| 1 | Windows `QueryPerformanceCounter`, in nanoseconds (Python `time.perf_counter_ns`) |
| 2 | Linux `CLOCK_MONOTONIC`, in nanoseconds |
| 3 | macOS `mach_absolute_time` converted to nanoseconds with `mach_timebase_info` (`CLOCK_UPTIME_RAW`) |
| 128 | Synthetic timeline of a conversion writer (skellysync). Time 0 is the start of the output. |

The `freemocap.timing` Metadata record of a camera file holds these keys
([ADR-FF01](../decisions/entries/FF01-fit-and-breakpoints-in-metadata.md)):

| Key | Value |
|---|---|
| `fitter` | The name of the method that made the fit |
| `fitter_version` | The version of that method |
| `fitter_params` | A JSON object of its parameters |
| `segments` | A JSON array of fit segments, in order of `seq_first`. Each segment is an object with `seq_first`, `seq_last`, `t0_ns` and `period_ps`. |
| `breakpoints` | A JSON array of `[position, sequence]` pairs, in order of position |

Example:

```
fitter         = skellycam-lattice
fitter_version = 1.0.0
fitter_params  = {"outlier_reject_ms": 5}
segments       = [{"seq_first": 1000, "seq_last": 55012, "t0_ns": "81234567000", "period_ps": "33389000"}]
breakpoints    = [[0, 1000], [5, 1007]]
```

**SFF-250** (withdrawn) Draft v0.

**SFF-251** (withdrawn) Draft v0.

**SFF-252** (withdrawn) Draft v0.

**SFF-253** (withdrawn) Draft v0.

**SFF-254** (withdrawn) Draft v0.

**SFF-255** (withdrawn) Draft v0.

**SFF-256** (withdrawn) Draft v0.

**SFF-257** (withdrawn) Draft v0.

**SFF-258** (withdrawn) Draft v0.

**SFF-259** (withdrawn) Draft v0.

**SFF-260** (withdrawn) Draft v0.

**SFF-261** (withdrawn) Draft v0.

**SFF-262** (withdrawn) Draft v0.

**SFF-263** (withdrawn) Draft v0.

**SFF-264** (writer) All files of a take have the same `clock_id`, from the table of section 7. All
their times are on that clock.

**SFF-265** (provisional: Linux and macOS timing tests, T-S7 of the skellycam plan) The `clock_id`
values 2 and 3 are provisional.

**SFF-266** (writer) Before it finishes a camera file, a capture writer writes the
`freemocap.timing` record with the keys of the table of section 7. The fitting method is the
writer's choice. A conversion writer MAY write the record.

**SFF-267** (writer) In each segment, `seq_first` ≤ `seq_last`, and both are sequence values of
frames of the file. `t0_ns` is the fitted time of the frame with sequence `seq_first`. `period_ps` is
the fitted frame period in picoseconds, an integer greater than 0. The segments do not overlap, and a
segment does not span a wrap of the sequence past 2^32 − 1.

**SFF-268** (reader) The fitted time of a frame with sequence s in a segment is
`t0_ns` + ⌊(s − `seq_first`) × `period_ps` / 1000⌋, computed with integers.

**SFF-269** (writer) The first breakpoint is `[0, s0]`, where s0 is the sequence of position 0.
After it, each frame at position p > 0 whose sequence is not (sequence of position p − 1 + 1)
modulo 2^32 is a breakpoint `[p, sequence]`.

**SFF-270** (reader) The sequence of the frame at position p is (s_b + p − p_b) modulo 2^32, where
`[p_b, s_b]` is the last breakpoint with p_b ≤ p.

**SFF-271** (reader) The player time of each frame of a camera file is its fitted time, when the file
has a `freemocap.timing` record and each frame is in a segment. Otherwise it is the arrival time
(`log_time`), for every frame of the file. A reader does not mix the two in one file, and it reports
the warning `missing_fit` when it uses the arrival time.

**SFF-272** (writer) The player time never decreases from one position to the next in one file.

**SFF-273** (reader) A reader MUST NOT change its behaviour because of `fitter`, `fitter_version` or
`fitter_params`.

**SFF-274** (reader) The time zero of a take is `take_start_host_ns` (section 15). A reader shows no
frame of a camera at a time before the player time of position 0 of that camera.

## 8. skellysync files

skellysync writes this profile ([ADR-X1G6](../decisions/entries/X1G6-read-old-write-mcap.md)). The
provisional requirements of this section wait for the skellysync decisions D-Q, D-FPS, D-HDR,
D-DRIFT and D-AUDIO. SFF-307 is final.

**SFF-300** (withdrawn) Draft v0.

**SFF-301** (withdrawn) Draft v0.

**SFF-302** (withdrawn) Draft v0.

**SFF-303** (withdrawn) Draft v0.

**SFF-304** (withdrawn) Draft v0.

**SFF-305** (provisional: skellysync D-AUDIO) skellysync writes one camera file for each source video
and one audio file for the audio that it keeps, with the rules of sections 4 to 6.

**SFF-306** (provisional: skellysync D-FPS) skellysync writes `clock_id` 128. The `log_time` of a frame
is its slot time on the synthetic timeline. The `timestamp` is the source presentation time minus the
presentation time of the first source frame used. `sequence` is the index of the source frame.
skellysync writes no `freemocap.timing` record.

**SFF-307** (writer) skellysync does not rotate the pixels. It writes the source rotation as
`display_rotation`.

**SFF-308** (provisional: skellysync D-Q, D-HDR and D-DRIFT) skellysync writes a description of each
source (file base name, size and content hash, codec, bit depth, range and transfer, encoder and
quality, and the sync result) in a Metadata record that those decisions name.

**SFF-309** (provisional: skellysync D-FPS) skellysync writes `take_start_host_ns` = 0. It writes
`take_start_utc_ns` as the start of the source recording when it knows it, else as the time of the
conversion.

## 9. Finished, unfinished and repaired files

([ADR-S4FG](../decisions/entries/S4FG-writing-crash-and-repair.md))

**SFF-350** (withdrawn) Draft v0.

**SFF-351** (withdrawn) Draft v0.

**SFF-352** (withdrawn) Draft v0.

**SFF-353** (withdrawn) Draft v0.

**SFF-354** (withdrawn) Draft v0.

**SFF-355** (withdrawn) Draft v0.

**SFF-356** (withdrawn) Draft v0.

**SFF-357** (withdrawn) Draft v0.

**SFF-358** (withdrawn) Draft v0.

**SFF-359** (withdrawn) Draft v0.

**SFF-360** (withdrawn) Draft v0.

**SFF-361** (withdrawn) Draft v0.

**SFF-362** (withdrawn) Draft v0.

**SFF-363** (withdrawn) Draft v0.

**SFF-364** (withdrawn) Draft v0.

**SFF-365** (withdrawn) Draft v0.

**SFF-366** (withdrawn) Draft v0.

**SFF-367** (withdrawn) Draft v0.

**SFF-368** (withdrawn) Draft v0.

**SFF-369** (writer) A writer finishes a device file with a Data End record, a Summary and a Footer.
The Summary holds the Schema, Channel, Statistics, Chunk Index and Metadata Index records, and a
Summary Offset section follows it. The Data End record holds the CRC of the data section.

**SFF-370** (provisional: fsync cost test) While it records, a capture writer forces the file data to
the disk at least once each second.

**SFF-371** (reader) A device file is unfinished when its last 8 bytes are not the MCAP magic, or when
its Footer does not point to a valid Summary. A reader opens an unfinished file without its Summary:
it reads the records from the start of the file in order. It uses each complete Chunk whose
`uncompressed_crc` is correct.

**SFF-372** (reader) A reader of an unfinished file stops at the first record that is not complete.
It reports the number of bytes after the last complete record (`torn_bytes`). When a Chunk is
complete but its CRC is wrong, the reader stops before that Chunk and reports the state `damaged`.
A reader checks that its read reached the last complete record. A stop with no error before that
record is a reader fault.

**SFF-373** (reader) In an unfinished file, a reader takes the `freemocap.format` and
`freemocap.recording` records from the data section (SFF-123). A file with no `freemocap.format`
record before its first Chunk is not in this format.

**SFF-374** (writer) A program MUST NOT repair a file without the agreement of the user for that
file. skellycam asks: "An incomplete recording was found. Would you like to repair it?"

**SFF-375** (writer) A repair cuts the file after the last complete Chunk that has a correct CRC, with
its complete Message Index records. Then it appends a `freemocap.timing` record (camera files), a
`freemocap.repair` Metadata record, a Data End record with a data section CRC of 0, a rebuilt Summary,
a Summary Offset section and a Footer. It never changes a byte before the cut. A repair that stops
before its end leaves an unfinished file, and a new repair starts again from the same cut.

**SFF-376** (writer) The `freemocap.repair` record has the keys `cut_bytes` (the number of bytes that
the repair removed) and `repair_writer` (the writer string of the program that repaired the file).

**SFF-377** (reader) A reader treats a repaired file as a finished file. It reports the state
`repaired` when the file has a `freemocap.repair` record. A data section CRC of 0 means "not
available" (MCAP).

## 10. Withdrawn section

Draft v0 section 10 (Segment UID and offsets) is withdrawn.

**SFF-400** (withdrawn) Draft v0.

**SFF-401** (withdrawn) Draft v0.

**SFF-402** (withdrawn) Draft v0.

**SFF-403** (withdrawn) Draft v0.

**SFF-404** (withdrawn) Draft v0.

**SFF-405** (withdrawn) Draft v0.

## 11. Withdrawn section

Draft v0 section 11 (unfinalised and crashed files) is withdrawn. Section 9 replaces it.

**SFF-450** (withdrawn) Draft v0.

**SFF-451** (withdrawn) Draft v0.

**SFF-452** (withdrawn) Draft v0.

**SFF-453** (withdrawn) Draft v0.

**SFF-454** (withdrawn) Draft v0.

**SFF-455** (withdrawn) Draft v0.

## 12. Withdrawn section

Draft v0 section 12 (file, attachment and MIME names) is withdrawn.

**SFF-500** (withdrawn) Draft v0.

**SFF-501** (withdrawn) Draft v0.

**SFF-502** (withdrawn) Draft v0.

**SFF-503** (withdrawn) Draft v0.

**SFF-504** (withdrawn) Draft v0.

## 13. Files that are not in this format

**SFF-550** (withdrawn) Draft v0.

**SFF-551** (withdrawn) Draft v0.

**SFF-552** (withdrawn) Draft v0.

**SFF-553** (withdrawn) Draft v0.

**SFF-554** (reader) A reader examines each regular file directly in the folder whose first 8 bytes
are the MCAP magic. It ignores the other files.

**SFF-555** (reader) An MCAP file is in this format when its Header `profile` is `freemocap` and it
has a `freemocap.format` record whose `major` the reader knows. A finished file has the record in its
Metadata Index. An unfinished file has it before its first Chunk (SFF-373).

**SFF-556** (reader) An MCAP file with another `profile`, or with no `freemocap.format` record, is not
in this format (state `not_in_format`). A file of this format with a `major` that the reader does not
know has the state `unsupported_version` (SFF-060).

**SFF-557** (reader) A folder with no file of this format holds a legacy recording, or none. This spec
does not tell how to read a legacy recording.

## 14. Withdrawn section

Draft v0 section 14 (skellysync camera sidecar header) is withdrawn. Section 8 replaces it.

**SFF-600** (withdrawn) Draft v0.

**SFF-601** (withdrawn) Draft v0.

**SFF-602** (withdrawn) Draft v0.

**SFF-603** (withdrawn) Draft v0.

## 15. The recording as a whole

The `freemocap.recording` Metadata record holds these keys
([ADR-TDB5](../decisions/entries/TDB5-whole-recording-no-manifest.md)):

| Key | Value |
|---|---|
| `take_uuid` | The ID of the take: a random UUID version 4, in the text form of SFF-013 |
| `take_start_host_ns` | The start of the take on the host clock |
| `take_start_utc_ns` | The start of the take in UTC, in nanoseconds since 1970-01-01T00:00:00Z |
| `utc_offset_min` | Local time minus UTC at the start of the take, in minutes |
| `clock_id` | The host clock (section 7) |
| `clock_freq_hz` | Optional. The frequency of the host clock counter, for diagnostics |
| `group_size` | The number of camera files of the take |

**SFF-650** (withdrawn) Draft v0.

**SFF-651** (withdrawn) Draft v0.

**SFF-652** (withdrawn) Draft v0.

**SFF-653** (withdrawn) Draft v0.

**SFF-654** (withdrawn) Draft v0.

**SFF-655** (withdrawn) Draft v0.

**SFF-656** (withdrawn) Draft v0.

**SFF-657** (withdrawn) Draft v0.

**SFF-658** (withdrawn) Draft v0.

**SFF-659** (withdrawn) Draft v0.

**SFF-660** (withdrawn) Draft v0.

**SFF-661** (withdrawn) Draft v0.

**SFF-662** (withdrawn) Draft v0.

**SFF-663** (withdrawn) Draft v0.

**SFF-664** (withdrawn) Draft v0.

**SFF-665** (withdrawn) Draft v0.

**SFF-666** (withdrawn) Draft v0.

**SFF-667** (withdrawn) Draft v0.

**SFF-668** (withdrawn) Draft v0.

**SFF-669** (writer) A writer writes the keys of the table of section 15 in the `freemocap.recording`
record of each device file. All files of a take have the same values.

**SFF-670** (writer) A capture writer reads `take_start_host_ns` and `take_start_utc_ns` one after the
other, with no other work between the two reads, before the first frame or sample of any file of the
take. `utc_offset_min` is the local offset at that moment. A writer MUST NOT write a time-zone name.

**SFF-671** (writer) `group_size` is the number of camera files of the take. The audio file is not
counted.

**SFF-672** (writer) No record of a file of this format holds an absolute path, a user name, the
friendly name of a device, a device path or a raw serial number.

**SFF-673** (writer) A writer puts the files of one take, and no other device files, directly in one
folder.

**SFF-674** (reader) A reader opens one folder. It looks only at the files directly in that folder.
It groups the files of this format by `take_uuid`, and it reports each take. It needs no other file to
open a take. An unfinished file belongs to the take of its `take_uuid`.

**SFF-675** (reader) When a take has fewer camera files than `group_size`, the reader reports the
take as `incomplete`, with the warning `incomplete_take`, and it opens the other files.

**SFF-676** (reader) When two camera files of one take have the same `camera_label`, the reader
reports the warning `duplicate_label` and keeps both files.

**SFF-677** (reader) When the files of one take disagree on a key of the `freemocap.recording` record,
the reader reports the warning `take_fact_mismatch` and uses the values of the first camera file in
the order of SFF-192.

### 15.1 The reader result

A reader can give the result of opening a folder as JSON. The conformance tests and the golden files
use this result to compare readers.

**SFF-678** (reader) The reader result is a JSON object with these members, serialised with the JSON
Canonicalization Scheme (RFC 8785):

- `result_version`: 1;
- `folder_state`: `ok` (one or more takes), `legacy` or `empty` (SFF-557);
- `takes`: an array, in order of `take_uuid`. Each take has `take_uuid`, `state` (`complete` or
  `incomplete`), `warnings` (an array of warning codes, sorted) and `files` (an array in the order of
  SFF-192, then the audio file);
- each item of `files`: `name` (the file name), `kind` (`camera` or `audio`), `state`, `reason` (a
  reason code or null), `label`, `torn_bytes`, `messages` (the number of image or audio Messages
  read), `encode_skips` (camera files), `fit` (true when the player time is the fitted time),
  `warnings` and, when the test asks for them, `records`;
- each item of `records`: `[position, sequence, log_time, sample_time or null, player_time]` for a
  camera file, and `[packet_index, log_time, timestamp]` for an audio file;
- `other_files`: an array of the files of SFF-554 that are not in this format, each with `name`,
  `state` and `reason`.

Each integer that can be outside the range −2^53 to 2^53 is a JSON string (SFF-010).

**SFF-679** (reader) The file states are `finished`, `repaired`, `unfinished`, `damaged`,
`unsupported_version` and `not_in_format`. When two states apply, the reader reports the first in
this order: `unsupported_version`, `damaged`, `unfinished`, `repaired`, `finished`.

**SFF-680** (reader) The reason codes are `bad_metadata`, `bad_rate`, `bad_rotation`, `bad_label`,
`bad_schema`, `missing_metadata` and `crc_mismatch`. The warning codes are `incomplete_take`,
`duplicate_label`, `take_fact_mismatch`, `missing_fit`, `encode_skip` and `opus_head_mismatch`. A
reader reports each reason and warning that this spec names, and no other.

## Appendix A. Golden files

Gate 2 makes these files. Each is committed with its SHA-256 sum and the script that made it, from
synthetic frames and pinned tools. The tests of [conformance.md](conformance.md) name them. Each
golden file has the reader result of SFF-678, with records, as a committed JSON file.

| # | Golden file | Sections |
|---|---|---|
| G1 | A finished take: 2 camera files of about 90 frames each at a small size, one with a dropped frame (a breakpoint) and a `freemocap.timing` record; and an audio file of 3 s, mono, with a click every 500 ms | 4, 5, 6, 7, 15 |
| G2 | G1 with a stereo audio file | 6 |
| G3 | A camera file with `frames_per_chunk` = 3 and a last Chunk of 2 frames | 4 |
| G4 | Unfinished camera and audio files: a clean cut at a record boundary; a torn tail of 37 bytes; a complete Chunk with a wrong CRC | 9 |
| G5 | G4 after repair, and G4 with an interrupted repair (a partial `freemocap.timing` record after the cut) | 9 |
| G6 | Version vectors: a higher `minor` with an unknown key, an unknown channel and an unknown Metadata record; an unknown `major`; `prerelease` > 0; two files that differ only in the Header `library` | 3 |
| G7 | Metadata error vectors: an integer with a leading zero; a `+` sign; a `nominal_rate` of 0/1 and of 2^20 + 1; a `display_rotation` of 45; a bad `camera_label`; a missing `freemocap.format` record; a `channels` value that disagrees with `opus_head` | 2, 5, 6 |
| G8 | Rotation vectors: `display_rotation` 0, 90, 180 and 270 with coloured corner markers and the expected upright corner colours | 5 |
| G9 | A camera file with an unset `timestamp` on every frame, and one with an encoder skip (a `skellyfileformat.encode_skip` Log Message) | 5 |
| G10 | Fit vectors: two segments, a sequence wrap at 2^32 − 1, a `period_ps` that gives a remainder, and a file with no `freemocap.timing` record | 7 |
| G11 | Recording folders: a finished take of 4 cameras and audio; a missing camera; a crashed take; two cameras with one label; two takes in one folder; files of one take that disagree on `clock_id` | 15 |
| G12 | Files not in this format: an MCAP file with the profile `ros2`; an MCAP file of profile `freemocap` with no `freemocap.format` record; an MJPEG MKV; a small H.264 MP4 | 13 |
| G13 | (provisional) A skellysync camera file and audio file | 8 |
