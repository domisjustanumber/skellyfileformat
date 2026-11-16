# skellyfileformat conformance tests

Status: **draft v2 (the whole take folder), for review at gate 1**, together with
[SPEC.md](SPEC.md). Gate 2 turns each test into a runnable test and makes the golden folders (SPEC.md
Appendix A). The tests of draft v0 and draft v1 stay in this file, marked withdrawn.

This list is normative. The license of the text is CC-BY-4.0 ([LICENSE](LICENSE)).

## How to read a test

- A test starts on a new line with its ID in bold, then its title.
- The next line starts with `Checks:` and gives the SFF IDs of the requirements that the test checks.
- An `Input:` line names the inputs, for example a golden folder (G1 to G17 of SPEC.md Appendix A).
  A `Pass:` line gives the pass criteria.
- A removed test keeps its line, with `(withdrawn)` after its ID.
- Each requirement of [SPEC.md](SPEC.md) that is not withdrawn has one or more tests.
  `tools/check_spec_traceability.py` checks the IDs and the links.
- The tests of draft v2 start at SFT-700 and are numbered in file order (SPEC.md section 2).
- **Writer** tests run a writer and check its output. **Reader** tests run a reader on the inputs. A
  test marked `(provisional)` waits for the same open item as the requirement that it checks.
- "Python and JS" means that the test runs for the scope `player` (SPEC.md SFF-892) with two
  readers: the Python reader with the scope `player`, and the JavaScript reader. Each gives the
  committed `player` result of the case (`<case>.player.json`, SPEC.md Appendix A), byte for byte.
  The Python reader with the scope `full` also runs the test. It gives the committed `full` result
  (`<case>.full.json`), byte for byte
  ([ADR-0JVZ](../decisions/entries/0JVZ-spec-v2-details-part-9.md) item 21).
- In this repository, "skellycam" in an Input line is the package writer `TakeWriter` with
  synthetic input. "The converter" is `TakeWriter` in a conversion. The repair is `repair_take`
  ([ADR-QH61](../decisions/entries/QH61-spec-v2-details-part-15.md) item 46).
- A test, or a Pass sentence, is **external** when it needs a run of freemocap, a run of the
  Blender addon, capture hardware or an answer of a user. Its mark is `(external: <program>)`.
  `<program>` names what the test needs: `freemocap`, `Blender addon`, `Blender`, `skellycam` (the
  capture program with a camera), `capture hardware` or `user`. Two names have a comma between
  them. The mark after a test ID applies to the whole test. The mark at the end of a Pass sentence
  applies only to that sentence. The repository of that program runs an external test or sentence.
  This repository does not.
- An external test can have a line that starts with `Golden part:`. The line gives what this
  repository runs of the test: each Pass sentence that a file of the named golden folder, or the
  package writer, can show. An external test with no such line has no golden part.
- A test whose only inputs are golden files is not external. Examples are SFT-746, SFT-748, SFT-750
  and SFT-753. The test makes the Parquet of the G12 vector of SFT-748 with the functions of the
  golden generator.

## Withdrawn tests

<details>
<summary>Withdrawn IDs SFT-001 to SFT-665</summary>

**SFT-001** (withdrawn) Draft v0.

**SFT-002** (withdrawn) Draft v0.

**SFT-003** (withdrawn) Draft v0.

**SFT-004** (withdrawn) Draft v0.

**SFT-005** (withdrawn) Draft v1.

**SFT-006** (withdrawn) Draft v1.

**SFT-007** (withdrawn) Draft v1.

**SFT-050** (withdrawn) Draft v0.

**SFT-051** (withdrawn) Draft v0.

**SFT-052** (withdrawn) Draft v0.

**SFT-053** (withdrawn) Draft v0.

**SFT-054** (withdrawn) Draft v0.

**SFT-055** (withdrawn) Draft v0.

**SFT-056** (withdrawn) Draft v0.

**SFT-057** (withdrawn) Draft v0.

**SFT-058** (withdrawn) Draft v1.

**SFT-059** (withdrawn) Draft v1.

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

**SFT-110** (withdrawn) Draft v1.

**SFT-111** (withdrawn) Draft v1.

**SFT-112** (withdrawn) Draft v1.

**SFT-113** (withdrawn) Draft v1.

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

**SFT-172** (withdrawn) Draft v1.

**SFT-173** (withdrawn) Draft v1.

**SFT-174** (withdrawn) Draft v1.

**SFT-175** (withdrawn) Draft v1.

**SFT-176** (withdrawn) Draft v1.

**SFT-177** (withdrawn) Draft v1.

**SFT-178** (withdrawn) Draft v1.

**SFT-200** (withdrawn) Draft v0.

**SFT-201** (withdrawn) Draft v0.

**SFT-202** (withdrawn) Draft v0.

**SFT-203** (withdrawn) Draft v0.

**SFT-204** (withdrawn) Draft v0.

**SFT-205** (withdrawn) Draft v0.

**SFT-206** (withdrawn) Draft v0.

**SFT-207** (withdrawn) Draft v0.

**SFT-208** (withdrawn) Draft v1.

**SFT-209** (withdrawn) Draft v1.

**SFT-210** (withdrawn) Draft v1.

**SFT-211** (withdrawn) Draft v1.

**SFT-212** (withdrawn) Draft v1.

**SFT-213** (withdrawn) Draft v1.

**SFT-250** (withdrawn) Draft v0.

**SFT-251** (withdrawn) Draft v0.

**SFT-252** (withdrawn) Draft v0.

**SFT-253** (withdrawn) Draft v0.

**SFT-254** (withdrawn) Draft v0.

**SFT-255** (withdrawn) Draft v0.

**SFT-256** (withdrawn) Draft v0.

**SFT-257** (withdrawn) Draft v0.

**SFT-258** (withdrawn) Draft v1.

**SFT-259** (withdrawn) Draft v1.

**SFT-260** (withdrawn) Draft v1.

**SFT-261** (withdrawn) Draft v1.

**SFT-300** (withdrawn) Draft v0.

**SFT-301** (withdrawn) Draft v0.

**SFT-302** (withdrawn) Draft v1.

**SFT-303** (withdrawn) Draft v1.

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

**SFT-364** (withdrawn) Draft v1.

**SFT-365** (withdrawn) Draft v1.

**SFT-366** (withdrawn) Draft v1.

**SFT-367** (withdrawn) Draft v1.

**SFT-368** (withdrawn) Draft v1.

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

**SFT-550** (withdrawn) Draft v0.

**SFT-551** (withdrawn) Draft v1.

**SFT-600** (withdrawn) Draft v0.

**SFT-601** (withdrawn) Draft v0.

**SFT-602** (withdrawn) Draft v0.

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

**SFT-663** (withdrawn) Draft v1.

