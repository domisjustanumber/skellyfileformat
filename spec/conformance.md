# skellyfileformat conformance tests

Status: **draft v1 (MCAP profile), for review at gate 1**, together with [SPEC.md](SPEC.md). Gate 2
turns each test into a runnable test and makes the golden files (SPEC.md Appendix A). The tests of
draft v0 stay in this file, marked withdrawn.

This list is normative. The license of the text is CC-BY-4.0 ([LICENSE](LICENSE)).

## How to read a test

- A test starts on a new line with its ID in bold, for example `**SFT-005**`, then its title.
- The next line starts with `Checks:` and gives the SFF IDs of the requirements that the test
  checks, for example `Checks: SFF-008, SFF-009`.
- A `Pass:` line gives the pass criteria. A test can also name its inputs, for example a golden file.
- A removed test keeps its line, with `(withdrawn)` after its ID. The withdrawn lines of a section
  come first in that section.
- Each requirement of [SPEC.md](SPEC.md) that is not withdrawn has one or more tests.
  `tools/check_spec_traceability.py` checks the IDs and the links.
- The tests use the ID blocks of the spec sections (SPEC.md section 2).
- **Writer** tests run a writer and check its output. **Reader** tests run a reader on the inputs.
  A test marked `(provisional)` waits for the same open item as the requirement that it checks.
- "Python and JS" means that the Python reader and the JavaScript reader both run the test and give
  the same reader result (SPEC.md SFF-678), byte for byte.
- "The MCAP checks" means: `mcap doctor` of the MCAP CLI (pinned version) exits 0 on a finished file,
  and the pinned Python `mcap` library reads every record with CRC validation on.

## Tests

### Conventions (section 2)

**SFT-001** (withdrawn) Draft v0.

**SFT-002** (withdrawn) Draft v0.

**SFT-003** (withdrawn) Draft v0.

**SFT-004** (withdrawn) Draft v0.

**SFT-005** Writer: the output is valid MCAP with valid metadata values
Checks: SFF-008, SFF-009, SFF-010, SFF-011, SFF-013
Input: writer output of a short take (2 cameras, audio).
Pass: the MCAP checks pass. Each metadata value matches SFF-009 or SFF-010 by a regular expression.
Each protobuf `timestamp` has `nanos` from 0 to 999,999,999. `take_uuid` is 32 lowercase hexadecimal
characters.

**SFT-006** Reader: metadata form errors, Python and JS
Checks: SFF-009, SFF-010
Input: G7.
Pass: each file with a bad integer form has the state `not_in_format` with the reason
`bad_metadata`. The results of the two readers are equal to the committed result.

**SFT-007** Reader: 64-bit values in JavaScript
Checks: SFF-012
Input: G1 and G10, and a file whose times are near ±2^53 from `take_start_host_ns`.
Pass: each time below 2^53 from the take start is exact. A difference of 2^53 or more gives an error.
No value is rounded.

### Versioning (section 3)

**SFT-050** (withdrawn) Draft v0.

**SFT-051** (withdrawn) Draft v0.

**SFT-052** (withdrawn) Draft v0.

**SFT-053** (withdrawn) Draft v0.

**SFT-054** (withdrawn) Draft v0.

**SFT-055** (withdrawn) Draft v0.

**SFT-056** (withdrawn) Draft v0.

**SFT-057** (withdrawn) Draft v0.

**SFT-058** Writer: version metadata and writer string
Checks: SFF-059, SFF-062, SFF-064
Pass: each device file has one `freemocap.format` record with `major` = 2, `minor` = 0 and the
prerelease revision of the build. The Header `library` is the writer string.

**SFT-059** Reader: version vectors, Python and JS
Checks: SFF-060, SFF-061, SFF-063, SFF-064, SFF-065, SFF-066
Input: G6.
Pass: the higher-`minor` file opens, and its unknown key, channel and record are ignored. The
unknown-`major` file has the state `unsupported_version`, not `legacy`. A reader that refuses
`prerelease` > 0 says so in its result. The two files that differ only in `library` give equal
results. A file whose magic version byte differs is not read as another format version.

