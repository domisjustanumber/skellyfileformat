# skellyfileformat conformance tests

Status: **draft v0, for review at gate 1**, together with [SPEC.md](SPEC.md). Gate 2 turns each test
into a runnable test and makes the golden files (SPEC.md Appendix A).

This list is normative. The license of the text is CC-BY-4.0 ([LICENSE](LICENSE)).

## How to read a test

- A test starts on a new line with its ID in bold, for example `**SFT-001**`, then its title.
- The next line starts with `Checks:` and gives the SFF IDs of the requirements that the test
  checks, for example `Checks: SFF-001, SFF-004`.
- A `Pass:` line gives the pass criteria. A test can also name its inputs, for example a golden file.
- A removed test keeps its line, with `(withdrawn)` after its ID.
- Each requirement of [SPEC.md](SPEC.md) that is not withdrawn has one or more tests.
  `tools/check_spec_traceability.py` checks the IDs and the links.
- The tests use the ID blocks of the spec sections (SPEC.md section 2).
- **Writer** tests run a writer and check its output. **Reader** tests run a reader on the inputs.
  A test marked `(provisional)` waits for the same open item as the requirement that it checks.
- "Python and JS" means that the Python reader and the JavaScript reader both run the test and give
  the same result.

## Tests

### Conventions (section 2)

**SFT-001** Reader and writer: sidecar codec round trip, Python and JS
Checks: SFF-001, SFF-002, SFF-003, SFF-006
Input: G1, G6, G13 and their reference values (a JSON file of each field, made by the generator);
writer output.
Pass: the CRC-32 of the ASCII bytes `123456789` is 0xCBF43926. Each decoded field of the golden files
is equal to its reference value. Each recomputed CRC-32 is equal to the stored CRC. Each INT64_MIN
time is reported as absent. The writer output, parsed with an independent table of offsets and types
made from SPEC.md, gives the values that the writer was given.

**SFT-002** Reader: 64-bit values in JavaScript
Checks: SFF-005
Input: G6 (offsets above 2^32 and near 2^53, times near ±2^53 from the base, INT64_MIN).
Pass: with `BigInt` and `DataView.prototype.getBigUint64` removed, the reader runs. Each value with a
magnitude below 2^53 is exact. Each value of 2^53 or more gives an error. INT64_MIN is "absent".

**SFT-003** Writer: alignment
Checks: SFF-004
Pass: in each sidecar that the writer makes, `header_size`, `record_size` and `table_record_size`
are multiples of 8, and each table offset is a multiple of 8.

**SFT-004** Writer: UID text form
Checks: SFF-007
Pass: each UID in the manifest matches `^[0-9a-f]{32}$` and is equal to the bytes in the header.

### Versioning (section 3)

**SFT-050** Reader: unknown major
Checks: SFF-050, SFF-051, SFF-552
Input: G7 (unknown `major`, other bytes after offset 10 changed, `header_crc32` wrong).
Pass: Python and JS report `unsupported_version`, not `bad_header_crc`. They give no records. They do
not report `legacy`.

**SFT-051** Reader: higher minor
Checks: SFF-052
Input: G7 (higher `minor`, more header bytes, larger `record_size`).
Pass: each known field is equal to its reference value. The reader finds each `record_crc32` in the
last 4 bytes of the larger records.

**SFT-052** Writer: version values
Checks: SFF-053
Pass: a prerelease writer writes `major` = 2, `minor` = 0 and `prerelease` > 0. A writer built as a
release writes `prerelease` = 0.

**SFT-053** Reader: prerelease file
Checks: SFF-054
Input: G7 (`prerelease` > 0).
Pass: the reader reads the file, or it refuses it with a "prerelease" message. It does not fail in
any other way.

**SFT-054** Reader: writer string has no effect
Checks: SFF-055
Input: G7 (two files that differ only in the writer string).
Pass: the reader output is identical for the two files.

**SFT-055** Writer and reader: reserved fields, padding and unknown bits
Checks: SFF-056
Input: writer output; G6 with undefined header flag bits, undefined record flag bits and non-zero
reserved bytes.
Pass: each reserved byte, padding byte and undefined bit in the writer output is 0. For G6, the
player times, the offsets and the frame list are identical to the same file with those bits and bytes
clear.

**SFT-056** Reader: the version comes from the sidecar
Checks: SFF-057
Input: G1, and G1 with the `major` of its embedded sidecar changed to an unknown value (the media
bytes are unchanged).
Pass: G1 reads. The changed file is "unsupported version".