**SFT-664** (withdrawn) Draft v1.

**SFT-665** (withdrawn) Draft v1.

</details>

## Tests

### Conventions and versioning (sections 2 and 3)

**SFT-700** Writer: text files, integers, JSON, IDs and CRCs
Checks: SFF-700, SFF-701, SFF-702, SFF-703, SFF-704, SFF-705
Input: the output of each writer on G1 and G3.
Pass: each CSV, JSON and TOML file is UTF-8 with no BOM and LF line ends. Each CSV integer has the
form of SFF-701. Each JSON file has one object, with the members in the order of its section, and
no member is an integer in a string. Each JSON number has the form of SFF-702, for example `30`
and `29.97`. Each `take_uuid` and `calibration_uuid` is 32 lowercase
hexadecimal characters of a UUID version 4. Each CRC is 8 lowercase hexadecimal characters. Each row
time is relative to the take start, and an absent time is an empty field.

**SFT-701** Reader: integer and value forms
Checks: SFF-701, SFF-748
Input: G11.
Pass: a sidecar with a leading zero or a `+` sign in an integer, or with a missing header key, is
`invalid` with the reason `bad_metadata` or `missing_metadata`. A sidecar with a row integer of 2^53
that is not a time is `invalid` with `bad_metadata`.

**SFT-702** Reader: 64-bit integers in JavaScript
Checks: SFF-706
Input: G1 with `take_start_host_ns` near 2^62; a copy of G1, changed at test time, in which
`arrival_ns` of one row of one video sidecar is 2^53, with a correct row CRC.
Pass: the JS reader gives the same times as the Python reader. A time difference of 2^53 ns or more
is reported as an error: the file of the changed sidecar is `invalid` with `bad_time`, in Python
and JS.

**SFT-703** Writer and reader: version fields and rules
Checks: SFF-707, SFF-708, SFF-709, SFF-710, SFF-711, SFF-712, SFF-714, SFF-891
Input: G10; the output of each writer, with an export and a BVH.
Pass: each file that SFF-707 names has `format_version` 2.0, a `format_prerelease` and a `writer`:
the manifest, each timing sidecar, both info JSONs, the calibration TOML, the Parquet descriptor and
the journal header. The export inventory and the BVH metadata JSON also have them (external:
freemocap, Blender addon). Before v2.0.0, `format_prerelease` is 1 in each file (SFF-710). No camera file and no audio file
holds one of these three fields. The version and the writer string of a device pair are those of its
timing sidecar. A file with an
unknown `major` is `unsupported_version`, not legacy. A folder file with an unknown `major` has the
state `unsupported_version` in `folder_files`. A file with a higher `minor` reads, and the
unknown key, column and member are ignored. In `higher_minor` of G10, the reader also ignores the
unknown key in `[metadata]` and in the camera table of the TOML, and the flag bit 7 (128) of the
row of the video sidecar. In `higher_minor_journal` of G10, the good record of the unknown type 200
counts in `records`, and the reader uses no value of it. The TOML and journal vectors are tests of
the scope `full` only. SFF-714 has no case in version 2.0, because each field has minor 0. The
first minor version that adds a field adds the vector. The Python and JS readers of this package
read a file with `format_prerelease` > 0 and give it the file warning `prerelease` (SFF-891). Each
file of each golden case has this warning. The only exception is the case `prerelease_0` of G10:
no file of it has the warning. No other file of SPEC.md section 18 holds one of the three fields
(external: freemocap, Blender addon).

**SFT-704** Reader: the writer string and container versions do not change the result
Checks: SFF-712, SFF-713
Input: two copies of G1 that differ only in `writer`, and a copy whose MKV `DocTypeVersion` differs.
Pass: the reader results are equal.

### The take folder and the manifest (sections 4 and 5)

**SFT-705** (external: freemocap) Writer: names and layout
Checks: SFF-715, SFF-716, SFF-719, SFF-720, SFF-722
Input: the output of skellycam and freemocap for G3; a writer run with two cameras whose keys have the
same first 6 characters; a converter run that writes a camera with `camera_key` 0; a `TakeWriter`
that gets a folder with a file of this format of another take.
Golden part: the names in G3, and the three runs of the package writer.
Pass: each file has the name and the place of section 4. `<rec>` obeys SFF-715. The labels are 6
hexadecimal characters, or 7 or 8 for the two cameras. The camera with `camera_key` 0 has the label
`cam<N>`, where N is its `group_position`. No `synchronized_videos_README.md` exists. The
`TakeWriter` that gets a folder with a file of another take refuses to start (SFF-719).

**SFT-706** Reader: a renamed take folder
Checks: SFF-717, SFF-718, SFF-824
Input: G8 (G3 in a folder with another name).
Pass: the reader result of the renamed folder is equal to that of G3, byte for byte: each `name`
and `path` of the result is relative to the take folder.
The reader opens no file by a glob pattern. The Parquet item is `present`: the reader checks
`recording_id` against `<rec>`, not against the name of the take folder.

**SFT-707** Reader: only the root and the media folder are scanned
Checks: SFF-721
Input: G3 with a camera file and its sidecar copied into `exports/`.
Pass: the copy is not in the result.

**SFT-708** Writer: the manifest
Checks: SFF-723, SFF-724, SFF-725, SFF-726, SFF-727, SFF-728
Input: a skellycam take with a forced camera gap; freemocap processing of it, with the file system
calls traced.
Pass: the manifest exists before the first frame, with `state` `recording`, and is complete and
valid at each moment of the take. After the take, `state` is `finished`, and `warnings` has
`camera_gap`. The test calls `add_warning` with `control_mismatch` and with `awb_not_settled`. The
manifest holds each with `source` `skellycam`, its `camera_key` and its `detail`. The detection of
the two conditions is not in this test (external: skellycam). After freemocap, each file of the
take is listed with its role and owner, the warnings
of skellycam remain, and `writer` is the freemocap string (external: freemocap). Each `sha256` of a `files` item is a
SHA-256 or null, as SFF-723 gives for its role. skellycam holds
`.processing.lock` while it reads, changes and writes the manifest. freemocap does the same, and
each keeps the members and
the items of the other (external: freemocap). `summary` has the members and the values of SFF-728: `exposure_us` for each camera, the
`audio` object, the sorted `warnings`, and a
`nominal_fps` and a `duration_s` with at most 3 decimal places. In the manifest with `state`
`recording`, each `duration_s`, `stored_px`, `gaps` and `filled` is null. `processing_runs` has
`{run_id, origin, recorded_at}` for each run (external: freemocap).