### The MCAP profile (section 4)

**SFT-100** (withdrawn) Draft v0.

**SFT-101** (withdrawn) Draft v0.

**SFT-102** (withdrawn) Draft v0.

**SFT-103** (withdrawn) Draft v0.

**SFT-104** (withdrawn) Draft v0.

**SFT-105** (withdrawn) Draft v0.

**SFT-106** (withdrawn) Draft v0.

**SFT-107** (withdrawn) Draft v0.

**SFT-108** (withdrawn) Draft v0.

**SFT-109** (withdrawn) Draft v0.

**SFT-110** Writer: files, profile, schemas and channels
Checks: SFF-114, SFF-115, SFF-116, SFF-117, SFF-124
Input: writer output of a take of 2 cameras and audio.
Pass: there is one camera file per camera and one audio file. Each Header `profile` is `freemocap`.
Each Channel has `message_encoding` = `protobuf`. Each Schema has `encoding` = `protobuf`, a name of
the table of SFF-116, and a FileDescriptorSet with those field numbers. The channels are exactly those
of SFF-117. There is no Attachment record.

**SFT-111** Writer: chunks
Checks: SFF-118, SFF-119, SFF-121, SFF-122
Pass: each Message is in a Chunk of one channel, with `compression` = "" and a correct non-zero
`uncompressed_crc`, followed by its Message Index records. Each image Chunk holds 1 Message. Each
audio Chunk holds 5 Messages, except the last. In each channel, `log_time` never decreases.

**SFT-112** Reader: any frames per chunk, Python and JS
Checks: SFF-120
Input: G1 and G3.
Pass: for each position p, the reader reads the frame from Chunk ⌊p / `frames_per_chunk`⌋ with one
read of that Chunk. The JPEG bytes and `sequence` of each frame are equal to those of the generator.

**SFT-113** Writer: where the metadata records are
Checks: SFF-123
Input: writer output, and the same output cut after its first Chunk.
Pass: `freemocap.format` and `freemocap.recording` are after the Header and before the first Chunk.
`freemocap.timing` is after the last Chunk and before Data End. The cut file still holds the first
two records.

### Camera files (section 5)

**SFT-150** (withdrawn) Draft v0.

**SFT-151** (withdrawn) Draft v0.

**SFT-152** (withdrawn) Draft v0.

**SFT-153** (withdrawn) Draft v0.

**SFT-154** (withdrawn) Draft v0.

**SFT-155** (withdrawn) Draft v0.

**SFT-156** (withdrawn) Draft v0.

**SFT-157** (withdrawn) Draft v0.

**SFT-158** (withdrawn) Draft v0.

**SFT-159** (withdrawn) Draft v0.

**SFT-160** (withdrawn) Draft v0.

**SFT-161** (withdrawn) Draft v0.

**SFT-162** (withdrawn) Draft v0.

**SFT-163** (withdrawn) Draft v0.

**SFT-164** (withdrawn) Draft v0.

**SFT-165** (withdrawn) Draft v0.

**SFT-166** (withdrawn) Draft v0.

**SFT-167** (withdrawn) Draft v0.

**SFT-168** (withdrawn) Draft v0.

**SFT-169** (withdrawn) Draft v0.

**SFT-170** (withdrawn) Draft v0.

**SFT-171** (withdrawn) Draft v0.

**SFT-172** Writer: camera channel metadata
Checks: SFF-181, SFF-182, SFF-183, SFF-184, SFF-192
Input: writer output with a camera that has a known serial number; a writer started with two cameras
of one label.
Pass: the image Channel has the keys of section 5. `camera_label` matches its rule and is in the
topic. `camera_key` is the first 8 bytes of the SHA-256 of the identity string, as an unsigned
little-endian integer. `nominal_rate` has `<num>` and `<den>` from 1 to 2^20. `group_position` is
written only when an order was given. The writer refuses the take with two cameras of one label.

**SFT-173** Reader: bad camera metadata, Python and JS
Checks: SFF-184, SFF-186
Input: G7.
Pass: the rate vectors have the reason `bad_rate`. The rotation vector has the reason
`bad_rotation`. The results are equal to the committed results.