**SFT-057** Reader: minor gate
Checks: SFF-058
Input: a generated version 2.0 file whose JSON block starts right after the fixed fields, read by a
reader built with a test field "added in minor 1" at that offset.
Pass: the reader does not read the test field from the 2.0 file.

### Video: the MKV profile (section 4)

**SFT-100** Writer and reader: MKV profile check
Checks: SFF-100, SFF-101, SFF-103, SFF-107
Input: writer output; G1; G15.
Pass: one video track with CodecID `V_MJPEG` (and one `A_FLAC` track in G15); each SimpleBlock has
the keyframe flag and is not laced; the video track number is below 128; no `Projection` element.

**SFT-101** Writer: passthrough
Checks: SFF-102, SFF-110
Input: a fake MJPEG camera that sends recorded JPEG frames.
Pass: the SHA-256 of each stored JPEG is equal to the SHA-256 of the frame that the camera sent
(100 %).

**SFT-102** Writer: no pixel rotation
Checks: SFF-103, SFF-159
Input: a fake camera with corner markers, mounted so that the picture is upright after a clockwise
rotation of 90 degrees.
Pass: the stored frames are equal to the frames that the camera sent. `display_rotation` is 90.
After a clockwise rotation of 90 degrees, the top-left corner has the colour of the stored
bottom-left corner.

**SFT-103** Writer: container timestamps
Checks: SFF-104
Input: fake cameras at 30/1 and 30000/1001, with dropped frames; a nominal rate of 1001/1.
Pass: TimestampScale is 1,000,000. The container timestamp of block k is k × den × 1000 / num ms,
round half up, also after a dropped frame. At 30000/1001, block 15 has the timestamp 501 ms. The
writer refuses the rate 1001/1.

**SFT-104** Writer: room for the attachment
Checks: SFF-105, SFF-106
Input: writer output (camera files and `.mka` files) after the container closes and before the
embed.
Pass: the first child of the Segment is a SeekHead, followed by a Void. 23 or more bytes of the
SeekHead span are not used by the SeekHead. The file has no Attachments element and no Chapters
after the first Cluster.

**SFT-105** Reader: JPEG edge frames
Checks: SFF-108
Input: G9.
Pass: the reader gives each frame with the correct offset and size, and the CRC check passes. It
gives no JPEG validation error.

**SFT-106** Reader: block header parsing
Checks: SFF-109
Input: a generated MKV with a video track number of 130 (a 2-byte track number in the block header).
Pass: the reader finds each payload at the correct offset.

**SFT-107** Writer: no timing inside frames
Checks: SFF-111
Input: writer output from a fake MJPEG camera; a fake raw camera that sends the same pixels twice with
different timestamps.
Pass: the MJPEG frames are byte-identical to the camera frames. The two JPEG frames of the raw camera
are byte-identical. The sidecar alone gives each time.

**SFT-108** Reader: Segment UID of a live file
Checks: SFF-112
Input: G3 (no SeekHead, unknown sizes).
Pass: the reader finds the `SegmentUID` of the live file and matches the live sidecar to it.

**SFT-109** Writer: Segment UID present
Checks: SFF-113
Input: two media files that the writer makes, each killed after its first frame.
Pass: each file has a 16-byte `SegmentUID` that is not all zero. The two values are different.

### Video timing sidecar (section 5)

**SFT-150** Reader and writer: common header layout
Checks: SFF-150
Input: G1, G13 and their reference values; writer output.
Pass: each common header field of the golden files is equal to its reference value, in Python and JS.
The writer output, parsed with an independent offset table made from SPEC.md, gives the values that
the writer was given.

**SFT-151** Writer and reader: header CRC and check order
Checks: SFF-151, SFF-152
Input: writer output, live and finalised; G7 (wrong `header_crc32`; wrong magic with a wrong
`header_crc32`; `header_size` larger than the file).
Pass: the writer output has a correct `header_crc32` in the live and the finalised sidecar. The reader
refuses the files with the reasons `bad_header_crc`, `bad_magic` and `bad_header_size`.

**SFT-152** Writer and reader: diagnostics JSON block
Checks: SFF-153, SFF-154
Input: writer output; G1 and G1 without its JSON block (generated).
Pass: the writer's JSON block is valid UTF-8 JSON at `json_offset`, after the fixed fields and before
`header_crc32`. All other bytes after the fixed fields are 0. The reader output is identical for G1
with and without the JSON block.

