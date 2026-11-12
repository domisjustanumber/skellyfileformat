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

**SFT-001** Reader: sidecar codec round trip, Python and JS
Checks: SFF-001, SFF-002, SFF-003, SFF-006
Input: G1, G6, G13 and their reference values (a JSON file of each field, made by the generator).
Pass: each decoded field is equal to its reference value. Each recomputed CRC-32 is equal to the
stored CRC. Each INT64_MIN time is reported as absent.

**SFT-002** Reader: 64-bit values in JavaScript
Checks: SFF-005
Input: G6 (offsets above 2^32 and near 2^53, times near ±2^53 from the base, INT64_MIN).
Pass: each value with a magnitude below 2^53 is exact. Each value of 2^53 or more gives an error.
INT64_MIN is "absent". The reader does not use `BigInt`.

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
Input: G7 (unknown `major`).
Pass: Python and JS report "unsupported version". They give no records. They do not report
"legacy".

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

**SFT-055** Writer and reader: reserved fields and unknown bits
Checks: SFF-056
Input: writer output; G6 with undefined header flag bits and record flag bits set.
Pass: each reserved byte and each undefined bit in the writer output is 0. For G6, the player times,
the offsets and the frame list are identical to the same file with those bits clear.

**SFT-056** Reader: the version comes from the sidecar
Checks: SFF-057
Input: G1, and G1 with the `major` of its embedded sidecar changed to an unknown value (the media
bytes are unchanged).
Pass: G1 reads. The changed file is "unsupported version".

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
Input: a fake camera with corner markers, configured with a rotation of 90 degrees.
Pass: the stored frames are equal to the frames that the camera sent. `display_rotation` is the
value that shows the frame upright (SFF-159).

**SFT-103** Writer: container timestamps
Checks: SFF-104
Input: fake cameras at 30/1 and 30000/1001, with dropped frames.
Pass: the container timestamp of block k is k × den / num seconds, rounded to the TimestampScale,
also after a dropped frame.

**SFT-104** Writer: room for the attachment
Checks: SFF-105, SFF-106
Input: writer output before finalisation.
Pass: the first child of the Segment is a SeekHead, followed by a Void. The SeekHead and Void span
has 23 or more unused bytes. The file has no Attachments element and no Chapters after the first
Cluster.

**SFT-105** Reader: JPEG edge frames
Checks: SFF-108
Input: G9.
Pass: the reader gives each frame with the correct offset and size, and the CRC check passes. It
gives no JPEG validation error.

**SFT-106** Reader: block header parsing
Checks: SFF-109
Input: a generated MKV with a video track number of 130 (a 2-byte track number in the block header).
Pass: the reader finds each payload at the correct offset.

### Video timing sidecar (section 5)

**SFT-150** Reader: common header layout
Checks: SFF-150
Input: G1, G13, and their reference values.
Pass: each common header field is equal to its reference value, in Python and JS.

**SFT-151** Writer and reader: header CRC
Checks: SFF-151, SFF-152
Input: writer output after finalisation; G7 (wrong `header_crc32`).
Pass: the writer output has a correct `header_crc32`. The reader refuses the G7 file.

**SFT-152** Writer and reader: diagnostics JSON block
Checks: SFF-153, SFF-154
Input: writer output; G1 and G1 without its JSON block (generated).
Pass: the writer's JSON block is valid UTF-8 JSON inside the header, before `header_crc32`. The
reader output is identical for G1 with and without the JSON block.

**SFT-153** Writer and reader: the `finalised` flag
Checks: SFF-155, SFF-156
Input: a writer stopped at each finalisation step; G2 with `finalised` cleared.
Pass: the writer sets `finalised` only after step 3 is complete. The reader treats the G2 file
without `finalised` as live.

**SFT-154** Writer and reader: body CRC
Checks: SFF-157, SFF-158
Input: writer output; G7 (wrong `body_crc32`).
Pass: the writer's `body_crc32` matches the body. For G7, the reader checks each record CRC and
reports the sidecar as damaged.

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
Input: a fake USB camera with known vid, pid and serial.
Pass: `camera_key` is the first 8 bytes, as a little-endian `u64`, of the SHA-256 of the string
that the writer documents for that camera.

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

**SFT-161** Reader: records and their size
Checks: SFF-166, SFF-168
Input: G1 (64-byte records); G7 (larger records).
Pass: each record field is equal to its reference value. The reader steps by `record_size` in both
files.