**SFT-174** Reader: rotation
Checks: SFF-185, SFF-186
Input: G8.
Pass: after the reader applies `display_rotation`, each corner has the expected colour. The stored
JPEG bytes are not rotated.

**SFT-175** Writer: image messages and their times
Checks: SFF-187, SFF-188
Input: writer output from a test source with known frame numbers, arrival times and sample times,
some frames with no sample time.
Pass: each `data` is one complete JPEG from SOI to EOI, identical to the source bytes. `format` is
`jpeg` and `frame_id` is the label. `log_time` and `publish_time` are the arrival time. `sequence` is
the source frame number modulo 2^32. `timestamp` is the sample time, and it is unset for the frames
with none.

**SFT-176** Reader: unset sample time
Checks: SFF-189
Input: G9.
Pass: the result gives `sample_time` null for every frame, not 0.

**SFT-177** Writer and reader: encoder skips
Checks: SFF-190, SFF-191
Input: writer output from a test source whose encoder fails on 2 known frames; G9.
Pass: the log channel has 2 `foxglove.Log` Messages with `level` = `WARNING`, `name` =
`skellyfileformat.encode_skip` and the arrival times of the 2 frames. The positions of the other
frames are consecutive. The reader reports `encode_skips` = 2 and the warning `encode_skip`.

**SFT-178** Reader: camera order
Checks: SFF-192
Input: G11.
Pass: the files of each take are in the order of `group_position` (unset last), then of the bytes of
`camera_label`.

### Audio files (section 6)

**SFT-200** (withdrawn) Draft v0.

**SFT-201** (withdrawn) Draft v0.

**SFT-202** (withdrawn) Draft v0.

**SFT-203** (withdrawn) Draft v0.

**SFT-204** (withdrawn) Draft v0.

**SFT-205** (withdrawn) Draft v0.

**SFT-206** (withdrawn) Draft v0.

**SFT-207** (withdrawn) Draft v0.

**SFT-208** Writer: audio channel metadata and encoder settings
Checks: SFF-209, SFF-210
Input: writer output from a mono and a stereo test signal, and from a 4-channel test signal.
Pass: the audio Channel has the keys of section 6. `opus_head` decodes to a valid RFC 7845 header
with mapping family 0, and its channel count and pre-skip are equal to `channels` and `pre_skip`.
The 4-channel signal gives `channels` = 2. The encoder settings in the writer's log are those of
SFF-210.

**SFT-209** Writer: audio messages and their times
Checks: SFF-211, SFF-212
Pass: each `data` is one raw Opus packet that decodes to 960 samples. `format` is `opus`.
`sequence` counts 0, 1, 2 and so on. `log_time` and `publish_time` are the arrival times of the
callback blocks. `timestamp` of packet 0 is the time of the first microphone sample minus
`pre_skip` × 10^9 / 48000 ns, within 1 sample.

**SFT-210** (provisional) Writer: audio timestamps follow the microphone clock
Checks: SFF-213
Input: a test source whose sample clock runs 20 ppm fast against the host clock.
Pass: the timestamps of consecutive packets differ by 20 ms × (1 − 20 × 10^−6), within 1 sample over
the take.

**SFT-211** Reader: audio decoding and placement, Python and JS
Checks: SFF-214, SFF-216
Input: G1 and G2 (clicks every 500 ms).
Pass: the reader decodes with no Opus header and drops `pre_skip` samples. Each click is at its
expected time within 0 samples. With an `audio_latency_ns` added to a copy of G1, the click times move
by that value.

**SFT-212** Reader: seek pre-roll
Checks: SFF-215
Input: G1, 20 seek targets.
Pass: after each seek, the 80 ms after the target are within −25 dB RMS of a full decode of the same
range.

**SFT-213** Reader: Opus header mismatch
Checks: SFF-217
Input: G7 (a `channels` value that disagrees with `opus_head`).
Pass: the reader uses the channel count in `opus_head` and reports `opus_head_mismatch`.

### Clocks, times and the fit (section 7)

**SFT-250** (withdrawn) Draft v0.

**SFT-251** (withdrawn) Draft v0.