**SFT-153** Writer and reader: the `finalised` flag
Checks: SFF-155, SFF-156
Input: a writer killed after each write and rename of finalisation; G2 with `finalised` cleared and
`header_crc32` recomputed.
Pass: `finalised` appears only in the complete final sidecar of step 3. A later `separate_final`
sidecar differs from it only in bit 1 of `header_flags` and in `header_crc32`. The reader treats the
G2 file without `finalised` as live.

**SFT-154** Writer and reader: body CRC
Checks: SFF-157, SFF-158
Input: writer output; G7 (wrong `body_crc32` with one bad record).
Pass: the writer's `body_crc32` matches the body. For G7, a reader that checks `body_crc32` gives
only the records before the bad record and reports the sidecar as damaged.

**SFT-155** Reader: rotation
Checks: SFF-159, SFF-160
Input: G8, and a generated sidecar with `display_rotation` = 45.
Pass: for each G8 file, the corner colours of the upright frame are the expected colours. The reader
refuses the value 45.

**SFT-156** Writer: camera labels
Checks: SFF-161
Input: fake cameras; two fake cameras with the same label.
Pass: each label matches `^[A-Za-z0-9_-]{1,16}$`, and the labels of one take are different. The
writer refuses to start the take with the two equal labels.

**SFT-157** Writer: camera key
Checks: SFF-162
Input: a fake USB camera with vid 0x046D, pid 0x0843 and serial `TESTSERIAL01`.
Pass: `camera_key` is 5443682299978691806: the first 8 bytes, little-endian, of the SHA-256 of
`usb:046d:0843:TESTSERIAL01`.

**SFT-158** Writer: nominal rate
Checks: SFF-163
Pass: `nominal_rate_num` and `nominal_rate_den` are greater than 0 in each writer output.

**SFT-159** Writer: clock id
Checks: SFF-164
Pass: `clock_id` is a value of the table in SPEC.md section 5.3, and it is the same in all sidecars
of a take.

**SFT-160** (provisional) Writer: Linux and macOS clock ids
Checks: SFF-165
Pass: on Linux the writer writes `clock_id` 2, and on macOS 3. The video and audio times of one take
agree within the bound that the Linux and macOS timing tests give.

**SFT-161** Reader and writer: records and their size
Checks: SFF-166, SFF-168
Input: G1 (64-byte records); G7 (larger records); writer output.
Pass: each record field of the golden files is equal to its reference value. The reader steps by
`record_size` in both files. The writer output, parsed with an independent offset table, gives the
values that the writer was given.

**SFT-162** Writer: record to frame pairing
Checks: SFF-167, SFF-169
Input: a fake camera that writes its frame number as a barcode into each frame, with dropped
frames and an encoder failure.
Pass: for each record k, the bytes at `offset` have the CRC `jpeg_crc32`, the barcode is equal to
`source_frame_number`, and the block with the container timestamp of `write_index` k has the same
offset (100 %).

**SFT-163** Writer: gap and repeat flags
Checks: SFF-170
Input: a fake camera with the frame numbers 5, 6, 6, 9, 10, then 2^32 − 1, 0; and a fake camera with
frame numbers 20, 21, 22 where the encoder fails on 21.
Pass: `repeat` is set on the second 6 only. `gap` is set on 9 and on 2^32 − 1 only. The wrap to 0
sets no flag. The first record has neither flag. The record of 22 has `encode_skip` and `gap`.

**SFT-164** Writer: encode skip
Checks: SFF-171
Input: an encoder that fails on one frame.
Pass: the record of the next written frame has `encode_skip`. No other record has it.

**SFT-165** Writer: fitted times
Checks: SFF-172, SFF-175
Input: a fake camera on a known lattice (arrival = lattice time + 2 ms + jitter of 0 to 3 ms), with one
stall of 500 ms; a take with 1 frame.
Pass: after finalisation, every record has `fit_valid` and a `fitted_ns` that is not absent; outside
the stall, fitted time minus lattice time is the same value within 1 ms for every frame; the fitted
times do not decrease across the stall. The 1-frame file has no record with `fit_valid`.

**SFT-166** Writer: final offset state
Checks: SFF-173
Pass: each record of a finalised sidecar has `offset_state` = 2.

