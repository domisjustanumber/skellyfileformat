# skellyfileformat specification

Status: **draft v0, for review at gate 1** ([AGENTS.md section 4](../AGENTS.md#4-project-rules)).
No format version is released yet. A requirement marked `(provisional)` names the open item that it
waits for ([open-work.md](../decisions/open-work.md)).

This specification is normative. The license of the spec text is CC-BY-4.0 ([LICENSE](LICENSE)).

## 1. Scope and terms

This spec describes one **recording** (one take): a set of synchronised camera video files and
audio files that share one clock. It gives the byte layouts, the field meanings, the clocks, the
finalisation and recovery rules, and how a reader opens a recording. Another program can implement
the format from this spec alone.

The spec does not describe these:

- recordings that older programs wrote, for example H.264 MP4 files, timestamp CSV files and WAV
  audio (section 13 tells how to find them);
- skellycam's recording info JSON (`<rec>_info.json`), which is a skellycam file;
- overlays. The format has no overlay file and no overlay attachment;
- the transport that a player uses to read the files;
- Opus audio, lossless video and Bayer video.

Terms:

| Term | Meaning |
|---|---|
| recording, take | The files of one synchronised capture. All its sidecars hold the same `take_uuid`. |
| camera file | An MKV file with one JPEG video track (section 4). A skellysync camera file also has one FLAC track (section 8). |
| audio file | A skellycam `.mka` file with one FLAC track (section 6), or its live native `.flac` file before finalisation. |
| sidecar | A binary file that holds the timing and the byte index of one media file. The video timing sidecar has the magic `SKVT` (section 5). The audio timing sidecar has the magic `SKAT` (section 7). |
| embedded sidecar | A sidecar stored as a Matroska attachment at the end of its media file (section 9). |
| separate sidecar | A sidecar stored as its own file next to its media file. |
| live | The state of a file while the writer records it, or after a crash before recovery. |
| finalised | The state of a file after the finalisation steps of section 9. Its sidecar has the `finalised` header flag. |
| recovered | A live file that a recovery (section 11) changed into a finalised file. |
| writer | A program that writes files in this format. A writer with live capture is a **capture writer** (skellycam). A writer that writes from other files is a **conversion writer** (the skellycam converter, skellysync). |
| reader | A program that reads files in this format. A player is a reader. |
| host clock | The monotonic clock of the computer that recorded the take (section 5.3). |
| arrival time | The host-clock time at which the writer received a frame. |
| sample time | The time that the capture driver gives for a frame, on the host clock. |
| fitted time | The writer's estimate, on the host clock, of the regular frame lattice of a camera (section 5.5). It is not capture time. It does not include the camera latency. |
| player time | The time that a reader uses to place a frame (section 5.5). |
| `write_index` | The position of a frame in its camera file: 0, 1, 2 and so on. It is the recording frame number. |
| `source_frame_number` | The frame number that the camera or the source gives. A gap shows a dropped frame. |
| nominal rate | The frame rate, as a rational number, that the writer uses for the container timestamps. It is the requested or configured rate. |
| Segment UID | The 16-byte `SegmentUID` element in the Matroska `Info` element. |
| live offset | A byte offset that the writer recorded while it wrote the media file. |
| final offset | A byte offset into the final bytes of a finalised media file. |
| recording manifest | A JSON file that indexes the files and the facts of one recording (section 15.3). It is derived. The headers win. |

## 2. Conventions

- The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have the meanings of RFC 2119 and
  RFC 8174, when they are in capital letters.
- A requirement starts on a new line with its ID in bold, for example `**SFF-001**`. The ID has
  three digits. A requirement has one ID. An ID is not reused or renumbered.
- Each section has a block of 50 IDs. Section 2 uses SFF-001 to SFF-049. Section N (N ≥ 3) uses the
  block that starts at (N − 2) × 50, for example section 5 uses SFF-150 to SFF-199. A new
  requirement gets the next free ID in the block of its section. The tests in
  [conformance.md](conformance.md) use the same blocks.
- A removed requirement keeps its line, with `(withdrawn)` after its ID.
- A provisional requirement has `(provisional)` after its ID and names the open item that it waits
  for. A provisional requirement must be closed before v2.0.0.
- `(writer)` or `(reader)` after an ID tells which program the requirement applies to.
- Each requirement has one or more tests in [conformance.md](conformance.md).
  `tools/check_spec_traceability.py` checks this.

Binary conventions:

**SFF-001** (writer, reader) Each multi-byte integer and float in a sidecar is little-endian. `u8`,
`u16`, `u32` and `u64` are unsigned. `i16` and `i64` are two's complement. `f64` is IEEE 754
binary64.

**SFF-002** (writer, reader) CRC-32 is the CRC-32/ISO-HDLC (the zlib `crc32`: polynomial
0x04C11DB7 reflected, initial value 0xFFFFFFFF, final XOR 0xFFFFFFFF). A sidecar stores it as a
little-endian `u32`.

**SFF-003** (writer, reader) Each time is a signed 64-bit integer in nanoseconds. The value
INT64_MIN (−2^63) means "absent". A reader MUST NOT use an absent time as a number.

**SFF-004** (writer) `header_size`, `record_size` and `table_record_size` are multiples of 8. Each
section of a sidecar starts at an offset from the start of the sidecar that is a multiple of 8.

**SFF-005** (reader) A JavaScript reader reads each 64-bit integer as two unsigned 32-bit halves. It
does not use `BigInt`. For a time, it subtracts a recording base (for example `take_start_host_ns`)
before it makes a JavaScript number. A reader MUST NOT give an inexact value as exact: it reports an
offset or a time difference with a magnitude of 2^53 or more as an error. INT64_MIN stays "absent".

**SFF-006** (writer, reader) A text field of fixed size holds UTF-8 bytes, padded with zero bytes to
its size. The text has no zero byte.

**SFF-007** (writer, reader) The text form of a 16-byte UID (Segment UID or `take_uuid`) is 32
lowercase hexadecimal characters, with no dashes, in byte order.

## 3. Versioning

The rules of the README section [Versioning](../README.md#versioning-normative) apply. This section
tells how they apply to the bytes.

**SFF-050** (writer, reader) Each sidecar holds `major`, `minor` and `prerelease` as `u16` at the
offsets of section 5.1. These offsets do not change in any version.

**SFF-051** (reader) A reader MUST refuse a sidecar with a `major` that it does not know. It reports
"unsupported version". It does not report the file as legacy.

**SFF-052** (reader) A reader MUST read a sidecar with a higher `minor` of a `major` that it knows.
It reads the fields that it knows at their offsets. It skips the other bytes by `header_size`,
`record_size` and `table_record_size`.

**SFF-053** (writer) A writer writes only the latest format version. Before v2.0.0 is released, a
writer writes `major` = 2, `minor` = 0 and `prerelease` = N, where N is the prerelease revision. A
released writer writes `prerelease` = 0.

**SFF-054** (reader) A reader MAY refuse a sidecar with `prerelease` > 0.

**SFF-055** (writer, reader) Each sidecar holds a writer string, for example `skellycam 2.1.0`. A
reader MUST NOT change its behaviour because of the writer string.

**SFF-056** (writer, reader) A writer writes 0 to each reserved field and to each flag bit that this
spec does not define. A reader ignores reserved fields and the flag bits that it does not know.

**SFF-057** (writer, reader) A media file (MKV or MKA) has no version of its own. Its version is the
version of its sidecar.

## 4. Video: the MKV profile

A camera file is a Matroska file ([RFC 9559](https://www.rfc-editor.org/rfc/rfc9559)) with DocType
`matroska`.

**SFF-100** (writer) A camera file has exactly one video track, with CodecID `V_MJPEG`. A skellycam
camera file has no other track. A skellysync camera file also has exactly one FLAC track
(section 8).

**SFF-101** (writer) Each video frame is one JPEG image in one `SimpleBlock`. Each block has the
keyframe flag. No block is laced.

**SFF-102** (writer) A capture writer stores the JPEG bytes that an MJPEG camera sent, unchanged.
For a camera that sends raw frames, it encodes each frame to JPEG.

**SFF-103** (writer) A writer stores each frame in the orientation of the sensor. It does not rotate
the pixels. It does not write a container rotation element, for example `Projection` or
`ProjectionPoseRoll`. The rotation is in the sidecar (`display_rotation`, section 5.2).

**SFF-104** (writer) The container timestamp of the frame with `write_index` k is k ×
`nominal_rate_den` / `nominal_rate_num` seconds, rounded to the TimestampScale of the file. A writer
MUST NOT store measured times in the container timestamps.

**SFF-105** (writer) The first child of the Segment is a SeekHead, followed by a Void element. Before
finalisation, the SeekHead and the Void together have 23 or more unused bytes, so that the SeekHead
can take one more Seek entry (section 9.2).

**SFF-106** (writer) Before finalisation, a camera file has no Attachments element, and no Chapters
element after the first Cluster.

**SFF-107** (writer) The video track number is below 128.

**SFF-108** (reader) A reader MUST NOT require a JFIF or APP0 segment, a DHT segment or a fixed
marker order in a JPEG. It MUST accept bytes after the entropy-coded data. A frame is the bytes of
its block payload.

**SFF-109** (reader) A reader finds a block payload by parsing the block header: the track number as
an EBML variable-size integer, then 2 bytes of timestamp, then 1 byte of flags. It MUST NOT assume a
fixed header length.

**SFF-110** (writer) A skellycam capture writer writes no overlay and no burned-in text into the
frames.

## 5. Video timing sidecar

A video timing sidecar has a header, then one record for each frame, in `write_index` order. A
skellysync sidecar also has an audio packet table after the records (section 8).

### 5.1 Common header

All sidecars (`SKVT` and `SKAT`) start with these 160 bytes.

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 4 | `magic` | ASCII | `SKVT` (video) or `SKAT` (audio) |
| 4 | 2 | `major` | u16 | Format major version |
| 6 | 2 | `minor` | u16 | Format minor version |
| 8 | 2 | `prerelease` | u16 | 0 for a released format, N for the Nth prerelease revision |
| 10 | 2 | `clock_id` | u16 | The clock of all times in this sidecar (section 5.3) |
| 12 | 4 | `header_size` | u32 | Size of the header in bytes, with `header_crc32` |
| 16 | 4 | `record_size` | u32 | Size of each record in bytes |
| 20 | 4 | `header_flags` | u32 | Section 5.1.1 |
| 24 | 8 | `n_records` | u64 | Number of records. 0 in a live sidecar. |
| 32 | 16 | `segment_uid` | bytes | Segment UID of the media file. All zero when the media file has none (a live `.flac`). |
| 48 | 16 | `take_uuid` | bytes | The ID of the take. Random (UUID version 4). |
| 64 | 8 | `take_start_host_ns` | i64 | Start of the take on the host clock |
| 72 | 8 | `take_start_utc_ns` | i64 | Start of the take in UTC, in nanoseconds since 1970-01-01T00:00:00Z |
| 80 | 8 | `clock_freq_hz` | u64 | Frequency of the host clock counter, for diagnostics. 0 when not known. |
| 88 | 2 | `utc_offset_min` | i16 | Local time minus UTC at the start of the take, in minutes |
| 90 | 2 | `group_size` | u16 | Number of camera files in the take |
| 92 | 4 | `body_crc32` | u32 | CRC-32 of all bytes after the header. 0 in a live sidecar. |
| 96 | 8 | `table_offset` | u64 | Offset of the audio packet table from the start of the sidecar. 0 when there is no table. |
| 104 | 8 | `table_count` | u64 | Number of packet records in the table |
| 112 | 4 | `table_record_size` | u32 | Size of each packet record. 0 when there is no table. |
| 116 | 4 | `json_offset` | u32 | Offset of the diagnostics JSON block from the start of the sidecar. 0 when there is none. |
| 120 | 4 | `json_size` | u32 | Size of the JSON block in bytes |
| 124 | 4 | reserved | | 0 |
| 128 | 32 | `writer` | text | Writer string, for example `skellycam 2.0.0` |

The kind-specific fields start at offset 160 (section 5.2 and section 7.1). The last 4 bytes of the
header (at offset `header_size` − 4) are `header_crc32`.

**SFF-150** (writer) A writer writes the common header fields at the offsets and with the types of
the table in section 5.1.

**SFF-151** (writer) `header_crc32` is the CRC-32 of the header bytes from offset 0 to offset
`header_size` − 5. A writer that changes a header field recomputes it.

**SFF-152** (reader) A reader checks `magic`, then `major` (SFF-051), then `header_crc32`. It
refuses a header with a wrong `header_crc32`.

**SFF-153** (writer) The diagnostics JSON block, when present, is UTF-8 JSON inside the header, after
the fixed fields and before `header_crc32`. It holds facts for diagnostics only, for example the
encoder name, `async_depth`, the camera control values and the audio host API.

**SFF-154** (reader) A reader MUST NOT need the diagnostics JSON block to read, play or recover a
file.

#### 5.1.1 Header flags

| Bit | Name | Meaning |
|---|---|---|
| 0 | `finalised` | The writer completed finalisation steps 1 to 3 (section 9.1). The writer sets it last, before the embed. |
| 1 | `separate_final` | The appender refused this media file. The separate sidecar is the final form (SFF-354). |
| 2 | `recovered` | A recovery (section 11) made this sidecar. |
| 3 | `table_offsets_final` | The packet table offsets refer to the final media file. When 0, they refer to the live `.flac` file. |

**SFF-155** (writer) A writer sets `finalised` only after the record offsets, `n_records`,
`segment_uid`, the fitted times, the tables and `body_crc32` are final.

**SFF-156** (reader) A reader treats a sidecar without `finalised` as live (section 11).

**SFF-157** (writer) In a finalised sidecar, `body_crc32` is the CRC-32 of all bytes from offset
`header_size` to the end of the sidecar.

**SFF-158** (reader) A reader of a finalised sidecar SHOULD check `body_crc32`. When it matches, the
reader does not need to check each record CRC. When it does not match, the reader checks each record
CRC and reports the sidecar as damaged.

### 5.2 Video header fields

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 160 | 2 | `display_rotation` | u16 | 0, 90, 180 or 270 |
| 162 | 2 | `group_position` | u16 | Optional order of the camera in the take. 0xFFFF when not set. |
| 164 | 4 | `nominal_rate_num` | u32 | Nominal rate numerator (frames) |
| 168 | 4 | `nominal_rate_den` | u32 | Nominal rate denominator (seconds) |
| 172 | 4 | reserved | | 0 |
| 176 | 8 | `camera_key` | u64 | Stable camera key. 0 when not set. |
| 184 | 16 | `camera_label` | text | Short camera label |
| 200 | 64 | `audio` | struct | Audio track descriptor (section 7.2). All zero when the file has no audio track. |
| 264 | | | | End of the fixed video fields. In version 2.0, `header_size` ≥ 272. |

**SFF-159** (writer) `display_rotation` is the clockwise rotation, in degrees, that a reader applies
to the stored pixels to show the frame upright. Its value is 0, 90, 180 or 270.

**SFF-160** (reader) A reader that shows or processes frames applies `display_rotation`. A reader
refuses a value that is not 0, 90, 180 or 270.

**SFF-161** (writer) `camera_label` has 1 to 16 bytes from the set `A`–`Z`, `a`–`z`, `0`–`9`, `_`
and `-`. The camera files of one take have different labels. A writer refuses to start a take with
two cameras that have the same label.

**SFF-162** (writer) When a writer sets `camera_key`, it is the first 8 bytes, as a little-endian
`u64`, of the SHA-256 of a UTF-8 string that names the kind of identity and its value, for example
`usb:<vid>:<pid>:<serial>` or `path:<port path>`. A writer SHOULD set `camera_key`.

**SFF-163** (writer) `nominal_rate_num` and `nominal_rate_den` are both greater than 0.

### 5.3 Clocks

| `clock_id` | Clock |
|---|---|
| 1 | Windows `QueryPerformanceCounter`, in nanoseconds (Python `time.perf_counter_ns`) |
| 2 | Linux `CLOCK_MONOTONIC`, in nanoseconds |
| 3 | macOS `mach_absolute_time` / `CLOCK_UPTIME_RAW`, in nanoseconds |
| 0x80 | Synthetic aligned timeline of a conversion writer (skellysync). Time 0 is the start of the output. |

**SFF-164** (writer) A writer writes a `clock_id` from the table in section 5.3. All the sidecars of
one take have the same `clock_id`.

**SFF-165** (provisional: Linux and macOS timing tests, T-S7) The `clock_id` values 2 and 3 are
provisional until the Linux and macOS timing tests are done.

### 5.4 Video record

In version 2.0, `record_size` is 64. A later minor version can make records larger. Its new fields
then go after byte 59 and before `record_crc32`.

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 8 | `arrival_ns` | i64 | Arrival time (section 5.5) |
| 8 | 8 | `sample_time_ns` | i64 | Sample time, or absent |
| 16 | 8 | `legacy_ns` | i64 | A compatibility time that the writer defines, or absent |
| 24 | 8 | `fitted_ns` | i64 | Fitted time. Absent before finalisation. |
| 32 | 8 | `offset` | u64 | Offset of the first JPEG byte (the block payload) from the start of the media file |
| 40 | 4 | `size` | u32 | Size of the JPEG in bytes |
| 44 | 4 | `jpeg_crc32` | u32 | CRC-32 of the JPEG bytes |
| 48 | 4 | `source_frame_number` | u32 | Frame number from the camera or the source, modulo 2^32 |
| 52 | 4 | `write_index` | u32 | Position of the frame in the file |
| 56 | 4 | `flags` | u32 | Section 5.4.1 |
| `record_size` − 4 | 4 | `record_crc32` | u32 | CRC-32 of the record bytes from 0 to `record_size` − 5 |

**SFF-166** (writer) A writer writes each record with the fields of the table in section 5.4.
`record_size` is 64 or more.

**SFF-167** (writer) Record number k has `write_index` k. Its frame is the block with the container
timestamp of `write_index` k (SFF-104).

**SFF-168** (reader) A reader steps through the records by `record_size`. It finds `record_crc32`
in the last 4 bytes of each record.

**SFF-169** (writer) `jpeg_crc32` is the CRC-32 of the `size` bytes at `offset` in the media file.

#### 5.4.1 Record flags

| Bit | Name | Set when |
|---|---|---|
| 0 | `gap` | `source_frame_number` is not the previous `source_frame_number` + 1 (modulo 2^32). Frames were lost before the writer received them. |
| 1 | `repeat` | `source_frame_number` is equal to the previous `source_frame_number`. |
| 2 | `encode_skip` | The encoder failed on one or more frames before this frame. Those frames are not in the file. |
| 3 | reserved | Always 0 |
| 4 | `fit_valid` | `fitted_ns` holds a fitted time. |
| 5 | `fit_unreliable` | The fit of this part of the file has a large residual or is short. For information only. |
| 6–7 | `offset_state` | 0 = live offset; 1 = live offset found by a search of the file end; 2 = final offset; 3 = reserved |
| 8 | `recovered` | A recovery made this record (section 11). |

**SFF-170** (writer) A writer sets `gap` exactly when `source_frame_number` is not the previous value
+ 1 (modulo 2^32), and `repeat` exactly when it is equal to the previous value. It sets neither on
the first record.

**SFF-171** (writer) When the encoder fails on a frame, the writer sets `encode_skip` on the record
of the next frame that it writes.

**SFF-172** (writer) A writer sets `fit_valid` on all records of a file or on none.

**SFF-173** (writer) In a finalised sidecar, `offset_state` is 2 on each record.

### 5.5 Times and player time

| Writer kind | `arrival_ns` | `sample_time_ns` | `legacy_ns` | `fitted_ns` |
|---|---|---|---|---|
| Capture writer | Host-clock time when the writer received the frame | Capture-driver time on the host clock (for Media Foundation: sample time × 100), or absent | Writer-defined, or absent | Written at finalisation |
| Conversion writer from old timestamp files | The old per-frame timestamp, on its host clock | Absent | Writer-defined, or absent | Written at finalisation, or absent |
| skellysync (`clock_id` 0x80, provisional, section 14) | Slot time on the synthetic timeline | Source presentation time of the frame | Absent | Absent |

**SFF-174** (writer) A writer fills the time fields as the table in section 5.5 gives for its kind.

**SFF-175** (writer) The fitted time is the writer's estimate of the frame lattice on the host clock,
from the arrival times and the sample times. At finalisation, a writer that writes fitted times
writes `fitted_ns` for every frame and sets `fit_valid` on every record. Where the camera stalled
or stepped, it fits each part separately.

**SFF-176** (reader) The player time of a frame is `fitted_ns` when the sidecar is finalised and
every record has `fit_valid`. Otherwise it is `arrival_ns`, for every frame of the file.

**SFF-177** (writer) The player time never decreases from one record to the next in one file.

**SFF-178** (reader) A reader does not use `legacy_ns` to place frames.

## 6. Audio: FLAC in `.mka` (skellycam)

While the writer records, a skellycam audio file is a native FLAC file
([RFC 9639](https://www.rfc-editor.org/rfc/rfc9639)). At finalisation, the writer stream-copies its
FLAC frames into a Matroska file with DocType `matroska` (the `.mka` file).

**SFF-200** (writer) The final audio file has exactly one track, with CodecID `A_FLAC`. Its
CodecPrivate starts with `fLaC`, followed by the FLAC metadata blocks. The first metadata block is
STREAMINFO.

**SFF-201** (writer) Each FLAC frame is one `SimpleBlock`. No block is laced. The FLAC frames in the
`.mka` are byte-identical to the frames of the live `.flac` file.

**SFF-202** (writer) While it records, the writer writes each FLAC frame whole and flushes it to the
file before it writes the packet record of that frame (section 7.4).

**SFF-203** (reader) A reader MUST NOT use the STREAMINFO total sample count. It is 0 after a crash,
and the stream copy keeps that value. The reader uses `total_samples` of the sidecar and the packet
table.

**SFF-204** (writer) A writer deletes the live `.flac` file only after the `.mka` verifies: the
CRC-32 of each FLAC frame in the `.mka` matches its packet record, and the decoded sample count of
the `.mka` is `total_samples`.

**SFF-205** (writer) The audio file and the camera files of one take use the same host clock.

## 7. Audio timing sidecar (`.skat`) and the packet table

An audio timing sidecar has the common header (section 5.1) with magic `SKAT`, then audio records.
All audio records have `record_size` bytes, a `type` field at offset 40 and `record_crc32` in the
last 4 bytes. In version 2.0, `record_size` is 48.

- The **live** audio sidecar (`<stem>.skat.live`, section 12) holds timing records and packet
  records in the order that the writer wrote them.
- The **final** audio sidecar holds `n_records` timing records, then the packet table at
  `table_offset` (`table_count` packet records), then the drift table (section 7.5).

### 7.1 Audio header fields

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 160 | 64 | `audio` | struct | Audio track descriptor (section 7.2) |
| 224 | 8 | `audio_latency_ns` | i64 | Time from the sound at the microphone to its ADC time, or absent (provisional) |
| 232 | 8 | `drift_table_offset` | u64 | Offset of the drift table from the start of the sidecar. 0 when there is none (provisional). |
| 240 | 4 | `drift_count` | u32 | Number of drift records (provisional) |
| 244 | 4 | reserved | | 0 |
| 248 | | | | End of the fixed audio fields. In version 2.0, `header_size` ≥ 256. |

**SFF-250** (writer) A writer writes the audio header fields at the offsets of the table in
section 7.1. In a final audio sidecar, `table_record_size` is equal to `record_size`.

**SFF-251** (provisional: audio latency test A3) `audio_latency_ns` comes from a latency measurement
of the microphone. Until that test is done, a writer writes INT64_MIN.

### 7.2 Audio track descriptor

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| +0 | 2 | `track_number` | u16 | Matroska TrackNumber of the FLAC track. 0 = no audio track. |
| +2 | 2 | `channels` | u16 | Number of channels |
| +4 | 2 | `bits_per_sample` | u16 | Bits per sample |
| +6 | 2 | reserved | | 0 |
| +8 | 4 | `sample_rate` | u32 | Samples per second |
| +12 | 4 | reserved | | 0 |
| +16 | 8 | `total_samples` | u64 | Total samples for each channel. 0 in a live sidecar. |
| +24 | 34 | `flac_streaminfo` | bytes | The 34-byte body of the FLAC STREAMINFO block |
| +58 | 6 | reserved | | 0 |

**SFF-252** (writer) A writer writes the audio track descriptor with the fields of the table in
section 7.2. In a finalised sidecar, `total_samples` is the sum of `n_samples` of the packet table.

**SFF-253** (reader) A reader that decodes with the WebCodecs `AudioDecoder` uses the codec `flac`
and this 42-byte description: `fLaC`, then the 4 bytes `0x80 0x00 0x00 0x22`, then
`flac_streaminfo`.

### 7.3 Timing record (type 1)

The writer writes one timing record for each audio callback block, before it encodes the block.

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 8 | `sample_index` | i64 | Index of the first sample of the block |
| 8 | 8 | `host_ns` | i64 | Host-clock time at the start of the callback |
| 16 | 8 | `adc_ns` | i64 | ADC time of the block on the host clock, or absent |
| 24 | 8 | `current_ns` | i64 | Current time that the audio API gives, on the host clock, or absent |
| 32 | 4 | `block_index` | u32 | Index of the block |
| 36 | 4 | `frames` | u32 | Samples in the block for each channel |
| 40 | 2 | `type` | u16 | 1 |
| 42 | 2 | `flags` | u16 | Bit 0 input overflow; bit 1 input underflow; bit 2 silence inserted for a lost block; bit 3 priming |
| 44 | 4 | `record_crc32` | u32 | CRC-32 of bytes 0 to 43 (version 2.0) |

**SFF-254** (writer) A writer writes timing records with the fields of the table in section 7.3, in
`block_index` order, with no gap in `block_index`.

**SFF-255** (writer) When the audio API gives no usable ADC time (for example 0), the writer writes
`adc_ns` as INT64_MIN.

### 7.4 Packet record (type 2)

The writer writes one packet record for each FLAC frame, after the frame is in the file.

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 8 | `offset` | u64 | Offset of the FLAC frame from the start of the media file |
| 8 | 8 | `first_sample` | i64 | Index of the first sample of the frame |
| 16 | 4 | `size` | u32 | Size of the FLAC frame in bytes |
| 20 | 4 | `n_samples` | u32 | Samples in the frame for each channel |
| 24 | 4 | `frame_crc32` | u32 | CRC-32 of the FLAC frame bytes |
| 28 | 12 | reserved | | 0 |
| 40 | 2 | `type` | u16 | 2 |
| 42 | 2 | reserved | | 0 |
| 44 | 4 | `record_crc32` | u32 | CRC-32 of bytes 0 to 43 (version 2.0) |

**SFF-256** (writer) A writer writes packet records with the fields of the table in section 7.4. It
writes no packet record with `size` = 0. The first `first_sample` is 0. Each next `first_sample` is
the previous `first_sample` + `n_samples`.

**SFF-257** (writer) For each audio block, the writer writes in this order: the timing record, then
the FLAC frame or frames, then their packet records. It flushes each record to the file when it
writes it.

**SFF-258** (writer) In a final audio sidecar, the packet offsets refer to the `.mka` file, and the
writer sets `table_offsets_final`. In a live audio sidecar, they refer to the `.flac` file.

**SFF-259** (reader) A reader finds the bytes of audio sample n by a binary search of the packet
table on `first_sample`.

### 7.5 Drift table and the audio-to-video mapping (provisional)

| Offset | Size | Field | Type | Meaning |
|---|---|---|---|---|
| 0 | 8 | `first_sample` | i64 | n0: the first sample of the segment |
| 8 | 8 | `t0_ns` | i64 | Host-clock time of sample n0 |
| 16 | 8 | `rate_hz` | f64 | f_eff: the measured sample rate of the segment on the host clock |
| 24 | 8 | `residual_p99_ns` | i64 | 99th percentile of the fit residual |
| 32 | 8 | `end_sample` | i64 | The first sample after the segment |
| 40 | 2 | `type` | u16 | 3 |
| 42 | 2 | `flags` | u16 | Bit 0 `fit_unreliable` |
| 44 | 4 | `record_crc32` | u32 | CRC-32 of bytes 0 to 43 (version 2.0) |

**SFF-260** (provisional: audio clock drift test A4) At finalisation, a writer writes one drift record
for each segment of a piecewise-linear fit of the ADC times against the sample index. The writer
starts a new segment at a residual jump of more than about 3 ms. It sets `fit_unreliable` when
`residual_p99_ns` is more than 5 ms or the segment is shorter than 10 s.

**SFF-261** (provisional: audio clock drift test A4 and audio latency test A3) The host-clock time of
sample n in a segment is t0_ns + (n − n0) × 10^9 / f_eff. The sample at host-clock time T is
n0 + (T − t0_ns − `audio_latency_ns`) × f_eff / 10^9, rounded down. When `audio_latency_ns` is
absent, the reader uses 0.

## 8. Audio in the camera MKV (skellysync)

**SFF-300** (writer) A skellysync camera file has one FLAC track. The writer writes the audio in the
same pass as the video. The FLAC track keeps the source sample rate and the source channels, at
16 bits per sample.

**SFF-301** (writer) The audio of frame k is the samples from round(k × `sample_rate` ×
`nominal_rate_den` / `nominal_rate_num`) to the audio start of frame k + 1, minus one sample. The
audio does not continue after the end of the last frame.

**SFF-302** (writer) The sidecar of a skellysync camera file holds the audio track descriptor
(section 7.2) and an audio packet table at `table_offset`, after the video records. The packet
records have the layout of section 7.4. In version 2.0, `table_record_size` is 48. The writer sets
`table_offsets_final`.

**SFF-303** (writer) A skellysync writer writes no live offsets. It writes the sidecar after the
media file is complete, with final offsets from a scan (section 10).

## 9. Embedding and finalisation

### 9.1 Finalisation order

**SFF-350** (writer) A writer finalises each media file in this order:

1. When recovery or an audio step needs it, remux the file.
2. Scan the final media file (section 10). Rebuild each offset, and check each frame CRC.
3. Write into the sidecar: the fitted times and the flags (`offset_state` = 2), `n_records`, the
   tables, `total_samples` and the final `segment_uid`. Then recompute each record CRC, then
   `body_crc32`. Set `finalised` last, then recompute `header_crc32`.
4. Embed the sidecar (section 9.2).
5. Verify the embed (section 9.3).
6. Delete the separate sidecar. For an audio file, also delete the `.flac` file (SFF-204) and the
   live audio sidecar.

**SFF-351** (writer) The writer writes the recording manifest (section 15.3) after step 6 of every
file of the take.

### 9.2 Appender

**SFF-352** (writer) The appender embeds a sidecar in this order:

1. Append an `Attachments` element with one `AttachedFile` (`FileName`, `FileMediaType`, `FileUID`,
   `FileData`) at the end of the file. `FileUID` is 8 random bytes and is not 0. Flush the file to
   the disk.
2. Rewrite the Segment size in place, with the same size width. Flush the file to the disk.
3. Rewrite the SeekHead with one more Seek entry for the Attachments, inside the old SeekHead and
   Void span. Keep a CRC-32 element if there was one. When exactly 1 byte remains, make the SeekHead
   size field 1 byte wider. Otherwise, fill the rest with a Void. Flush the file to the disk.

**SFF-353** (writer) The appender refuses, and changes nothing, when: the Segment has an unknown
size; the Segment does not end at the end of the file; the first child of the Segment is not a
SeekHead; the file already has an Attachments element; or the SeekHead and Void span has no room for
one more Seek entry.

**SFF-354** (writer) A writer embeds each sidecar when the appender does not refuse. When the
appender refuses, the writer sets `separate_final` in the separate sidecar and keeps it as the final
form.

**SFF-355** (writer) The appender changes only the Segment size, the bytes of the SeekHead and Void
span, and the bytes after the old end of the file. It does not move a frame.

**SFF-356** (writer) A writer MUST NOT use a tool that writes the Attachments before the Clusters,
for example `ffmpeg -attach`.

### 9.3 Verify and delete

**SFF-357** (writer) The embed verifies when all of these are true: the SHA-256 of the embedded
`FileData` is equal to the SHA-256 of the separate sidecar; the locator (section 9.4) finds the
attachment; and the CRC-32 of the first frame and of the last frame are equal to their records.

**SFF-358** (writer) A writer deletes a separate sidecar only after its embed verifies. When the
embed does not verify, the writer keeps the separate sidecar.

### 9.4 Locator

**SFF-359** (reader) A reader finds an embedded sidecar from the start of the file. It reads the EBML
header, the Segment header, the SeekHead and the Info (for `SegmentUID`), then the Attachments
element at the position that the SeekHead gives, then the `FileData`. It does not read the Clusters.

**SFF-360** (reader) The locator matches an `AttachedFile` by its `FileName` and its
`FileMediaType` (section 12). It reports these failures: not EBML; no Segment; no SeekHead; no
Attachments entry; Attachments past the end of the file; a SeekHead entry that does not point to an
Attachments element; `FileData` with an unknown size; short `FileData`; no matching `AttachedFile`.

### 9.5 Which sidecar to use

**SFF-361** (reader) A reader uses the embedded sidecar when its `segment_uid` is equal to the
Segment UID of the media file. Otherwise, it uses a separate sidecar whose `segment_uid` is equal.
Otherwise, it can index the file by a scan (SFF-553), and the frames then have no times.

### 9.6 Interrupted embed

**SFF-362** (reader) When bytes follow the end of the Segment, or when the Segment ends with an
Attachments element that the SeekHead does not reference, the file is not embedded. A reader uses
the separate sidecar.

**SFF-363** (writer) To recover an interrupted embed, a writer cuts the file at the old end of the
Segment (the start of the unreferenced Attachments element, or the end of the Segment), restores the
Segment size, and embeds again from the separate sidecar.

**SFF-364** (reader, writer) A separate sidecar without `finalised` shows that finalisation did not
complete. A reader and a writer treat the file as live (section 11).

## 10. Segment UID, live offsets and final offsets

**SFF-400** (writer) `segment_uid` in a sidecar is the Segment UID of the media file whose bytes the
offsets refer to. After a remux, the writer writes the new Segment UID.

**SFF-401** (reader) A reader rejects a sidecar whose `segment_uid` is not equal to the Segment UID
of the media file, and reports the rejection.

**SFF-402** (writer) A capture writer of a camera file writes the sidecar header, with the Segment
UID of the live file, before it writes the first frame. Before finalisation, it writes record k
after the container has written frame k + 1, with the live offset `offset` = file size − `size` of
frame k, and `offset_state` = 0. It writes the last record after the container closes, with a search
of the file end (`offset_state` = 1), or at finalisation.

**SFF-403** (writer) A writer uses live offsets only in a media file that has one track.

**SFF-404** (writer) A scan finds each block of the media file by an EBML walk from the Segment
start. It gives the payload offset, the size and the CRC-32 of each block. Finalisation uses these
values as the final offsets.

**SFF-405** (reader) A reader that scans a file accepts Clusters with an unknown size.

## 11. Unfinalised and crashed files

**SFF-450** (reader) In a live sidecar, a reader reads records from the first record to the first
record with a wrong `record_crc32`, or to a partial record at the end. It ignores all bytes after
that point. When `n_records` is 0, the reader counts the records from the file size.

**SFF-451** (reader) A reader MAY play a live camera file from its live sidecar. It uses only frames
with a valid record. It does not use a frame that has no record.

**SFF-452** (writer) A video recovery does these steps: read the valid records (SFF-450); remux the
file; pair each record to the block with the container timestamp of its `write_index`, and check
`jpeg_crc32`; drop each block that has no record; set `recovered` on each record and in the header;
then do finalisation steps 2 to 6.

**SFF-453** (writer) An audio recovery does these steps: read the valid records of the live audio
sidecar (SFF-450); keep each FLAC frame of the `.flac` file that has a valid packet record with a
matching `frame_crc32`; drop the FLAC frames after the last valid packet record; keep the timing
records; set `recovered`; then do the audio finalisation (section 9.1, with the stream copy as
step 1).

**SFF-454** (reader) A reader accepts these states after a crash: one timing record with no packet
record after it; one complete FLAC frame with no packet record; one video frame in the file with no
record; a sidecar with a header and no records; a media file with a header and no frames.

**SFF-455** (writer) After a recovery finalises every file of the take, it writes the recording
manifest again.

## 12. File, attachment and MIME names

| Item | Video | Audio |
|---|---|---|
| Sidecar magic | `SKVT` | `SKAT` |
| Separate sidecar | `<stem>.skvt` | `<stem>.skat` |
| Live sidecar | `<stem>.skvt` | `<stem>.skat.live` (the stem of the `.flac` file) |
| Attachment `FileName` | `video_timing.skvt` | `audio_timing.skat` |
| Attachment `FileMediaType` | `application/x-skellyfileformat-video-timing` | `application/x-skellyfileformat-audio-timing` |

`<stem>` is the name of the media file without its last extension. For example, the separate sidecar
of `take.id-a1b2.idx-0.mkv` is `take.id-a1b2.idx-0.skvt`, and the live audio sidecar of
`take.audio.flac` is `take.audio.skat.live`.

**SFF-500** (writer) A writer uses the names of the table in section 12.

**SFF-501** (reader) A reader finds a separate or live sidecar by the name of the table, in the
folder of its media file. It finds an embedded sidecar by `FileName` and `FileMediaType` together.

**SFF-502** (reader) A reader gets nothing from a file name except the name of the sidecar of a media
file.

## 13. Files that are not in this format

**SFF-550** (reader) A media file is in this format when it has an embedded sidecar (section 9.4)
with a known magic, or a separate or live sidecar with the name of section 12 and a known magic. A
separate sidecar must also have a `segment_uid` equal to the Segment UID of the media file. The live
sidecar of a `.flac` file is an exception, because a `.flac` file has no Segment UID.

**SFF-551** (reader) A recording with no file in this format is a legacy recording. This spec does
not tell how to read it.

**SFF-552** (reader) A file with a sidecar of an unknown `major` is "unsupported version" (SFF-051),
not legacy.

**SFF-553** (reader) A reader MAY index an MJPEG MKV file that has no usable sidecar by a scan. The
frames then have no times. The reader reports that the file is not in this format.

## 14. skellysync camera sidecar header (provisional)

skellysync writes camera files with the video sidecar of section 5, the FLAC track of section 8 and
`clock_id` 0x80. This section waits for the skellysync decisions D-Q, D-FPS, D-HDR and D-DRIFT.

**SFF-600** (provisional: skellysync D-FPS) The record field `source_frame_number` holds the index of
the source frame. `sample_time_ns` holds its source presentation time. `arrival_ns` holds the slot
time on the synthetic timeline. `fitted_ns` is absent, and no record has `fit_valid`.

**SFF-601** (provisional: skellysync D-Q, D-HDR and D-DRIFT) skellysync puts the source description
in the diagnostics JSON block: the file base name, size and content hash, the codec, bit depth, range
and transfer, the encoder and quality, and the sync result. A later minor version can move fields
into fixed binary.

**SFF-602** (writer) skellysync does not rotate the pixels. It writes the source rotation as
`display_rotation`.

## 15. The recording as a whole

### 15.1 Recording facts in the headers

**SFF-650** (writer) Each sidecar of a take holds the same `take_uuid`, `take_start_host_ns`,
`take_start_utc_ns`, `utc_offset_min`, `group_size` and `clock_id`.

**SFF-651** (writer) The writer takes `take_start_host_ns` and `take_start_utc_ns` at the same
moment, before the first frame or sample of any file of the take. `utc_offset_min` is the local
offset at that moment. A writer MUST NOT write a time-zone name.

**SFF-652** (writer) `group_size` is the number of camera files of the take. The audio file is not
counted.

**SFF-653** (writer) No file of this format holds an absolute path, a user name, a device name or a
raw serial number.

### 15.2 Opening a recording

**SFF-654** (reader) A reader opens a recording from one folder. It looks only at the files directly
in that folder, not in its subfolders. The recording is the files in this format (SFF-550) that hold
the same `take_uuid`.

**SFF-655** (reader) A reader MUST be able to open a recording without its manifest, also when some
files are live.

**SFF-656** (reader) A reader does not mix files with different `take_uuid` values. When the
manifest exists, a file with a `take_uuid` different from the manifest is stale: the reader ignores
it and reports a warning. When no manifest exists and the folder holds more than one take, the
reader reports each take.

**SFF-657** (reader) When a take has fewer camera files than `group_size`, the reader reports the
take as incomplete and opens the other files.

**SFF-658** (reader) The time zero of the take is `take_start_host_ns`. A reader shows no frame of a
camera before the first frame of that camera.

**SFF-659** (reader) When two camera files of one take have the same `camera_label`, the reader
reports a warning and keeps both files.

### 15.3 Recording manifest

The manifest is a UTF-8 JSON file `<rec>.skellyrec.json` in the recording folder. The writer chooses
`<rec>`. Example:

```json
{
  "skellyfileformat": {"major": 2, "minor": 0, "prerelease": 1},
  "writer": "skellycam 2.0.0",
  "take_uuid": "3f2a0c1e9b7d4e8a8f61c2d4b5a69e01",
  "group_size": 1,
  "take": {"start_host_ns": "123456789012345", "start_utc_ns": "1794500000000000000", "utc_offset_min": -300},
  "clock": {"id": 1, "freq_hz": "10000000"},
  "files": [
    {"path": "take.id-a1b2.idx-0.mkv", "kind": "camera", "camera_label": "a1b2",
     "camera_key": "1234567890123456789", "segment_uid": "cc82e5a1d3f04b7f9a1e2b3c4d5e6f70",
     "n_records": "1800", "nominal_rate": {"num": 30, "den": 1}, "display_rotation": 90},
    {"path": "take.audio.mka", "kind": "audio", "segment_uid": "0a1b2c3d4e5f60718293a4b5c6d7e8f9",
     "total_samples": "1440000", "sample_rate": 48000, "channels": 1}
  ]
}
```

**SFF-660** (writer) A writer writes the manifest with these members: `skellyfileformat` (`major`,
`minor`, `prerelease`), `writer`, `take_uuid`, `group_size`, `take` (`start_host_ns`,
`start_utc_ns`, `utc_offset_min`), `clock` (`id`, `freq_hz`) and `files`. Each item of `files` has
`path`, `kind` (`camera` or `audio`) and `segment_uid`. A camera item also has `camera_label`,
`n_records`, `nominal_rate` (`num`, `den`) and `display_rotation`, and `camera_key` when the header
sets it. The item of a file with audio also has `total_samples`, `sample_rate` and `channels`.

**SFF-661** (writer) Each 64-bit integer in the manifest is a JSON string of decimal digits, with a
`-` sign when negative. Each UID is in the text form of SFF-007. `path` is relative to the recording
folder and uses `/`.

**SFF-662** (writer) The manifest has the same values as the headers. Its `skellyfileformat.major`
is equal to the `major` of each listed sidecar.

**SFF-663** (writer) A writer writes the manifest to a temporary file in the recording folder, then
renames it over `<rec>.skellyrec.json`.

**SFF-664** (reader) When the manifest and a header disagree, the reader uses the header and reports
a warning.

## Appendix A. Golden files

Gate 2 makes these files. Each is committed with its SHA-256 sum and the script that made it, from
synthetic frames and pinned tools. The tests of [conformance.md](conformance.md) name them.

| # | Golden file | Sections |
|---|---|---|
| G1 | Finalised camera MKV, about 90 frames at a small size, with an embedded sidecar and valid fitted times | 4, 5, 9, 10 |
| G2 | The G1 media before the embed: no attachment, a separate finalised sidecar | 9.5 |
| G3 | Killed camera MKV (unknown-size Segment, no SeekHead) and its live sidecar, with a torn 37-byte tail, one record with a wrong CRC and one frame with no record | 11 |
| G4 | G3 after recovery | 11 |
| G5 | G1 remuxed by `ffmpeg -map 0 -c copy` (new Segment UID, Attachments before the Clusters) | 9.5, 10 |
| G6 | Sidecar-only vectors: offsets above 2^32 and near 2^53, INT64_MIN values, every flag bit, no fit, a zero-filled 4 KiB tail | 2, 5, 11 |
| G7 | Header vectors: a higher `minor` with more header bytes and a larger `record_size`; an unknown `major`; `prerelease` > 0; two files that differ only in the writer string; a wrong `header_crc32`; a wrong `body_crc32` | 3, 5.1 |
| G8 | Rotation vectors: `display_rotation` 0, 90, 180 and 270 with coloured corner markers and the expected upright corner colours | 5.2 |
| G9 | JPEG edge frames: no DHT; bytes after the entropy-coded data | 4 |
| G10 | Appender inputs: no tags; tags; Chapters in the header; a SeekHead with exactly 1 byte left; refusal inputs (Attachments present, no room, bytes after the Segment, unknown-size Segment) | 9.2 |
| G11 | Interrupted-embed states: Attachments after the Segment end; Segment size updated but SeekHead not | 9.6 |
| G12 | A file above 4 GiB with `FileData` past 4 GiB. The test makes it and does not commit it. | 9.4 |
| G13 | `.mka` with an embedded `.skat`, mono and stereo at 48 kHz, with the packet table and a drift table | 6, 7 |
| G14 | Killed `.flac` (STREAMINFO total 0) and its `.skat.live`: one timing record with no packet record; one FLAC frame with no packet record; a clean kill | 7, 11 |
| G15 | skellysync camera MKV: JPEG and FLAC 44.1 kHz stereo, embedded sidecar with an audio packet table | 8, 14 |
| G16 | Recording folders: finalised (4 cameras, `.mka`, manifest); the same without the manifest; a manifest that disagrees with a header; a stale file of another take; a missing camera; a crashed folder; two cameras with one label; two takes and no manifest | 15 |
| G17 | Files not in this format: MJPEG MKV with no sidecar; a small H.264 MP4; a WAV with a timestamp JSON | 13 |