**SFT-709** Reader: the summary is not used
Checks: SFF-729, SFF-730
Input: G3 with a `summary` whose `display_rotation` and `nominal_fps` differ from the sidecars; G3
with a `summary` whose `gaps` differs from the `# end` line; G3 with a wrong `sha256` in a `files`
item.
Pass: the reader result uses the sidecar values and has the warning `summary_stale`, for the first
two inputs. The wrong `sha256` of the `files` item changes nothing in the result.

**SFT-710** Reader: a missing or wrong manifest
Checks: SFF-731, SFF-867, SFF-868
Input: G7; G1 with its manifest and its camera pairs deleted; the case `no_manifest` of G7, with
a file `other_info.json` in its root and a file in `exports/`, both added at test time; the case
`no_manifest` of G7 with one camera pair renamed at test time to another `<rec>`.
Pass: with no manifest, the result has `manifest` = `missing` and the warning `manifest_missing`.
`recording_name` is the `<rec>` of the camera sidecar names. The result has the same device pairs as
G3. Its `folder_files` are the root files of G3 that have an exact name of SFF-731: the capture
info JSON, the processing info JSON, the calibration TOML and the Parquet. The
file `other_info.json`, whose name only ends in a fixed suffix, is not in `folder_files`. The file
in `exports/` is not in the result, and the reader does not list that subfolder. The link checks
`calibration` and `camera_key` are `not_checked`. `hashes` and `files` have
only their Parquet parts, and they are `ok`. `rotation` has only its capture info part. Each link
check that compares no manifest value has the
same state as for G3. For the case `other_take_manifest`, the take has `manifest` = `invalid` and
the warning `manifest_missing`, and the
reader rebuilds the links in the same way. The manifest is not in `folder_files`. It is in
`other_files` as `invalid`, with the reason `take_fact_mismatch`, and the folder has the warning
`orphan_file`. For the copy
of G1, `recording_name` is the audio sidecar name without `.audio.csv`. For the case with the
renamed camera pair, the take has the warning `take_fact_mismatch`, and `recording_name` is the
`<rec>` of the video sidecar with the lowest `group_position`. The reader writes no file.

### Camera files (section 6)

**SFT-711** Writer: the camera file
Checks: SFF-732, SFF-733, SFF-735, SFF-736, SFF-737
Input: the output of skellycam for G1 and G4; a writer run with a nominal rate of 1001/1.
Pass: each camera file has one `V_MJPEG` track, one keyframe `SimpleBlock` for each frame and no
lacing. The timestamps are the index timestamps of SFF-736, and `DefaultDuration` is the frame
period. No rotation element and no EXIF orientation exists. The JPEG bytes have no APPn timing data.
The take folder holds no overlay file. FFmpeg (pinned) counts the frames of the
sidecar. Blender (pinned) counts the same number (external: Blender). The writer refuses the nominal rate of 1001/1.

**SFT-712** Writer: JPEG bytes
Checks: SFF-734
Input: a recording from an MJPEG camera (test hardware), and from a raw-frame source; a request for
H.264 capture.
Pass: the block payloads are the bytes that the camera sent (external: capture hardware). A raw source gives valid JPEG frames.
The writer refuses the request for H.264 capture.

**SFT-713** Reader: JPEG and block parsing
Checks: SFF-738, SFF-739
Input: a camera file with JPEGs with no JFIF, no DHT, trailing bytes and an EXIF orientation tag,
and blocks with track numbers of 1 and 2 bytes.
Pass: the reader finds each frame and returns its stored bytes: the bytes of its block payload. The
reader does not decode them. The test decodes each frame with PyAV (pinned). The reader gives no
rotation from the EXIF tag
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 8).

**SFT-714** Reader: an unfinished camera file
Checks: SFF-740, SFF-757
Input: G5.
Pass: the reader finds each complete frame from the CSV offsets, and the same frames by a walk. Row
k belongs to the k-th complete block. The reader uses no row after the last complete block and no
block after the last usable row. `rows` is the number of usable CSV rows, and `records` holds only
the usable frames. The
check of the CSV offsets is provisional: it waits for desk test DT5 (SFF-757). The check of the walk
does not wait.

### Timing sidecars (sections 7, 8 and 10)

**SFT-715** Writer: the common CSV rules
Checks: SFF-741, SFF-742, SFF-743, SFF-744, SFF-745
Input: the sidecars of G1 and G2.
Pass: each sidecar has the header keys, in order, then the column line, the rows with correct CRCs,
and an `# end` line last. No field is quoted. Each footer line has the form of SFF-745, with its
keys in the order of the spec and single spaces.

**SFT-716** Reader: strict reading
Checks: SFF-746, SFF-747
Input: G5.
Pass: the torn row counts in `torn_bytes`, and the file is `unfinished`. The row with a wrong CRC makes
the file `damaged` with `crc_mismatch`, and the read stops at it. `torn_bytes` of the `damaged`
sidecar does not count the row with the wrong CRC or the rows after it. A sidecar with no `# end` line is
`unfinished`. A copy of a finished sidecar of G1, cut at test time in the middle of its `# end`
line, is `unfinished`: the reader reads no data row after the first footer line, the complete
footer lines count in no member, the bytes of the torn footer line are in `torn_bytes`, and `fit`
is false.

**SFT-717** Writer: the video sidecar
Checks: SFF-749, SFF-752, SFF-754, SFF-755, SFF-756, SFF-758
Input: the output of skellycam for G1 and of the converter for an old recording; a skellycam run
with a forced failure of the JPEG encoder; a source that gives one source frame number two times.
Pass: the take keys are equal in each sidecar. `camera_key` is not 0 for skellycam. It is the hash
of the identity string of SFF-752, built from the `device` values of the capture info JSON. The rows
count from 0, and each camera file of the take has the same number of rows. The gap of G1 has the
flag `gap`. `gap` is 0 in the first row and next to an empty `source_frame_number`. The row after
the encoder failure has the flag `encode_skip`. The row with the equal source frame number has the
flag `repeat` and not the flag `gap`. The `# end` counts agree with the rows, and `encode_skips` is
the number of rows with the flag `encode_skip`. The converter writes
the old time as `arrival_ns`. The check that the writer writes 0 to the bit `filled` is provisional:
it waits for the slot assembly of the skellycam plan and desk tests DT4 and DT7 (SFF-756). The other
checks do not wait.

**SFT-718** Reader: rate, rotation and label values
Checks: SFF-750, SFF-751, SFF-753
Input: G11; G4.
Pass: the sidecars are `invalid` with `bad_rate`, `bad_rotation` and `bad_label`. For each camera of
G4, the stored frame that is rotated clockwise by `display_rotation` has the upright corner colours
of G4.

**SFT-719** Reader: rows against blocks
Checks: SFF-759
Input: a finished pair whose sidecar has one row more than the camera file has blocks.
Pass: the pair is `invalid` with `bad_metadata`.