**SFT-167** Writer: time fields for each writer kind
Checks: SFF-174
Input: a fake camera with known arrival and sample times; a conversion of old timestamp files with
known values.
Pass: each time field is equal to the value that SPEC.md section 5.5 gives for the writer kind, and
is absent where that table says "absent".

**SFT-168** Reader: player time
Checks: SFF-176, SFF-178
Input: G1 (fit valid); G6 (no fit); G3 (live); G1 with `legacy_ns` changed (all CRCs and the embedded
attachment recomputed); a finalised sidecar with one record without `fit_valid`; a live sidecar with
`fit_valid` set.
Pass: the player time is `fitted_ns` for G1 and `arrival_ns` for the others. The G1 file with a
changed `legacy_ns` gives the same player times as G1.

**SFT-169** Writer and reader: player time does not decrease
Checks: SFF-177
Input: writer output; each golden file with video.
Pass: the player time does not decrease from one record to the next.

**SFT-170** Reader: refused sidecars
Checks: SFF-179
Input: G7 (each refusal case of SFF-179); a camera MKV with an embedded `SKAT` sidecar stored under
the attachment name `video_timing.skvt`.
Pass: Python and JS refuse each input with the reason code of SFF-179 for its case.

**SFT-171** Reader: larger audio records
Checks: SFF-180
Input: G7 (a `.skat` with a higher `minor` and 56-byte audio records).
Pass: the reader reads the known fields, finds `type` at offset 40 and the CRC in the last 4 bytes.

### Audio: FLAC in `.mka` (section 6)

**SFT-200** Writer: `.mka` profile and stream copy
Checks: SFF-200, SFF-201
Input: writer output; G13.
Pass: one track with CodecID `A_FLAC`; the CodecPrivate is exactly 42 bytes: `fLaC` and one
STREAMINFO block with the last-block flag; no laced block; each FLAC frame in the `.mka` is
byte-identical to the frame in the `.flac` file.

**SFT-201** Writer: audio write order
Checks: SFF-202, SFF-257
Input: a writer with a trace of each file write and flush, with callback blocks of 480 samples and
FLAC frames of 1,024 samples.
Pass: each timing record is in the file before each FLAC frame that holds any of its samples. Each
packet record follows its FLAC frame, before the next FLAC frame. Each write is flushed before the
next.

**SFT-202** Reader: STREAMINFO total is not used
Checks: SFF-203
Input: G14 after recovery (STREAMINFO total 0); the G14 `.mka` with a wrong non-zero STREAMINFO
total.
Pass: for both, the duration is `total_samples` / `sample_rate`.

**SFT-203** Writer: delete the `.flac` only after verify
Checks: SFF-204
Input: a finalisation with a CRC mismatch put into one `.mka` frame; a normal finalisation.
Pass: the writer keeps the `.flac` file after the mismatch, and deletes it after the normal
finalisation.

**SFT-204** Writer: one clock for audio and video
Checks: SFF-205
Input: one take with fake cameras and a fake microphone that start together.
Pass: the `.skat` and the `.skvt` files have the same `clock_id`. The first audio `host_ns` and the
first video `arrival_ns` differ by less than 100 ms, and both are at or after `take_start_host_ns`.

**SFT-205** Writer: audio container timestamps
Checks: SFF-206
Input: writer output at 48 kHz and 44.1 kHz.
Pass: the container timestamp of each FLAC frame is `first_sample` × 1000 / `sample_rate` ms, round
half up.

**SFT-206** (withdrawn)

**SFT-207** Reader: one audio file per take
Checks: SFF-208
Input: G16 (finalised) with the `.mka` renamed to a different stem.
Pass: the reader pairs the `.mka` with the take by `take_uuid`.

### Audio timing sidecar (section 7)

**SFT-250** Reader and writer: audio header and track descriptor
Checks: SFF-250, SFF-252
Input: G13 and its reference values; writer output.
Pass: each audio header field is equal to its reference value, and the writer output, parsed with an
independent offset table, gives the values that the writer was given. `table_record_size` is equal to
`record_size`. `total_samples` is the sum of `n_samples` of the packet table.

**SFT-251** (provisional) Writer: audio latency
Checks: SFF-251
Pass: until test A3 is done, `audio_latency_ns` is INT64_MIN.