**SFT-162** Writer: record to frame pairing
Checks: SFF-167, SFF-169
Input: a fake camera that writes its frame number as a barcode into each frame, with dropped
frames and an encoder failure.
Pass: for each record k, the bytes at `offset` have the CRC `jpeg_crc32`, the barcode is equal to
`source_frame_number`, and the block with the container timestamp of `write_index` k has the same
offset (100 %).

**SFT-163** Writer: gap and repeat flags
Checks: SFF-170
Input: a fake camera with dropped and repeated frame numbers, and a frame number that wraps at 2^32.
Pass: `gap` is set exactly on the records after a jump, and `repeat` exactly on the repeated
numbers. The wrap at 2^32 sets no flag. The first record has neither flag.

**SFT-164** Writer: encode skip
Checks: SFF-171
Input: an encoder that fails on one frame.
Pass: the record of the next written frame has `encode_skip`. No other record has it.

**SFT-165** Writer: fitted times
Checks: SFF-172, SFF-175
Input: a fake camera with jitter and one stall.
Pass: after finalisation, every record has `fit_valid` and a `fitted_ns` that is not absent. In a
file that has no fit, no record has `fit_valid`.

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
Input: G1 (fit valid); G6 (no fit); G3 (live); G1 with `legacy_ns` changed.
Pass: the player time is `fitted_ns` for G1 and `arrival_ns` for G6 and G3. The G1 file with a
changed `legacy_ns` gives the same player times as G1.

**SFT-169** Writer and reader: player time does not decrease
Checks: SFF-177
Input: writer output; each golden file with video.
Pass: the player time does not decrease from one record to the next.

### Audio: FLAC in `.mka` (section 6)

**SFT-200** Writer: `.mka` profile and stream copy
Checks: SFF-200, SFF-201
Input: writer output; G13.
Pass: one track with CodecID `A_FLAC`; CodecPrivate starts with `fLaC` and then STREAMINFO; no laced
block; each FLAC frame in the `.mka` is byte-identical to the frame in the `.flac` file.

**SFT-201** Writer: audio write order
Checks: SFF-202, SFF-257
Input: a writer with a trace of each file write and flush.
Pass: for each block, the trace shows the timing record, then the FLAC frame, then its packet
record, each flushed before the next write.

**SFT-202** Reader: STREAMINFO total of 0
Checks: SFF-203
Input: the recovered `.mka` of G14 (STREAMINFO total samples = 0).
Pass: the reader gives the duration from `total_samples` and the packet table.

**SFT-203** Writer: delete the `.flac` only after verify
Checks: SFF-204
Input: a finalisation with a CRC mismatch put into one `.mka` frame; a normal finalisation.
Pass: the writer keeps the `.flac` file after the mismatch, and deletes it after the normal
finalisation.

**SFT-204** Writer: one clock for audio and video
Checks: SFF-205
Input: one take with fake cameras and a fake microphone.
Pass: the `.skat` and the `.skvt` files have the same `clock_id`. The audio `host_ns` values and the
video `arrival_ns` values are in the same time range of the take.

### Audio timing sidecar (section 7)

**SFT-250** Reader: audio header and track descriptor
Checks: SFF-250, SFF-252
Input: G13 and its reference values.
Pass: each audio header field is equal to its reference value. `table_record_size` is equal to
`record_size`. `total_samples` is the sum of `n_samples` of the packet table.

**SFT-251** (provisional) Writer: audio latency
Checks: SFF-251
Pass: until test A3 is done, `audio_latency_ns` is INT64_MIN.

**SFT-252** Reader: decode by offset with WebCodecs
Checks: SFF-253, SFF-259
Input: G13 (mono and stereo).
Pass: the reader builds the 42-byte description and decodes from packet 0 and from a packet in the
middle (a cold start). The samples are equal to the reference decode, within one 16-bit step.

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
Input: G13 (a known drift with one step).
Pass: the writer finds the segments of the generator. The reader maps each test time to a sample
within ±1 sample of the reference.

### Audio in the camera MKV (section 8)