**SFT-720** Writer: the audio file and its sidecar
Checks: SFF-760, SFF-761, SFF-762, SFF-764, SFF-767, SFF-768, SFF-769, SFF-770
Input: the output of skellycam for G1 and G2, with the write calls of the audio file traced.
Pass: the audio file has the boxes of SFF-760 and fragments of about 1 s. `dOps` has 1 or 2
channels, the encoder pre-skip and output gain 0. The bitrate is in the range of the settings. The
trace shows a flush after each packet that the muxer gives, and the file ends with an `mfra` box. The
sidecar rows are contiguous in `first_sample`, and the `# end` counts agree. No microphone name is in
the sidecar.

**SFT-721** Release check: the Opus encoder is libopus
Checks: SFF-763
Pass: the release check of the writer reports that its Opus encoder resolves to libopus.

**SFT-722** Writer: audio gaps
Checks: SFF-765, SFF-768
Input: a recording with a simulated drop of 4,800 samples; a recording with a simulated input
overflow.
Pass: the decoded stream holds 4,800 samples of silence at the drop, and the row has the flag
`silence`. The click times of the decoded stream equal the device sample indexes. The row of the
input overflow has the flag `overflow`.

**SFT-723** Reader: pre-skip and output gain
Checks: SFF-766
Input: G1.
Pass: `audio_details` of the Python reader gives the pre-skip of `dOps`. The reader does not
decode. The test decodes the audio with PyAV (pinned), drops the pre-skip samples and applies no
output gain. Decoded sample 0 is the first sample after the pre-skip. The click offsets equal the
source.

**SFT-724** (provisional) Reader: audio latency
Checks: SFF-771
Input: G1 with `audio_latency_ns` = 5,000,000.
Pass: the microphone time of each sample is its fitted time minus 5 ms.

### Clocks, the fit and reader timing (section 11)

**SFT-725** Writer and reader: the clock and the take start
Checks: SFF-772, SFF-773, SFF-774
Input: the output of skellycam on Windows; G11 with an unknown `clock`.
Pass: each file has `clock` `windows_qpc` and the same take start. No time-zone name is written. An
unknown `clock` is `invalid` with `bad_metadata`. The same checks on Linux and macOS, with the
`clock` values `linux_monotonic` and `macos_uptime_raw`, are provisional: they wait for the timing
tests T-S7 (SFF-773). The Windows checks do not wait.

**SFT-726** Writer: the fit
Checks: SFF-775, SFF-776, SFF-778
Input: the output of skellycam for G1.
Pass: each finished sidecar has one `# fit` line and segments that hold each position or row, in
order, with no gap or overlap. `fitter_params` is the last key of the `# fit` line.

**SFT-727** Reader: fit evaluation
Checks: SFF-777, SFF-779, SFF-780
Input: G12, and G12 with a different `fitter`.
Pass: the fitted times equal the committed values, in Python and JS. The result does not depend on
`fitter`.

**SFT-728** Reader: player time and the frame shown
Checks: SFF-781, SFF-782, SFF-783
Input: G1, G12 (a sidecar with no fit, and the two rows with equal fitted times) and G5.
Pass: the player time is the fitted time for G1 and for the G12 file with the two equal fitted
times. It is the arrival time, with `missing_fit`, for the G12 sidecar with no fit and for G5. It
never decreases. For the two rows of G12 with equal fitted times, the `records` hold the
two equal player times, and the times that the reader gives to freemocap differ by 1 ns. At each
test time t, the frame shown is the last frame with a player time
at or before t, and no frame is shown before position 0.

**SFT-729** Reader: audio mapping and length
Checks: SFF-784, SFF-785
Input: G1, and G5 (a killed audio file with no fit); a copy of the G5 audio sidecar, changed at
test time, in which one row between the first row and the last row has the flag `silence`, with a
correct row CRC.
Pass: the take time of each click is the time of the matching video flash to within 1 ms. With no
fit, the reader fits the rows and gives `missing_fit`, and `fit` of the item is false. The fit of
the reader is the one segment of
SFF-784: its `n0`, `t0_ns` and `period_fs`, from `audio_details` of the Python reader, equal the
committed values. `fitted_ns` of each audio record is the fitted time of its `first_sample` with
the fit that the reader uses: the fit lines for G1, and the fit of the reader for G5, in Python and
JS. For the copy with one row, each `fitted_ns` is null. A row with
the flag `silence` is a usable row for the fit: the copy with the flag `silence` gives the same
`rows` and the same fit as G5. For a copy
of the G5 audio sidecar with one row, the reader computes no fit and maps no sample to take time. No
audio is scheduled after the usable length: the smaller of the samples of the CSV rows and the
samples of the complete fragments minus the pre-skip.

### Writing, crashed files and repair (section 12)

**SFT-730** Writer: whole files and live files
Checks: SFF-786, SFF-787, SFF-788, SFF-789
Input: a kill of each writer at 50 points during a take and during freemocap processing.
Pass: each whole file is the old or the new version, or is absent, with at most a `.tmp`. Each live
file is a valid prefix. freemocap holds `.processing.lock` while it writes a folder file whole (an
info JSON, the calibration TOML, the Parquet or an export) (external: freemocap). Each
writer of the manifest holds it while it reads, changes and writes the manifest. skellycam holds it
for each whole-file write that it makes: the manifest and the capture info JSON. freemocap appends
to the journal without the lock, also while another program holds the lock (external: freemocap). The lock is the
file lock of the operating system on the empty file `.processing.lock`. After a kill, the lock file
that no process holds does not stop the next writer. The check
that a writer forces each live file to disk about once a second is provisional: it waits for the
measurement of the cost of fsync (SFF-788). The other checks do not wait.

**SFT-731** Reader: stray temporary files
Checks: SFF-790
Input: G5.
Pass: the `.tmp` manifest is not read, and it is in no list of the result. `folder_warnings` has
`stray_tmp` one time.

**SFT-732** Reader: unfinished files
Checks: SFF-791, SFF-792
Input: G5.
Pass: each unfinished file reads to its last complete record. `torn_bytes` of each pair is the sum
of SFF-791: the bytes of the last line of its sidecar when that line has no LF, plus the bytes of
its media file after the last complete block
or fragment when the last line of the sidecar is not an `# end` line. The torn audio fragment is
ignored. `torn_bytes` is 0 for each pair of G1 and for each pair of `repaired` of G6.