**SFT-252** Reader: decode by offset with WebCodecs
Checks: SFF-253, SFF-259
Input: G13 (mono and stereo).
Pass: the reader builds the 42-byte description and decodes from packet 0 and from a packet in the
middle (a cold start). Decoded to 16-bit integers, the samples are equal to the reference decode;
decoded to floats, they are within one 16-bit step. The search gives the right packet for sample 0,
for the first sample of a packet, for the sample before it and for `total_samples` − 1. Sample
`total_samples` and sample −1 give an error.

**SFT-253** Writer: timing records
Checks: SFF-254, SFF-255
Input: a fake microphone; a fake audio API that gives an ADC time of 0.
Pass: `block_index` has no gap. With the fake API, each `adc_ns` is INT64_MIN.

**SFT-254** Writer: packet table
Checks: SFF-256, SFF-258
Input: writer output (live and final).
Pass: each packet record's `offset`, `size` and `frame_crc32` match the bytes of the `.mka` (final)
or the `.flac` (live). `first_sample` starts at 0 and has no gap. No record has `size` = 0. The final
sidecar has `table_offsets_final`. The live sidecar does not.

**SFT-255** (provisional) Writer and reader: drift table and mapping
Checks: SFF-260, SFF-261
Input: G13 (a known drift with one step, with `adc_ns` the time of sample `sample_index` + `frames`).
Pass: the writer finds the segments of the generator. The reader maps each test time to a sample
within ±1 sample of the reference.

**SFT-256** (provisional) Writer: ADC times on Linux and macOS
Checks: SFF-262
Pass: on Linux and macOS, `adc_ns` and `current_ns` have the meaning that the Linux and macOS audio
timing test gives.

**SFT-257** (provisional) Writer: drift table from host times
Checks: SFF-263
Input: a fake microphone that gives no ADC time, with a known drift.
Pass: the writer writes a drift table with `host_fit` on each record, and its segments match the
generator.

### Audio in the camera MKV (section 8)

**SFT-300** (provisional) Writer: skellysync audio
Checks: SFF-300, SFF-301, SFF-302, SFF-303
Input: a burst fixture (frame index in the pixels, irregular flashes, different left and right
channels); a source whose video starts after its audio; a 44.1 kHz source.
Pass: 0 samples of audio-to-video error; channels and sample rate kept; 16 bits per sample; the audio
does not continue after the last frame; the packet table follows the video records and matches a
scan; each record has `offset_state` = 2.

**SFT-301** Writer: skellysync audio timestamps
Checks: SFF-304
Input: G15 and writer output at 44.1 kHz.
Pass: the container timestamp of each FLAC frame is `first_sample` × 1000 / `sample_rate` ms, round
half up.

### Embedding and finalisation (section 9)

**SFT-350** Writer: finalisation order
Checks: SFF-350
Input: a writer killed after each write, flush and rename of finalisation, for a camera file and for
an audio file; a normal finalisation; a finalisation where one frame CRC does not match in step 2.
Pass: after a normal finalisation, each record has `offset_state` = 2, `segment_uid` is equal to the
Segment UID of the file, the fitted times are present, `finalised` is set, and the separate sidecar,
the `.flac` file and the live audio sidecar are deleted. Each kill leaves one of the states of the
table in SPEC.md section 9.7. The CRC mismatch stops the finalisation, and a recovery follows.

**SFT-351** Writer: manifest last
Checks: SFF-351
Input: a writer with a trace of file operations, for a take of 4 cameras and audio.
Pass: the rename of the manifest comes after the last operation of step 7 of every file.

**SFT-352** Writer: appender
Checks: SFF-352, SFF-355
Input: G10 (no tags; tags; Chapters in the header; 1 byte left; a SeekHead with a CRC-32 element);
G12; the appender with a trace of each write and flush.
Pass: only the Segment size, the SeekHead span and the bytes after the old end change. Each block has
the same offset, size and CRC. The SHA-256 of the extracted `FileData` is equal to the SHA-256 of the
sidecar. `FileUID` is not 0. The CRC-32 element is correct for the new SeekHead. ffprobe (the pinned
version) gives the same frame count. The trace shows: append, flush, Segment size, flush, SeekHead,
flush.

**SFT-353** Writer: appender refusals
Checks: SFF-353
Input: G10 refusal inputs (Attachments present, no room, bytes after the Segment, unknown-size
Segment, first Segment child not a SeekHead, Segment size width too small).
Pass: the appender gives an error for each input, and the SHA-256 of each file is unchanged.