**SFT-252** (withdrawn) Draft v0.

**SFT-253** (withdrawn) Draft v0.

**SFT-254** (withdrawn) Draft v0.

**SFT-255** (withdrawn) Draft v0.

**SFT-256** (withdrawn) Draft v0.

**SFT-257** (withdrawn) Draft v0.

**SFT-258** Writer: clock and timing record
Checks: SFF-264, SFF-266, SFF-267, SFF-269, SFF-272
Input: writer output of a take with a test source that drops 2 known frames.
Pass: all files have the same `clock_id` from the table. Each camera file has a `freemocap.timing`
record with the keys of section 7. The segments meet SFF-267. The breakpoints are `[0, s0]` and one
for the drop. The player time never decreases.

**SFT-259** (provisional) Writer: Linux and macOS clocks
Checks: SFF-265
Pass: on Linux the writer writes `clock_id` 2 and on macOS `clock_id` 3, with the clocks of the table.

**SFT-260** Reader: fit evaluation and breakpoints, Python and JS
Checks: SFF-268, SFF-270, SFF-271, SFF-273
Input: G1 and G10, and G10 with only `fitter`, `fitter_version` and `fitter_params` changed.
Pass: each fitted time is equal to the committed value, computed with integers. The sequence of each
position, from the breakpoints alone, is equal to the `sequence` of its Message. The file with no
record uses `log_time` for every frame and reports `missing_fit`. The changed-fitter file gives the
same times.

**SFT-261** Reader: time zero
Checks: SFF-274
Input: G1.
Pass: at a time before the player time of position 0 of a camera, the reader shows no frame of that
camera. Times in the result are relative to `take_start_host_ns` where the result says so.

### skellysync files (section 8)

**SFT-300** (withdrawn) Draft v0.

**SFT-301** (withdrawn) Draft v0.

**SFT-302** (provisional) Writer: skellysync output
Checks: SFF-305, SFF-306, SFF-308, SFF-309
Input: G13.
Pass: skellysync writes one camera file per source video and one audio file. `clock_id` is 128, and
the times, the source description and the take start meet the provisional rules.

**SFT-303** Writer: skellysync rotation
Checks: SFF-307
Input: a source video with a rotation of 90.
Pass: the JPEG pixels are in the source orientation, and `display_rotation` is 90.

### Finished, unfinished and repaired files (section 9)

**SFT-350** (withdrawn) Draft v0.

**SFT-351** (withdrawn) Draft v0.

**SFT-352** (withdrawn) Draft v0.

**SFT-353** (withdrawn) Draft v0.

**SFT-354** (withdrawn) Draft v0.

**SFT-355** (withdrawn) Draft v0.

**SFT-356** (withdrawn) Draft v0.

**SFT-357** (withdrawn) Draft v0.

**SFT-358** (withdrawn) Draft v0.

**SFT-359** (withdrawn) Draft v0.

**SFT-360** (withdrawn) Draft v0.

**SFT-361** (withdrawn) Draft v0.

**SFT-362** (withdrawn) Draft v0.

**SFT-363** (withdrawn) Draft v0.

**SFT-364** Writer: a finished file
Checks: SFF-369
Pass: the MCAP checks pass. The Summary holds the records of SFF-369. The data section CRC is correct.

**SFT-365** (provisional) Writer: fsync while recording
Checks: SFF-370
Input: a recording of 10 s with a tracer of the file system calls.
Pass: the writer flushes the file to the disk at least once in each second.

**SFT-366** Writer: kill test
Checks: SFF-371, SFF-372, SFF-373
Input: 40 `TerminateProcess` kills of the camera writer and 40 of the audio writer at random times.
Pass: each killed file is unfinished. The reader reads an exact prefix of what the writer flushed,
with no CRC failure, and reports `torn_bytes`. The `freemocap.format` and `freemocap.recording`
records are readable.

**SFT-367** Reader: unfinished and damaged files, Python and JS
Checks: SFF-371, SFF-372, SFF-373
Input: G4.
Pass: the clean cut and the torn tail have the state `unfinished`, with the committed message counts
and `torn_bytes`. The file with a wrong Chunk CRC has the state `damaged` and stops before that
Chunk. Each reader reaches the last complete record.