**SFT-733** Writer: repair
Checks: SFF-793, SFF-794, SFF-795, SFF-796, SFF-797, SFF-798
Input: G5; G6; a start-up of skellycam and of freemocap with G5, one time with a user who agrees
and one time with a user who does not agree.
Pass: the program asks the user the question of SFF-793 before it repairs, also at start-up
(external: user).
skellycam asks about a take that it recorded on its own (external: user). When freemocap runs, freemocap asks, and
the user gets one question for the take (external: freemocap, user). Before
the user agrees, and when the user does not agree, the SHA-256 of each file and the list of files do
not change (external: user). Before a call of `repair_take`, the reader reads the files of G5 in place. After the repair, each byte before the cut is
unchanged, each sidecar has a fit, a repair line and an `# end` line, and the reader reports
`repaired`. `state` of the manifest is `finished`, and no manifest has another value of `state`.
The repair writes the manifest after the media files and the sidecars, while it holds
`.processing.lock`. In the manifest, `writer` is the writer string of the program that did the
repair, the summary has the values of the repaired files, and `warnings` has `camera_gap` for a
repaired video sidecar with `gaps` more than 0. No other member changes. A copy of G5 with no
manifest gets no manifest from the repair. In `interrupted_repair` of G6, `state` of the manifest
is `recording`, and each sidecar is `unfinished`, with `fit` false and `missing_fit`, also when it
has fit lines and a `# repair` line.
The repair line has `cut_bytes`, `media_cut_bytes` and `repair_writer`, in this order.
The audio file is cut after its last complete fragment and is not remuxed. A repair of
the interrupted repair gives the same files, except for `cut_bytes` and `media_cut_bytes`. The check
of the repaired camera
file (each complete block is kept) is provisional: it waits for desk test DT-R1 (SFF-797). The checks
of the sidecars and the audio file do not wait.

**SFT-734** Reader: the reader changes nothing
Checks: SFF-799
Input: every golden folder.
Pass: the SHA-256 and the modification time of each file, and the list of files, are the same after
the read.

### Capture info, processing info and calibration (sections 13 to 15)

**SFT-735** Writer: the capture info JSON
Checks: SFF-800, SFF-801, SFF-802
Input: a skellycam take of 2 cameras, one with a user name, and a microphone, with the file system
calls traced.
Pass: the file exists at the take start and at its end, each time complete. skellycam holds
`.processing.lock` for each of the two writes. It has the members of
section 13, in order, and no member of the forbidden list. `camera_configs` is keyed by `camera_key`.
Each control name is from SFF-802, and `audio` names the microphone.

**SFT-736** Reader: camera configs by key
Checks: SFF-803
Input: G3 with the camera configs in another order and with `camera_label` values swapped.
Pass: each config is linked to the camera of its key.

**SFT-737** (external: freemocap) Writer: the processing info JSON
Checks: SFF-804, SFF-805
Input: freemocap processing of G1, then an export.
Golden part: G3.
Pass: the file has the members of section 14 and no member of the capture info JSON. `parquet_sha256`
is the hash of the Parquet after each write. `channel` of each `data` item is the `kind` of its
descriptor channel. `selected_run_id` is a key of `runs`. The file is rewritten after the export,
with the inventory in `export_inventories`.

**SFT-738** (external: freemocap) Writer: the calibration TOML
Checks: SFF-806, SFF-807, SFF-808, SFF-809
Golden part: G14.
Input: freemocap calibration of G14, with and without a ground-plane alignment; freemocap processing
with each of the two TOML files.
Pass: the file parses as TOML 1.0.0, with `[metadata]` first and one table for each camera, keyed by
label, in order of `index`. Each key of section 15 is present, with the alignment keys only when
`aligned` is true. Camera 0 has zero rotation and translation when not aligned. `world_orientation`
is the transpose of the rotation matrix. For each of the two TOML files, a point (X, Y, Z) that is
triangulated in the TOML world is the point (−Y, X, Z) of `calibrated_world`.

**SFT-739** (external: freemocap) Writer: calibration identity, copies and the library
Checks: SFF-810, SFF-811, SFF-812, SFF-813
Golden part: G14.
Input: G14; then a ground-plane alignment of the calibration; a kill during each TOML write.
Pass: the calibration take, the library and `last_successful_camera_calibration.toml` hold identical
bytes. The motion-capture take holds a byte-identical copy, and its manifest has the
`calibration_uuid` and the SHA-256. The alignment gives a new `calibration_uuid` and a new history
entry, and the copy of the old take does not change. After each kill, each TOML is complete.

**SFT-740** Reader: finding and linking the calibration
Checks: SFF-814, SFF-815
Input: G14; G9 (a calibration hash mismatch and a `calibration_uuid` mismatch); a take with a second
TOML in its root; G7 (the copy with no manifest).
Pass: the reader uses the TOML of the manifest and ignores the second TOML. A hash or ID mismatch is a
`mismatch` of the links. The camera tables are linked by `camera_key`, in order of `index`. With no
manifest, the reader uses `<rec>_camera_calibration.toml`.

### Blender outputs, annotated videos, exports and logs (section 18)

**SFT-741** (external: Blender addon) Writer: Blender outputs
Checks: SFF-847, SFF-848, SFF-849
Input: the Blender export of G3, with FBX and BVH, for run 0 and run 1; then a change of
`selected_run_id` from 0 to 1.
Pass: only the files of section 18.1 are written. No file of run 0 has a run number in its name:
`<rec>.blend` is the scene of run 0. Each file of run 1 has `run-1` in its name, at the place that
section 18.1 gives. `<route>` in each name is `parquet_segments` or `parquet_constraints`. The
export of run 1 changes no file of run 0. The change of `selected_run_id`
renames and replaces no file, and it does not change the Parquet. The scene has the objects and
properties of
SFF-848, and the video plane of a rotated camera is upright. A `<rec>.blend1` is not in the
reader result. The checks of the scene (its objects, its properties and the upright video plane) are
provisional: they wait for the freemocap work on the `.blend` scene contents (SFF-848). The checks of
the written files and of `<rec>.blend1` do not wait.

**SFT-742** (external: freemocap) Writer: annotated videos
Checks: SFF-850, SFF-851, SFF-852, SFF-853
Input: freemocap processing of G3 and G4.
Pass: each camera has `annotated_videos/<rec>.<label>.annotated.mp4` with as many frames as its
camera file, in the stored orientation, with the derivation comment. Frame k shows the 2D points of
frame k of the run. A `.partial.mp4` file is not in the reader result.