**SFT-354** Writer: embed fallback
Checks: SFF-354
Input: a finalisation of a G10 refusal input.
Pass: the separate sidecar stays, with `separate_final` set.

**SFT-355** Writer: attachment position
Checks: SFF-356
Pass: in each finalised file, the Attachments element is after the last Cluster.

**SFT-356** Writer: verify and delete
Checks: SFF-357, SFF-358
Input: an embed with one changed `FileData` byte; an embed into a file whose last frame was changed
after the scan; a normal embed; a normal embed of a file with 0 frames; an audio embed.
Pass: the two changed embeds do not verify; the attachment is cut off, `separate_final` is set and the
separate sidecar stays. The normal embeds verify (the audio one by its packet records), and the
separate sidecar is deleted.

**SFT-357** Reader: locator, Python and JS
Checks: SFF-359, SFF-360
Input: G1; a plain MKV; G3; a file with a SeekHead entry that points to the wrong element; G12;
generated inputs for each failure.
Pass: G1 and G12 give the sidecar, and the reader reads no byte inside a Cluster. Each other input
gives its failure from the list of SFF-360.

**SFT-358** Reader: which sidecar to use
Checks: SFF-361, SFF-401
Input: G1 (embedded); G2 (separate); G1 next to a separate sidecar with another `segment_uid`; G5
next to the separate sidecar of G2; G1 with a wrong `header_crc32` in the embedded sidecar, next to
the separate sidecar of G2.
Pass: G1 uses the embedded sidecar. G2 uses the separate sidecar. The other separate sidecar is
rejected and reported. For G5, both sidecars are rejected and reported, and the reader indexes the
file by a scan, with no times. The file with the bad embedded sidecar uses the separate sidecar.

**SFT-359** Writer and reader: interrupted embed
Checks: SFF-362, SFF-363
Input: G11 (including the torn SeekHead span).
Pass: the reader uses the separate sidecar for each state. The recovery makes a file with one
attachment that the locator finds, a SeekHead span that parses, and each block unchanged.

**SFT-360** Writer and reader: finalisation not complete
Checks: SFF-364
Input: G2 with `finalised` cleared.
Pass: the reader treats the file as live. The writer recovers it as section 11 gives.

**SFT-361** Writer and reader: crash during finalisation
Checks: SFF-365
Input: each row of the table in SPEC.md section 9.7, made by a script from G1, G2 and G13.
Pass: for each row, the reader reports the state of the table and uses the file that it gives. The
recovery ends with a finalised file that passes SFT-350.

**SFT-362** Writer: repeatable recovery
Checks: SFF-366
Input: a recovery killed after each of its writes and renames, from G3 and G14, then run again.
Pass: each kill leaves a state of section 9.7 or section 11. Each second run ends with the same files
as an uninterrupted recovery.

**SFT-363** Writer and reader: open files during finalisation
Checks: SFF-367, SFF-368
Input: on Windows, a reader that opens a live camera file and its sidecar while the writer records and
then finalises; a test process that holds `<stem>.skvt` open without delete sharing for 2 s during
step 4.
Pass: the reader keeps no sidecar open after it reads it. The writer retries the blocked rename and
completes the finalisation after the test process closes the file. During the block, the files are
in the state before the rename.

### Segment UID, live offsets and final offsets (section 10)

**SFT-400** Writer: Segment UID in the header
Checks: SFF-400
Input: writer output; a recovered file.
Pass: `segment_uid` is equal to the `SegmentUID` of the media file, in the separate and the embedded
sidecar. After the recovery remux, it is the new Segment UID.

**SFT-401** Writer: live offsets
Checks: SFF-402, SFF-403
Input: a live writer stopped at random times, with frames of about 0.5 KiB, about 2 KiB and more than
40 KiB; a skellysync writer.
Pass: the sidecar header is in the file before the first frame. Each live record points at a JPEG
with the CRC `jpeg_crc32` (100 %), with `offset_state` 0, or 1 for the last record. The skellysync
writer writes no record with `offset_state` 0 or 1.

**SFT-402** Writer and reader: scan
Checks: SFF-404, SFF-405
Input: G1; G15 (video and FLAC blocks); G3 (partial last Cluster).
Pass: the scanned offsets of the track of the sidecar are equal to the record offsets, and each CRC
matches. The FLAC blocks of G15 are not in the video scan. The partial element at the end of G3 is
ignored.

### Unfinalised and crashed files (section 11)