**SFT-368** Writer: repair
Checks: SFF-374, SFF-375, SFF-376, SFF-377
Input: G4, and G5 with an interrupted repair.
Pass: the repair does nothing until the user agrees. After the repair, the MCAP checks pass, the bytes
before the cut are unchanged, the file has a `freemocap.timing` record (camera) and a
`freemocap.repair` record with the correct `cut_bytes`, and the data section CRC is 0. The repair of
the interrupted repair gives the same file. The reader reports the state `repaired`.

### Withdrawn sections (sections 10, 11, 12 and 14)

**SFT-400** (withdrawn) Draft v0.

**SFT-401** (withdrawn) Draft v0.

**SFT-402** (withdrawn) Draft v0.

**SFT-450** (withdrawn) Draft v0.

**SFT-451** (withdrawn) Draft v0.

**SFT-452** (withdrawn) Draft v0.

**SFT-453** (withdrawn) Draft v0.

**SFT-454** (withdrawn) Draft v0.

**SFT-455** (withdrawn) Draft v0.

**SFT-456** (withdrawn) Draft v0.

**SFT-500** (withdrawn) Draft v0.

**SFT-501** (withdrawn) Draft v0.

**SFT-502** (withdrawn) Draft v0.

**SFT-503** (withdrawn) Draft v0.

**SFT-504** (withdrawn) Draft v0.

### Files that are not in this format (section 13)

**SFT-550** (withdrawn) Draft v0.

**SFT-551** Reader: files that are not in this format, Python and JS
Checks: SFF-554, SFF-555, SFF-556, SFF-557
Input: G12, a folder with only G12, and G6 (unknown `major`).
Pass: non-MCAP files are ignored. The `ros2` file and the file with no `freemocap.format` record have
the state `not_in_format`. The unknown-`major` file has the state `unsupported_version`. The folder
with only G12 has `folder_state` = `legacy`.

### Withdrawn section 14

**SFT-600** (withdrawn) Draft v0.

**SFT-601** (withdrawn) Draft v0.

**SFT-602** (withdrawn) Draft v0.

### The recording as a whole (section 15)

**SFT-650** (withdrawn) Draft v0.

**SFT-651** (withdrawn) Draft v0.

**SFT-652** (withdrawn) Draft v0.

**SFT-653** (withdrawn) Draft v0.

**SFT-654** (withdrawn) Draft v0.

**SFT-655** (withdrawn) Draft v0.

**SFT-656** (withdrawn) Draft v0.

**SFT-657** (withdrawn) Draft v0.

**SFT-658** (withdrawn) Draft v0.

**SFT-659** (withdrawn) Draft v0.

**SFT-660** (withdrawn) Draft v0.

**SFT-661** (withdrawn) Draft v0.

**SFT-662** (withdrawn) Draft v0.

**SFT-663** Writer: recording facts
Checks: SFF-669, SFF-670, SFF-671, SFF-672, SFF-673
Input: writer output of a take of 4 cameras and audio.
Pass: each file has the keys of section 15 with the same values. `group_size` is 4. The take start
times were read before the first frame. No record holds an absolute path, a user name, a friendly
device name, a device path or a raw serial number (checked against a list of the test machine's
values). All files of the take, and no others, are in one folder.

**SFT-664** Reader: recording folders, Python and JS
Checks: SFF-674, SFF-675, SFF-676, SFF-677
Input: G11.
Pass: the results are equal to the committed results: one take, or two takes for the folder with two;
`incomplete_take` for the missing camera; the crashed take opens with its unfinished files;
`duplicate_label` with both files kept; `take_fact_mismatch` with the values of the first camera file.

**SFT-665** Reader: the reader result, Python and JS
Checks: SFF-678, SFF-679, SFF-680
Input: every golden file of Appendix A.
Pass: each result is valid JSON in the canonical form of RFC 8785, with the members of SFF-678. The
states follow the order of SFF-679. Each reason and warning is from the lists of SFF-680. The Python
and JS results are equal to the committed result, byte for byte.