**SFT-300** Writer: skellysync audio
Checks: SFF-300, SFF-301, SFF-302, SFF-303
Input: a burst fixture (frame index in the pixels, irregular flashes, different left and right
channels); a source whose video starts after its audio; a 44.1 kHz source.
Pass: 0 samples of audio-to-video error; channels and sample rate kept; 16 bits per sample; the audio
does not continue after the last frame; the packet table follows the video records and matches a
scan; each record has `offset_state` = 2.

### Embedding and finalisation (section 9)

**SFT-350** Writer: finalisation order
Checks: SFF-350
Input: a writer stopped after each finalisation step; a normal finalisation.
Pass: after a normal finalisation, each record has `offset_state` = 2, `segment_uid` is equal to the
Segment UID of the file, the fitted times are present, `finalised` is set and the separate sidecar
is deleted. A stop at each step leaves the state that SPEC.md section 9.1 gives for that step.

**SFT-351** Writer: manifest last
Checks: SFF-351
Input: a writer with a trace of file operations, for a take of 4 cameras and audio.
Pass: the rename of the manifest comes after the last delete of finalisation step 6.

**SFT-352** Writer: appender
Checks: SFF-352, SFF-355
Input: G10 (no tags; tags; Chapters in the header; 1 byte left).
Pass: only the Segment size, the SeekHead and Void span and the bytes after the old end change. Each
block has the same offset, size and CRC. The SHA-256 of the extracted `FileData` is equal to the
SHA-256 of the sidecar. `FileUID` is not 0. ffprobe gives the same frame count.

**SFT-353** Writer: appender refusals
Checks: SFF-353
Input: G10 refusal inputs.
Pass: the appender gives an error, and the SHA-256 of each file is unchanged.

**SFT-354** Writer: embed fallback
Checks: SFF-354
Input: a finalisation of a G10 refusal input.
Pass: the separate sidecar stays, with `separate_final` set.

**SFT-355** Writer: attachment position
Checks: SFF-356
Pass: in each finalised file, the Attachments element is after the last Cluster.

**SFT-356** Writer: verify and delete
Checks: SFF-357, SFF-358
Input: an embed with one changed `FileData` byte; a normal embed.
Pass: the changed embed does not verify, and the separate sidecar stays. The normal embed verifies,
and the separate sidecar is deleted.

**SFT-357** Reader: locator, Python and JS
Checks: SFF-359, SFF-360
Input: G1; a plain MKV; G3; a file with a SeekHead entry that points to the wrong element; G12;
generated inputs for each failure.
Pass: G1 and G12 give the sidecar in 3 reads. Each other input gives its failure from the list of
SFF-360. The locator reads no Cluster.

**SFT-358** Reader: which sidecar to use
Checks: SFF-361, SFF-401
Input: G1 (embedded); G2 (separate); G1 next to a separate sidecar with another `segment_uid`; G5.
Pass: G1 uses the embedded sidecar. G2 uses the separate sidecar. The other separate sidecar is
rejected and reported. For G5, both sidecars are rejected and reported, and the reader indexes the
file by a scan, with no times.

**SFT-359** Writer and reader: interrupted embed
Checks: SFF-362, SFF-363
Input: G11.
Pass: the reader uses the separate sidecar for both states. The recovery makes a file with one
attachment that the locator finds, and each block is unchanged.

**SFT-360** Writer and reader: finalisation not complete
Checks: SFF-364
Input: G2 with `finalised` cleared.
Pass: the reader treats the file as live. The writer recovers it as section 11 gives.

### Segment UID, live offsets and final offsets (section 10)

**SFT-400** Writer: Segment UID in the header
Checks: SFF-400
Input: writer output; a recovered file.
Pass: `segment_uid` is equal to the `SegmentUID` of the media file, in the separate and the embedded
sidecar. After the recovery remux, it is the new Segment UID.

**SFT-401** Writer: live offsets
Checks: SFF-402, SFF-403
Input: a live writer stopped at random times; a skellysync writer.
Pass: the sidecar header is in the file before the first frame. Each live record points at a JPEG
with the CRC `jpeg_crc32` (100 %), with `offset_state` 0, or 1 for the last record. The skellysync
writer writes no record with `offset_state` 0 or 1.

**SFT-402** Writer and reader: scan
Checks: SFF-404, SFF-405
Input: G1; G15; G3 (unknown-size Clusters).
Pass: the scanned offsets are equal to the record offsets, and each CRC matches.

### Unfinalised and crashed files (section 11)