**SFT-450** Reader: live sidecar
Checks: SFF-450, SFF-451
Input: G3 (its reference gives the expected record count); G6 (zero-filled 4 KiB tail).
Pass: the reader gives exactly the expected records: those before the torn tail, the wrong CRC or the
zero-filled bytes. The reader gives no frame that has no record.

**SFT-451** Writer: video recovery
Checks: SFF-452
Input: G3; the G3 variant with a record in the middle whose block has another CRC.
Pass: for G3, the records have the same `write_index`, `source_frame_number`, `arrival_ns`,
`sample_time_ns`, `size`, `jpeg_crc32` and flags (except bits 4 and 5) as G4. For the variant, the
recovered file ends before the record with the other CRC. Each offset is equal to a scan of the
recovered file. `segment_uid` is equal to the Segment UID of the file. The file passes SFT-100.

**SFT-452** Writer: video kill test
Checks: SFF-452, SFF-454
Input: kills at each writer point (before the mux, after the mux, in a record write, after a record,
after the container closes) and 3 kills at random times.
Pass: each record on disk pairs with a complete frame. A torn record is found. The records are a
subset of the frames in the file. After the recovery, the file passes SFT-100 and SFT-162.

**SFT-453** Writer: audio kill test
Checks: SFF-202, SFF-453, SFF-454
Input: 30 kills of an unpaced audio writer and 10 kills of a writer paced at 48 kHz. Each kill is an
external process kill (`TerminateProcess` on Windows, `SIGKILL` elsewhere) at a random time from a
generator with seed 20261112: 0.05 to 1.5 s after the first FLAC frame (unpaced) or 0.3 to 6 s
(paced). Only kills with a non-zero exit code count.
Pass: each packet record matches the FLAC bytes. The recovery accepts a timing record with no packet
record and a FLAC frame with no packet record. The recovered `.mka` decodes to an exact prefix of the
source.

**SFT-454** Reader: crash before the first frame
Checks: SFF-454
Input: a camera file with a header and no frames, with a header-only sidecar.
Pass: the reader reports `live` with no records and gives no error.

**SFT-455** Writer: manifest after recovery
Checks: SFF-455
Input: G16 (crashed folder).
Pass: after the recovery, the manifest exists and is equal to the reference manifest, except for the
Segment UIDs that the remux changed.

**SFT-456** Reader: audio crash states
Checks: SFF-454
Input: G14 (a timing record with no packet record; a FLAC frame with no packet record).
Pass: the reader reports `live` and gives the samples of the frames with a packet record.

### Names (section 12)

**SFT-500** Writer: names
Checks: SFF-500
Pass: the separate and live sidecar names, the attachment `FileName` and the `FileMediaType` are
exactly the values of SPEC.md section 12.

**SFT-501** Reader: find a sidecar
Checks: SFF-501
Input: G2; G14; a file with the correct `FileName` and a wrong `FileMediaType`.
Pass: the reader finds the separate and the live sidecars by name. It does not match the attachment
with the wrong `FileMediaType`.

**SFT-502** Reader: names have no other meaning
Checks: SFF-502
Input: G16 (finalised) with each media file and its sidecar renamed.
Pass: the reader gives the same recording: the same labels, rotations, order and t0.

**SFT-503** Reader: temporary files
Checks: SFF-503
Input: G16 (leftover `.tmp` files that hold a different, valid sidecar and media file); the §9.7 row 2
state.
Pass: the reader gives the same recording as without the `.tmp` files. For the row 2 state, it reports
`needs_recovery`.

**SFT-504** Reader: candidate media files
Checks: SFF-504
Input: a folder with an MKV named `a.bin`, a `.flac` named `b.dat`, a text file named `c.mkv`, and a
`.tmp` MKV.
Pass: the candidates are `a.bin` and `b.dat`.

### Files not in this format (section 13)

**SFT-550** Reader: classification
Checks: SFF-550, SFF-551, SFF-552, SFF-553
Input: G1; G3; G7 (unknown `major`); G17; a folder with only the G17 files.
Pass: G1 is `finalised`. G3 is `live`. G7 is `unsupported_version`. Each G17 file is `not_in_format`,
and the MJPEG MKV can be indexed by a scan, with no times. The folder with only G17 files is
`legacy`.

### skellysync camera sidecar (section 14)