**SFT-743** (external: freemocap) Writer: exports
Checks: SFF-854, SFF-855, SFF-856, SFF-857, SFF-858, SFF-859
Input: an export of G3 with every format and data kind, for run 0 and run 1; then a change of
`selected_run_id` from 0 to 1.
Pass: each file has the path and the format of section 18.3. The prefix of each file of run 0 is
`<rec>`, and the prefix of each file of run 1 is `<rec>.run-1`. The export of run 1 changes no file of
run 0. The change of `selected_run_id` renames and replaces no file. The inventory has
`format_version`, `format_prerelease` and `writer`, `version` 5, and the `artifacts`, `snapshots`
and `csv` members of SFF-858, with `location` `exports` and a `format` of the list. A float32 value
`0.1` is written as
`0.1`. The arrays have the shape and the dtype of their channels, and load with pickles not allowed.
`frames.npy` is int32 and `timestamps.npy` is float64.
The inventory lists each file with its SHA-256 and is written last. An interrupted export leaves no
partial file outside `.staging-*`. A trace shows that the exporter holds `exports/.exports.lock`
from before its first write in `.staging-*` until after it writes the inventory (SFF-859). This
test has no golden part: G3 holds no export, and a golden export waits for the open-work item
"Complete section 18.3" ([ADR-PVG8](../decisions/entries/PVG8-spec-v2-details-part-10.md)
item 23).

**SFT-744** Reader: hidden export files
Checks: SFF-860
Input: G3 with `exports/.staging-1/` and `exports/.publication.json`. The test makes the two
hidden items at test time. It needs no export.
Pass: they are not in the reader result.

**SFT-745** (external: freemocap) Writer: logs
Checks: SFF-861
Input: a take after a freemocap run that writes a log.
Pass: each log is `logs/<program>.log`, UTF-8 with LF line ends.

### Tracking Parquet (section 16)

**SFT-746** Writer: schema, descriptor and encoding
Checks: SFF-816, SFF-817, SFF-818, SFF-820, SFF-821, SFF-823, SFF-825, SFF-824
Input: the Parquet of G3 and of G13.
Pass: the Arrow schema is the table of section 16. The `freemocap.recording` descriptor validates
against parts/parquet-descriptor.md (the structure and the writer rules of each model and of its
nested types), with `schema_version` 2, `take_uuid`, the format version and the
writer. `recording_id` is `<rec>`. The descriptor has no `selected_run_id`. The value columns use
`BYTE_STREAM_SPLIT` and no dictionary, and
the codec is ZSTD at level 3. Each row has its value in the column of its channel's `dtype`. No value
is NaN. Each row group holds one channel.

**SFT-747** Reader: other Parquet readers
Checks: SFF-819
Input: the Parquet of G3; a copy of it with the columns `frame_number` and `run_id` as int64.
Pass: pyarrow 26.0.0, polars 2.0.0, DuckDB 2.0.0 and hyparquet 1.25.6 with hyparquet-compressors
1.1.2 (pinned) read every value bit-exactly. The reader of this package reads the int64 copy. It
gives the same values as for the Parquet of G3, and it does not give the reason `bad_schema`.

**SFT-748** Writer: the row rules
Checks: SFF-822, SFF-827, SFF-828, SFF-831
Input: the Parquet of G3; a Parquet from G12 (the two rows with equal fitted times).
Pass: every row rule of parts/parquet-descriptor.md holds. `frame_number` of each camera row is the
position of its frame. The capture times equal the strict player times of the sidecars divided by
10^9: each is the float64 nearest to s / 10^9. The group time of each frame is the mean of the
strict camera times, rounded half up to the nanosecond: m = ⌊(2 × S + n) / (2 × n)⌋ ns, and the
group `timestamp_s` is the float64 nearest to m / 10^9 (SFF-828). The two frames of G12
have times that differ by 1 ns. A point that was not detected has null
`x` and `y` and `visibility` 0.

**SFT-749** Writer: 2D and 3D spaces
Checks: SFF-829, SFF-830
Input: G3 with a rotated camera (`display_rotation` 90); freemocap processing of one camera of G1.
Pass: the 2D points of the rotated camera are in stored-JPEG pixels, and its image reference has the
stored width and height. The 3D reference frame is `calibrated_world` with the Blender basis, in mm.
The take with one camera uses the reference frame `camera_plane`, in pixels (external: freemocap).

**SFT-750** Writer: camera sources and skeletons
Checks: SFF-826, SFF-832
Input: the Parquet of G3.
Pass: each camera source is `camera:<label>` with `camera_key`, `video_filename` and
`timing_filename`, and no nominal rate. Each of the two names is a file name with no folder, and
it names a file of the media folder. Each model has
`tracker_connections` whose names are in `tracker_keypoint_names`, and a `segment_topology`.
`segment_topology` has one item for each item of `skeleton.segments`, in that order, with `parent`
from `rest_pose.parents`, `proximal` = `frame.origin` and `distal` = `frame.primary_point`: landmark
names. A model
with no connection pair omits `tracker_connections`. No
`tracker_schema.json` exists.

**SFT-751** (external: freemocap) Writer: runs and realtime runs
Checks: SFF-833, SFF-834, SFF-844
Input: G13, then a posthoc run on it; a fold of G13 with unfinished timing sidecars (no fit), then a
repair of the sidecars, then freemocap opens the take; a take whose manifest has `state`
`recording`.
Golden part: G13.
Pass: the fold gives a run with `origin` `realtime`, a `coverage` object and no checkpoints. In
`coverage`, `frames_in_take` is `sample_count`, `frames_processed` is the number of frames with one
or more data records, `skips` is `{"no_record": frames_in_take − frames_processed}`,
`journal_crc_rejects` is `rejected_records` of the journal, and `clean_close` is true only when
the journal has a good end record. Each event has `time_ns`, `stage`, `parameter` and `value`. Each
event record of the journal is in `coverage.events` of the stage that it names, for each sensor
group, in journal order. `latency_ms` has the nearest-rank percentiles of `processed_ns` minus the
group time m of SFF-828: `p50` is latency ⌈0.5 × k⌉ and `p99` is latency ⌈0.99 × k⌉ of the k
latencies in increasing order, in milliseconds. Skipped
frames have null `x`, `y` and `visibility`. `timestamp_s` of each row of the realtime run and the
value of each of its `TIMESTAMPS` rows equal the player times that the timing sidecars give at the
time of the fold. With no fit, these are the arrival times. The posthoc run gets
a new `run_id`, and the realtime run is unchanged, byte for byte in its rows. After the repair,
freemocap opens the take, finds the `# repair` line and the new fit, and rewrites the times of the
realtime run: they equal the fitted times of the repaired sidecars. Only `timestamp_s` and the
values of the `TIMESTAMPS` rows of the realtime run differ: each other value of the run is unchanged.
With no agreement of the user to a repair (SFF-793), freemocap does not start the fold while
`state` is `recording`.

**SFT-752** Reader: the realtime warning
Checks: SFF-835
Input: G13.
Pass: the take has the warning `realtime_run` one time. The reader result holds the code and no
text and no counts.