**SFT-450** Reader: live sidecar
Checks: SFF-450, SFF-451
Input: G3; G6 (zero-filled 4 KiB tail).
Pass: the records stop before the torn tail, the wrong CRC or the zero-filled bytes. The record count
comes from the file size. The reader gives no frame that has no record.

**SFT-451** Writer: video recovery
Checks: SFF-452
Input: G3.
Pass: the output is equal to G4 (records, offsets and flags). `segment_uid` is equal to the Segment
UID of the file. The file passes SFT-100.

**SFT-452** Writer: video kill test
Checks: SFF-452, SFF-454
Input: kills at each writer point (before the mux, after the mux, in a record write, after a record,
after the container closes) and 3 kills at random times.
Pass: each record on disk pairs with a complete frame. A torn record is found. The records are a
subset of the frames in the file. After the recovery, the file passes SFT-100 and SFT-162.

**SFT-453** Writer: audio kill test
Checks: SFF-202, SFF-453, SFF-454
Input: 30 fast and 10 real-time external kills of the audio writer (the method of the 2026-11-12
`TerminateProcess` test, with one live audio sidecar).
Pass: each packet record matches the FLAC bytes. The recovery accepts a timing record with no packet
record and a FLAC frame with no packet record. The recovered `.mka` decodes to an exact prefix of the
source.

**SFT-454** Reader: crash before the first frame
Checks: SFF-454
Input: a camera file with a header and no frames, with a header-only sidecar.
Pass: the reader reports "live, no frames" and gives no error.

**SFT-455** Writer: manifest after recovery
Checks: SFF-455
Input: G16 (crashed folder).
Pass: after the recovery, the manifest exists and is equal to the reference manifest, except for the
Segment UIDs that the remux changed.

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

### Files not in this format (section 13)

**SFT-550** Reader: classification
Checks: SFF-550, SFF-551, SFF-552, SFF-553
Input: G1; G3; G7 (unknown `major`); G17.
Pass: G1 is "in format, finalised". G3 is "in format, live". G7 is "unsupported version". The MJPEG
MKV of G17 is "not in this format" and can be indexed by a scan, with no times. The MP4 and the WAV
of G17 are "not in this format".

### skellysync camera sidecar (section 14)

**SFT-600** (provisional) Writer: skellysync records
Checks: SFF-600, SFF-601
Input: a source with the frame index in its pixels.
Pass: `source_frame_number` is the source frame index of each output frame. `sample_time_ns` is its
source presentation time. No record has `fit_valid`. The JSON block holds the source description,
and a reader reads the file without it.

**SFT-601** Writer: skellysync rotation
Checks: SFF-602
Input: a source with a display matrix of 90 degrees and corner markers.
Pass: the stored frames are not rotated. `display_rotation` shows them upright (SFF-159).

### The recording as a whole (section 15)

**SFT-650** Writer: take facts
Checks: SFF-650, SFF-651, SFF-652
Input: a take with 4 fake cameras and a fake microphone.
Pass: the sidecars have equal `take_uuid`, take start times, `utc_offset_min`, `group_size` and
`clock_id`. `take_start_host_ns` is before the first frame and the first sample of every file.
`group_size` is 4. No file holds a time-zone name.

**SFT-651** Writer: no private data
Checks: SFF-653
Input: fake devices whose names, paths and serials hold known marker strings; a recording folder in a
path that holds a marker user name.
Pass: no marker string is in any file that the writer makes.

**SFT-652** Reader: open a folder
Checks: SFF-654, SFF-655, SFF-658
Input: G16 (finalised, and the same without the manifest), with a copy of one file in a subfolder.
Pass: both folders give the same files, labels, rotations and t0 (`take_start_host_ns`). The file in
the subfolder is not used. No frame of a camera is shown before its first frame.

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
Input: writer output for a take with 4 cameras and audio.
Pass: the manifest has each member of SFF-660. Each 64-bit integer is a decimal string. Each UID
matches SFF-007. Each `path` is relative and uses `/`. Each value is equal to the value in the
header of its file.

**SFT-657** Writer: manifest write is atomic
Checks: SFF-663
Input: a writer killed between the write of the temporary file and the rename.
Pass: `<rec>.skellyrec.json` is absent or holds a complete, valid manifest.

**SFT-658** Reader: header wins
Checks: SFF-664
Input: G16 (a manifest that disagrees with a header).
Pass: the reader uses the header value and reports a warning.