**SFT-600** (provisional) Writer: skellysync records
Checks: SFF-600, SFF-601
Input: a source with the frame index in its pixels.
Pass: `source_frame_number` is the source frame index of each output frame. `sample_time_ns` is its
source presentation time minus the presentation time of the first source frame used. No record has
`fit_valid`. The JSON block holds the source description, and a reader reads the file without it.

**SFT-601** Writer: skellysync rotation
Checks: SFF-602
Input: a source with corner markers whose display matrix tells a player to turn the picture 90 degrees
clockwise to show it upright (FFmpeg `display_rotation` −90, which is counter-clockwise positive).
Pass: the stored frames are not rotated. `display_rotation` is 90. After a clockwise rotation of 90
degrees, the top-left corner has the colour of the stored bottom-left corner.

**SFT-602** (provisional) Writer: skellysync take start
Checks: SFF-603
Pass: `take_start_host_ns` is 0. `take_start_utc_ns` is the start of the source when the source
gives it.

### The recording as a whole (section 15)

**SFT-650** Writer: take facts
Checks: SFF-650, SFF-651, SFF-652
Input: a take with 4 fake cameras and a fake microphone, on a test machine whose time zone is set to
`America/Toronto` (Windows: Eastern Standard Time).
Pass: the sidecars have equal `take_uuid`, take start times, `utc_offset_min`, `group_size` and
`clock_id`. `take_uuid` is not all zero, and no take time is INT64_MIN. `take_start_host_ns` is before
the first frame and the first sample of every file. `group_size` is 4. No file holds the strings
`America/Toronto`, `Eastern Standard Time` or `EST`.

**SFT-651** Writer: no private data
Checks: SFF-653
Input: fake devices whose names, paths and serials hold known marker strings; a recording folder in a
path that holds a marker user name.
Pass: no marker string is in any file that the writer makes.

**SFT-652** Reader: open a folder
Checks: SFF-654, SFF-655, SFF-658
Input: G16 (finalised, and the same without the manifest), with a copy of one file in a subfolder.
Pass: both folders give the same files, labels, rotations and t0 (`take_start_host_ns`). The file in
the subfolder is not used. For each camera, the frame at a time before the player time of its first
record is "none".

**SFT-653** Reader: stale files and more than one take
Checks: SFF-656
Input: G16 (a stale file of another take; two takes and no manifest).
Pass: the stale file is ignored, with a warning. The folder with two takes gives two takes. No take
holds a file of the other take.

**SFT-654** Reader: missing camera
Checks: SFF-657
Input: G16 (`group_size` 4, three camera files).
Pass: the reader reports "incomplete" and opens the three files.

**SFT-655** Reader: duplicate labels
Checks: SFF-659
Input: G16 (two cameras with one label).
Pass: the reader reports a warning and opens both files.

**SFT-656** Writer: manifest content
Checks: SFF-660, SFF-661, SFF-662
Input: writer output for a take with 4 cameras and audio, one camera with no `camera_key`.
Pass: the manifest has each member of SFF-660. The camera with no key has no `camera_key` member.
Each 64-bit integer is a decimal string. Each UID matches SFF-007. Each `path` is relative and uses
`/`. Each value is equal to the value in the header of its file.

**SFT-657** Writer: manifest write is atomic
Checks: SFF-663
Input: a writer killed between the write of the temporary file and the rename.
Pass: `<rec>.skellyrec.json` is absent or holds a complete, valid manifest.

**SFT-658** Reader: header wins
Checks: SFF-664
Input: G16 (a manifest that disagrees with a header).
Pass: the reader uses the header value and reports a warning.


**SFT-659** Reader: camera order
Checks: SFF-665
Input: G16 (finalised) with `group_position` set on two cameras.
Pass: the two cameras with `group_position` come first, in its order. The others follow in the byte
order of `camera_label`.

**SFT-660** Reader: states and warnings
Checks: SFF-666
Input: G1, G3, G7 (unknown `major`; wrong `body_crc32`), G17 and the G16 folders.
Pass: each file and each take gets the expected state, and each expected warning is reported.

**SFT-661** Reader: take facts that disagree
Checks: SFF-667
Input: G16 (files of one take that disagree on `clock_id`), and variants that disagree on
`take_start_host_ns`, `utc_offset_min` and `group_size`.
Pass: for each, the reader reports a warning and uses the values of the first camera file.

**SFT-662** Reader: two manifests
Checks: SFF-668
Input: G16 (two manifests).
Pass: the reader reports a warning and opens the folder as if it had no manifest.