**SFT-753** Writer: ChArUco observations
Checks: SFF-836
Input: G14 (the calibration take).
Pass: the Parquet of `calibration_take` has one run, with the `TIMESTAMPS` rows and the ChArUco
rows. The ChArUco corners are `OVERLAY_2D` rows of the source
`charuco_detector:<squares_x>x<squares_y>` of the board. Each name is `corner_<id>`, with the
OpenCV corner ID in decimal. No other file holds them.

**SFT-754** Reader: geometry against the TOML
Checks: SFF-837
Input: G3 with a TOML whose camera 0 is moved 10 mm; G3 with a TOML after a rigid change of the
world (an alignment); G3 with a TOML whose `fx` differs by 1e-3.
Pass: for the first and the third input, the run uses its stored geometry, and the take has the
warning `calibration_mismatch`. The rigid change of the world gives no `calibration_mismatch`.

**SFT-755** (external: freemocap) Writer: Parquet publication
Checks: SFF-838
Input: a freemocap run, with the file system calls traced.
Pass: the Parquet is written as a `.tmp` and replaced while `.processing.lock` is held, then the
processing info JSON, then the manifest.

### Realtime journal (section 17)

**SFT-756** (external: freemocap) Writer: journal records
Checks: SFF-839, SFF-840, SFF-841, SFF-842
Input: a realtime session of 60 s with the journal on.
Golden part: G13 (its good records).
Pass: the first record is the header. Each record has a correct magic, length and CRC, and no
padding: each data payload has 22 + 4 × n × k bytes. Each channel is
declared before its data, with the `dtype` `float32`. No channel has the kind `TIMESTAMPS`. Each
`frame_number` is a position of a multi-camera frame of the take. Missing values are NaN. Each result
kind of SFF-842 that the session
made is in the journal. The end record has `data_records` (the number of data records that the
writer wrote) and `clean_close`.

**SFT-757** Reader: damaged journals
Checks: SFF-843
Input: G13; G13 with a header that declares one channel with the `dtype` `float64`; G13 with a
header that declares one channel of the kind `TIMESTAMPS`; a copy of the
G13 journal with only good records and a torn tail; a copy with only good records and no end record.
Pass: the reader skips the record with a wrong CRC, finds the next record after the zero hole and
stops at the torn tail. The `folder_files` item of the journal has the three members of the committed
result: `records`, `rejected_records` and `torn_bytes`. They follow the scan of SFF-843: `records`
counts the good records of each type; `torn_bytes` is the number of bytes from the `magic` of the
torn tail to the end of the file; and a rejected record after the start of the torn tail does not
count. The zero hole is not a rejected record. A copy of the G13 journal, changed at test time,
with a cut record before a good record has that record in `rejected_records`. A copy that ends with
the first 2 bytes of `magic` and has no torn tail has `torn_bytes` 2. This is a test of the scope
`full` only. The
state is `damaged`, with the
reason `crc_mismatch`. Each of the two copies is `unfinished`. The journal with the `float64`
channel and the journal with the `TIMESTAMPS` channel are `invalid` with the reason `bad_schema`.

**SFT-758** (external: freemocap, user) Writer: the journal after the fold
Checks: SFF-793, SFF-845
Input: G13; G13 with a forced failure of the read-back check; an unfinished take (a manifest with
`state` `recording`) with a left-over journal, at the start-up of freemocap, one time with a user
who agrees and one time with a user who does not agree; a take whose manifest has `state`
`finished`, with a left-over journal with no end record, one time for each answer.
Golden part: G13 (the count and the digest of the check).
Pass: the journal is deleted only after a fold whose check passes. The count and the digest of the
check equal the values that the test computes from the G13 journal with the rule of SFF-845. After
the forced failure, the journal is
kept. At start-up, freemocap does not fold the left-over journal automatically. It asks the
question of SFF-793. Before the user agrees, and when the user does not agree, no file of the take
changes. When the user agrees, freemocap folds the journal as part of the repair. freemocap asks
one time for the whole take: one question for the media files and the journal together. For the
take with `state` `finished`, freemocap asks the question of SFF-793 before it folds the journal,
and it folds only when the user agrees.

**SFT-759** (provisional) Load and kill tests of the journal
Checks: SFF-846
Pass: the aggregator latency and the dropped frames do not change by more than the agreed limit with
the journal on. The kill test DT11 recovers each complete record.

### skellysync folders (section 19)

**SFT-760** (provisional) Writer and reader: a skellysync folder
Checks: SFF-862, SFF-863
Input: G17.
Pass: the folder holds device pairs with `clock` `synthetic` and a manifest. The reader gives no
`missing_fit`.

### Opening a folder (section 20)

**SFT-761** Reader: device pairs and orphan files
Checks: SFF-864, SFF-865
Input: G3 with an extra `.mkv` with no sidecar, and a sidecar of the take with no media file; G3
with a sidecar of another `take_uuid` with no media file.
Pass: the extra `.mkv` is in `other_files` as `not_in_format`. The sidecar of the take is in the
`files` of the take as `invalid`, with the reason `missing_media` and the path of the missing media
file as its `name`. It gives no `extra_files`. The sidecar of the other `take_uuid` is in
`other_files`, with the same state and reason. Its `name` there is the path of the sidecar. `folder_warnings` has `orphan_file` one time.

**SFT-762** Reader: takes and counts
Checks: SFF-866, SFF-869, SFF-870, SFF-871
Input: G9; a folder with two takes; G3 with a camera missing; G3 with a third camera pair of the same
take; G3 with two cameras that have one label;
G3 with sidecars that disagree on `clock`.
Pass: each take is reported. Two takes give `multiple_takes`. The missing camera gives `incomplete` and
`incomplete_take`. The third camera pair gives `extra_files`. One label gives `duplicate_label`. The
disagreement gives `take_fact_mismatch`,
and the values of `group_position` 0 are used.

**SFT-763** Reader: link checks
Checks: SFF-720, SFF-824, SFF-872, SFF-873, SFF-874
Input: G3; G9; G3 with one `camera_key` 0; G5; G6.
Pass: G3 has each link `ok`. `links` holds each check one time, in the order of the table of
SFF-872, with `detail` null. Each vector of G9 gives `mismatch` in its check, and the stale
`parquet_sha256` gives `stale_processing_info`. The camera files with different numbers of rows give
`mismatch` in `frames`. The row-count part of `frames` compares only the camera files with the
state `finished`, when the take has two or more of them: for G5 and G6, the reader does not
evaluate it. The check `files` tests each file name of a Parquet camera source in the media
folder. The Parquet with a wrong `recording_id` is `invalid` in `folder_files`, with
`take_fact_mismatch`. A part whose file is absent or `invalid` is not evaluated. The key 0 camera
has the label `cam<N>` and is linked by label, with
`camera_key_zero`.

### Legacy folders (section 21)

**SFT-764** Reader: legacy recognition
Checks: SFF-875, SFF-876, SFF-877, SFF-878, SFF-879
Input: G15.
Pass: each folder has `folder_state` `legacy`, and the family, the release range, `ambiguous`,
`eras` and the
warnings of the committed result. A folder whose matched rows are in one chain has the range of its
last matched row, and
`ambiguous` false. The folder with signals in two chains, and the folder with no era signal, have
`ambiguous` true. The case `v1i` matches only the row V1i, and `ambiguous` is false. The cases
`v1g_v1h` and later match their TOML signals only when the calibration lookup of SFF-880 gives the
state `present`. The pre-v1 folders have the family `pre_v1`, with `release_range` null,
`ambiguous` false and empty `eras` and `warnings`. The result holds no note text. The folder of MP4
files only has the
family `unknown`, with `release_range` null, `ambiguous` false and empty `eras` and `warnings`.
`legacy.calibration` is null for `pre_v1` and for `unknown`. In each legacy folder, `takes` is
`[]`, and `other_files` lists each file of the root and of `synchronized_videos/`, not of their
subfolders.

**SFT-765** Reader: calibration lookup in v1 folders
Checks: SFF-880
Input: v1 folders with an exact TOML name, one TOML with `calibration` in its name, two such TOMLs,
and no TOML.
Pass: `legacy.calibration` has the state `present` and the path of the TOML in the first two cases,
`ambiguous` in the third and `missing` in the fourth. `path` is null in the last two cases.

### Privacy and safety (section 22)

**SFT-766** Writer and reader: the privacy list
Checks: SFF-881, SFF-882, SFF-883
Input: G3 with a user camera name and a device serial; G7; G1 with its camera pairs deleted.
Pass: the manifest `privacy` list has exactly the fields of the table of SFF-881 that exist and are
not null, sorted, and `media_shows_people`
true. The reader result has `may_contain_private_data` true, also with no manifest, and also for the
take with only an audio file.

**SFT-767** Reader: no code in files
Checks: SFF-884
Input: G16; copies of G16, changed at test time, with these files in the manifest: an NPZ file
with one member with an object `descr` and one other member that is not an NPY file; a file with
the suffix `.npz` that is not a ZIP file; an NPZ file with a `.npy` member with no NPY header; an
NPY file with no NPY header.
Pass: the reader does not load the pickle or the object array. The pickle is in `other_files` as
`invalid` with `code_in_file`. The reader reads only the header of the NPY, and its `folder_files`
item is `invalid` with
`code_in_file`. For an NPZ file, the reader reads the ZIP directory and only the NPY header of each
member whose name ends in `.npy`. The NPZ file with the object `descr` is `invalid` with
`code_in_file`. The file that is not a ZIP file, the NPZ file with the member with no NPY header
and the NPY file with no NPY header are `invalid` with `bad_schema`. The checks of the NPY and NPZ
files are tests of the scope `full` only: for the scope `player`, each of these items is
`not_checked`. No code from the files runs (a canary file is not created).

### The reader result (section 23)

**SFT-768** Reader: the reader result, Python and JS
Checks: SFF-756, SFF-853, SFF-885, SFF-886, SFF-887, SFF-888, SFF-889, SFF-890
Input: every case of every golden folder of Appendix A; an empty folder; a folder with only one
timing sidecar of G1; a folder with only the capture info JSON of G3; a copy of G3, changed at test
time, with an empty file (0 bytes) at the path of an annotated video and its manifest item.
Pass: each result is valid JSON in the canonical form of RFC 8785, with each member of SFF-885.
The states follow the order of SFF-886, and each code is from SFF-887. The sort orders are
those of SFF-890. Each `name` and `path` is relative to the take folder, with `/`. A code is at most
one time in each `warnings` array. The file of G12 with the flag `encode_skip` in a usable row has
the file warning `encode_skip`. The empty folder has `folder_state` `empty`. The folder with one
timing sidecar has `folder_state` `unreadable`, the sidecar in `other_files` as `invalid` with
`missing_media`, its own path as its `name`, and the folder warning `orphan_file`. The folder with
only the capture info JSON is `unreadable`: the file is in `other_files` as `invalid`, with
`take_fact_mismatch`, and the folder has `orphan_file` (SFF-889). In the copy of G3 with the empty
annotated video, the item of that file is `present`, and the other members of the result do not
change: the reader reads no tracking data from an annotated video (SFF-853). For each case, the
Python reader with the scope `full` gives the bytes of `<case>.full.json`. The Python reader with
the scope `player` gives the bytes of `<case>.player.json`. The JS reader gives the bytes of
`<case>.player.json`. Each comparison is byte for byte (SFF-892).

**SFT-769** Reader: the scope `player`, Python and JS
Checks: SFF-892
Input: G3; G9; G13; G16; a `v1` case of G15; a folder with only the Parquet of G3.
Pass: the Python reader with the scope `player` and the JS reader give the same bytes for each
input: the committed `player` result. The JS command writes the canonical JSON to standard output,
and no other byte, with and without `--records`. In the `player` result, each item of a TOML, a
Parquet, a journal, an NPY file or an NPZ file that exists is `not_checked`, with `reason` null and
`warnings` `[]`, and the three integer members of the journal item are null. A `missing` item stays
`missing`. The link checks `frames`, `dimensions`, `hashes` and `calibration` are `not_checked`.
The checks `take_uuid`, `camera_key`, `rotation` and `files` have only the parts that need no TOML,
Parquet or journal. The take warnings `stale_processing_info`, `calibration_mismatch` and
`realtime_run` are absent. The Parquet alone is `not_in_format` in `other_files`, with no
`orphan_file`. For the `v1` case, `family` and `calibration` are those of the `full` result,
`release_range` is `["v1.0.25","v1.8.2"]`, `ambiguous` is true, `eras` is `[]`, and `warnings` has
the four warnings of SFF-879. Each other member of the `player` result equals the `full` result. A
vector of G9 that is only in the TOML, the Parquet or the journal is a test of the scope `full`
only.

### Tracking Parquet: the reader and the models (section 16)

**SFT-770** Reader: the structure of a model in the descriptor
Checks: SFF-893
Input: four copies of the Parquet of G3. The test makes them at test time, with a changed
descriptor: one with a missing member of a model; one with a member of a wrong JSON type; one with
an unknown member in a closed type; and one that breaks only a writer rule, for example a joint
whose `child` names no segment. A fifth copy has `1.0` for an integer member and `0` for a value
of a `position`.
Pass: this is a test of the scope `full` only (SFF-892). For each of the first three copies, the
`folder_files` item of the Parquet is `invalid`, with the reason `bad_schema`. The reader does not
refuse the fourth copy: its item is `present`, as for G3. The fifth copy is also `present`: an
"integer" is a JSON number with no fraction in its value, and a "float" is each JSON number.
