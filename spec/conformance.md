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
- "Python and JS" means that the Python reader and the JavaScript reader both run the test and give
  the same reader result (SPEC.md section 23), byte for byte, for the parts that the JS reader reads.

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
each integer outside ±2^53 is a string. Each `take_uuid` and `calibration_uuid` is 32 lowercase
hexadecimal characters of a UUID version 4. Each CRC is 8 lowercase hexadecimal characters. Each row
time is relative to the take start, and an absent time is an empty field.

**SFT-701** Reader: integer and value forms
Checks: SFF-701, SFF-748
Input: G11.
Pass: a sidecar with a leading zero or a `+` sign in an integer, or with a missing header key, is
`invalid` with the reason `bad_metadata` or `missing_metadata`.

**SFT-702** Reader: 64-bit integers in JavaScript
Checks: SFF-706
Input: G1 with `take_start_host_ns` near 2^62.
Pass: the JS reader gives the same times as the Python reader. A time difference of 2^53 ns or more
is reported as an error.

**SFT-703** Writer and reader: version fields and rules
Checks: SFF-707, SFF-708, SFF-709, SFF-710, SFF-711, SFF-712, SFF-714
Input: G10; the output of each writer, with an export and a BVH.
Pass: each file that SFF-707 names has `format_version` 2.0, a `format_prerelease` and a `writer`:
the manifest, each timing sidecar, both info JSONs, the calibration TOML, the Parquet descriptor, the
journal header, the export inventory and the BVH metadata JSON. No camera file and no audio file
holds one of these three fields. The version and the writer string of a device pair are those of its
timing sidecar. A file with an
unknown `major` is `unsupported_version`, not legacy. A folder file with an unknown `major` has the
state `unsupported_version` in `folder_files`. A file with a higher `minor` reads, and the
unknown key, column and member are ignored. A file with `format_prerelease` > 0 reads with the
warning `prerelease`.

**SFT-704** Reader: the writer string and container versions do not change the result
Checks: SFF-712, SFF-713
Input: two copies of G1 that differ only in `writer`, and a copy whose MKV `DocTypeVersion` differs.
Pass: the reader results are equal.

### The take folder and the manifest (sections 4 and 5)

**SFT-705** Writer: names and layout
Checks: SFF-715, SFF-716, SFF-719, SFF-720, SFF-722
Input: the output of skellycam and freemocap for G3; a writer run with two cameras whose keys have the
same first 6 characters.
Pass: each file has the name and the place of section 4. `<rec>` obeys SFF-715. The labels are 6
hexadecimal characters, or 7 or 8 for the two cameras. No `synchronized_videos_README.md` exists.

**SFT-706** Reader: a renamed take folder
Checks: SFF-717, SFF-718
Input: G8.
Pass: the reader result of the renamed folder is equal to that of the original, except for the path.
The reader opens no file by a glob pattern.

**SFT-707** Reader: only the root and the media folder are scanned
Checks: SFF-721
Input: G3 with a camera file and its sidecar copied into `exports/`.
Pass: the copy is not in the result.

**SFT-708** Writer: the manifest
Checks: SFF-723, SFF-724, SFF-725, SFF-726, SFF-727, SFF-728
Input: a skellycam take with a forced camera gap; freemocap processing of it.
Pass: the manifest exists before the first frame, with `state` `recording`, and is complete and
valid at each moment of the take. After the take, `state` is `finished`, and `warnings` has
`camera_gap`. After freemocap, each file of the take is listed with its role and owner, the warnings
of skellycam remain, and `writer` is the freemocap string. `summary` has the members of
SFF-728.

**SFT-709** Reader: the summary is not used
Checks: SFF-729, SFF-730
Input: G3 with a `summary` whose `display_rotation` and `nominal_fps` differ from the sidecars.
Pass: the reader result uses the sidecar values and has the warning `summary_stale`.

**SFT-710** Reader: a missing or wrong manifest
Checks: SFF-731, SFF-867, SFF-868
Input: G7; G1 with its manifest and its camera pairs deleted.
Pass: with no manifest, the result has `manifest` = `missing` and the warning `manifest_missing`.
`recording_name` is the `<rec>` of the camera sidecar names. The result has the same device pairs as
G3. Its `folder_files` are the root files of G3 that have a fixed suffix of SFF-731: the capture
info JSON, the processing info JSON, the calibration TOML and the Parquet. The files of G3 in
`annotated_videos/`, `exports/`, `blender/` and `logs/` are not in the result, and the reader lists
none of these subfolders. Each link check that compares no manifest value has the same state as for
G3. With a manifest of another take, the manifest is `invalid` (`take_fact_mismatch`), and the
reader rebuilds the links in the same way. For the copy
of G1, `recording_name` is the audio sidecar name without `.audio.csv`. The reader writes no file.

### Camera files (section 6)

**SFT-711** Writer: the camera file
Checks: SFF-732, SFF-733, SFF-735, SFF-736, SFF-737
Input: the output of skellycam for G1 and G4.
Pass: each camera file has one `V_MJPEG` track, one keyframe `SimpleBlock` for each frame and no
lacing. The timestamps are the index timestamps of SFF-736, and `DefaultDuration` is the frame
period. No rotation element and no EXIF orientation exists. The JPEG bytes have no APPn timing data.
FFmpeg (pinned) and Blender (pinned) count the frames of the sidecar.

**SFT-712** Writer: JPEG bytes
Checks: SFF-734
Input: a recording from an MJPEG camera (test hardware), and from a raw-frame source.
Pass: the block payloads are the bytes that the camera sent. A raw source gives valid JPEG frames.

**SFT-713** Reader: JPEG and block parsing
Checks: SFF-738, SFF-739
Input: a camera file with JPEGs with no JFIF, no DHT, trailing bytes and an EXIF orientation tag,
and blocks with track numbers of 1 and 2 bytes.
Pass: the reader decodes each frame and ignores the EXIF tag.

**SFT-714** Reader: an unfinished camera file
Checks: SFF-740, SFF-757
Input: G5.
Pass: the reader finds each complete frame from the CSV offsets, and the same frames by a walk. The
check of the CSV offsets is provisional: it waits for desk test DT5 (SFF-757). The check of the walk
does not wait.

### Timing sidecars (sections 7, 8 and 10)

**SFT-715** Writer: the common CSV rules
Checks: SFF-741, SFF-742, SFF-743, SFF-744, SFF-745
Input: the sidecars of G1 and G2.
Pass: each sidecar has the header keys, in order, then the column line, the rows with correct CRCs,
and an `# end` line last. No field is quoted.

**SFT-716** Reader: strict reading
Checks: SFF-746, SFF-747
Input: G5.
Pass: the torn row counts in `torn_bytes`, and the file is `unfinished`. The row with a wrong CRC makes
the file `damaged` with `crc_mismatch`, and the read stops at it. A sidecar with no `# end` line is
`unfinished`.

**SFT-717** Writer: the video sidecar
Checks: SFF-749, SFF-752, SFF-754, SFF-755, SFF-756, SFF-758
Input: the output of skellycam for G1 and of the converter for an old recording.
Pass: the take keys are equal in each sidecar. `camera_key` is not 0 for skellycam. The rows count
from 0. The gap of G1 has the flag `gap`. The `# end` counts agree with the rows. The converter writes
the old time as `arrival_ns`.

**SFT-718** Reader: rate, rotation and label values
Checks: SFF-750, SFF-751, SFF-753
Input: G11.
Pass: the sidecars are `invalid` with `bad_rate`, `bad_rotation` and `bad_label`.

**SFT-719** Reader: rows against blocks
Checks: SFF-759
Input: a finished pair whose sidecar has one row more than the camera file has blocks.
Pass: the pair is `invalid` with `bad_metadata`.

**SFT-720** Writer: the audio file and its sidecar
Checks: SFF-760, SFF-761, SFF-762, SFF-764, SFF-767, SFF-768, SFF-769, SFF-770
Input: the output of skellycam for G1 and G2.
Pass: the audio file has the boxes of SFF-760 and fragments of about 1 s. `dOps` has 1 or 2
channels, the encoder pre-skip and output gain 0. The bitrate is in the range of the settings. The
sidecar rows are contiguous in `first_sample`, and the `# end` counts agree. No microphone name is in
the sidecar.

**SFT-721** Release check: the Opus encoder is libopus
Checks: SFF-763
Pass: the release check of the writer reports that its Opus encoder resolves to libopus.

**SFT-722** Writer: audio gaps
Checks: SFF-765
Input: a recording with a simulated drop of 4,800 samples.
Pass: the decoded stream holds 4,800 samples of silence at the drop, and the row has the flag
`silence`. The click times of the decoded stream equal the device sample indexes.

**SFT-723** Reader: pre-skip and output gain
Checks: SFF-766
Input: G1.
Pass: decoded sample 0 is the first sample after the pre-skip. The click offsets equal the source.

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
order, with no gap or overlap.

**SFT-727** Reader: fit evaluation
Checks: SFF-777, SFF-779, SFF-780
Input: G12, and G12 with a different `fitter`.
Pass: the fitted times equal the committed values, in Python and JS. The result does not depend on
`fitter`.

**SFT-728** Reader: player time and the frame shown
Checks: SFF-781, SFF-782, SFF-783
Input: G1, G12 (a sidecar with no fit) and G5.
Pass: the player time is the fitted time for G1, and the arrival time with `missing_fit` for the
others. It never decreases. At each test time t, the frame shown is the last frame with a player time
at or before t, and no frame is shown before position 0.

**SFT-729** Reader: audio mapping and length
Checks: SFF-784, SFF-785
Input: G1, and G5 (a killed audio file with no fit).
Pass: the take time of each click is the time of the matching video flash to within 1 ms. With no
fit, the reader fits the rows and gives `missing_fit`. The fit of the reader is the one segment of
SFF-784: its `n0`, `t0_ns` and `period_fs` equal the committed values, in Python and JS. For a copy
of the G5 audio sidecar with one row, the reader computes no fit and maps no sample to take time. No
audio is scheduled after the usable length.

### Writing, crashed files and repair (section 12)

**SFT-730** Writer: whole files and live files
Checks: SFF-786, SFF-787, SFF-788, SFF-789
Input: a kill of each writer at 50 points during a take and during freemocap processing.
Pass: each whole file is the old or the new version, or is absent, with at most a `.tmp`. Each live
file is a valid prefix. freemocap holds `.processing.lock` while it changes a folder file. The check
that a writer forces each live file to disk about once a second is provisional: it waits for the
measurement of the cost of fsync (SFF-788). The other checks do not wait.

**SFT-731** Reader: stray temporary files
Checks: SFF-790
Input: G5.
Pass: the `.tmp` manifest is not read, and the take has the warning `stray_tmp`.

**SFT-732** Reader: unfinished files
Checks: SFF-791, SFF-792
Input: G5.
Pass: each unfinished file reads to its last complete record. `torn_bytes` is the bytes after it. The
torn audio fragment is ignored.

**SFT-733** Writer: repair
Checks: SFF-793, SFF-794, SFF-795, SFF-796, SFF-797, SFF-798
Input: G5; G6.
Pass: the program asks the user before it repairs. After the repair, each byte before the cut is
unchanged, each sidecar has a fit, a repair line and an `# end` line, and the reader reports
`repaired`. The audio file is cut after its last complete fragment and is not remuxed. A repair of
the interrupted repair gives the same files, except for `cut_bytes`. The check of the repaired camera
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
Input: a skellycam take of 2 cameras, one with a user name, and a microphone.
Pass: the file exists at the take start and at its end, each time complete. It has the members of
section 13, in order, and no member of the forbidden list. `camera_configs` is keyed by `camera_key`.
Each control name is from SFF-802, and `audio` names the microphone.

**SFT-736** Reader: camera configs by key
Checks: SFF-803
Input: G3 with the camera configs in another order and with `camera_label` values swapped.
Pass: each config is linked to the camera of its key.

**SFT-737** Writer: the processing info JSON
Checks: SFF-804, SFF-805
Input: freemocap processing of G1, then an export.
Pass: the file has the members of section 14 and no member of the capture info JSON. `parquet_sha256`
is the hash of the Parquet after each write. It is rewritten after the export, with the inventory in
`export_inventories`.

**SFT-738** Writer: the calibration TOML
Checks: SFF-806, SFF-807, SFF-808, SFF-809
Input: freemocap calibration of G14, with and without a ground-plane alignment.
Pass: the file parses as TOML 1.0.0, with `[metadata]` first and one table for each camera, keyed by
label, in order of `index`. Each key of section 15 is present, with the alignment keys only when
`aligned` is true. Camera 0 has zero rotation and translation when not aligned. `world_orientation`
is the transpose of the rotation matrix.

**SFT-739** Writer: calibration identity, copies and the library
Checks: SFF-810, SFF-811, SFF-812, SFF-813
Input: G14; then a ground-plane alignment of the calibration; a kill during each TOML write.
Pass: the calibration take, the library and `last_successful_camera_calibration.toml` hold identical
bytes. The motion-capture take holds a byte-identical copy, and its manifest has the
`calibration_uuid` and the SHA-256. The alignment gives a new `calibration_uuid` and a new history
entry, and the copy of the old take does not change. After each kill, each TOML is complete.

**SFT-740** Reader: finding and linking the calibration
Checks: SFF-814, SFF-815
Input: G14; G9 (a calibration hash mismatch and a `calibration_uuid` mismatch); a take with a second
TOML in its root.
Pass: the reader uses the TOML of the manifest and ignores the second TOML. A hash or ID mismatch is a
`mismatch` of the links. The camera tables are linked by `camera_key`, in order of `index`.

### Blender outputs, annotated videos, exports and logs (section 18)

**SFT-741** Writer: Blender outputs
Checks: SFF-847, SFF-848, SFF-849
Input: the Blender export of G3, with FBX and BVH, for run 0 and run 1; then a change of
`selected_run_id` from 0 to 1.
Pass: only the files of section 18.1 are written. No file of run 0 has a run number in its name:
`<rec>.blend` is the scene of run 0. Each file of run 1 has `run-1` in its name, at the place that
section 18.1 gives. The export of run 1 changes no file of run 0. The change of `selected_run_id`
renames and replaces no file. The scene has the objects and properties of
SFF-848, and the video plane of a rotated camera is upright. A `<rec>.blend1` is not in the
reader result. The checks of the scene (its objects, its properties and the upright video plane) are
provisional: they wait for the freemocap work on the `.blend` scene contents (SFF-848). The checks of
the written files and of `<rec>.blend1` do not wait.

**SFT-742** Writer: annotated videos
Checks: SFF-850, SFF-851, SFF-852, SFF-853
Input: freemocap processing of G3 and G4.
Pass: each camera has `annotated_videos/<rec>.<label>.annotated.mp4` with as many frames as its
camera file, in the stored orientation, with the derivation comment. Frame k shows the 2D points of
frame k of the run. A `.partial.mp4` file is not in the reader result.

**SFT-743** Writer: exports
Checks: SFF-854, SFF-855, SFF-856, SFF-857, SFF-858, SFF-859
Input: an export of G3 with every format and data kind, for run 0 and run 1; then a change of
`selected_run_id` from 0 to 1.
Pass: each file has the path and the format of section 18.3. The prefix of each file of run 0 is
`<rec>`, and the prefix of each file of run 1 is `<rec>.run-1`. The export of run 1 changes no file of
run 0. The change of `selected_run_id` renames and replaces no file. The inventory has
`format_version`, `format_prerelease` and `writer`. A float32 value `0.1` is written as
`0.1`. The arrays have the shape and the dtype of their channels, and load with pickles not allowed.
`frames.npy` is int32 and `timestamps.npy` is float64.
The inventory lists each file with its SHA-256 and is written last. An interrupted export leaves no
partial file outside `.staging-*`.

**SFT-744** Reader: hidden export files
Checks: SFF-860
Input: G3 with `exports/.staging-1/` and `exports/.publication.json`.
Pass: they are not in the reader result.

**SFT-745** Writer: logs
Checks: SFF-861
Input: a take after a freemocap run that writes a log.
Pass: each log is `logs/<program>.log`, UTF-8 with LF line ends.

### Tracking Parquet (section 16)

**SFT-746** Writer: schema, descriptor and encoding
Checks: SFF-816, SFF-817, SFF-818, SFF-820, SFF-821, SFF-823, SFF-825, SFF-824
Input: the Parquet of G3 and of G13.
Pass: the Arrow schema is the table of section 16. The `freemocap.recording` descriptor validates
against parts/parquet-descriptor.md, with `schema_version` 2, `take_uuid`, the format version and the
writer. `recording_id` is `<rec>`. The value columns use `BYTE_STREAM_SPLIT` and no dictionary, and
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
Input: the Parquet of G3.
Pass: every row rule of parts/parquet-descriptor.md holds. `frame_number` of each camera row is the
position of its frame. The capture times equal the player times of the sidecars divided by 10^9, and
the group time of each frame is the mean of the camera times. A point that was not detected has null
`x` and `y` and `visibility` 0.

**SFT-749** Writer: 2D and 3D spaces
Checks: SFF-829, SFF-830
Input: G3 with a rotated camera (`display_rotation` 90).
Pass: the 2D points of the rotated camera are in stored-JPEG pixels, and its image reference has the
stored width and height. The 3D reference frame is `calibrated_world` with the Blender basis, in mm.

**SFT-750** Writer: camera sources and skeletons
Checks: SFF-826, SFF-832
Input: the Parquet of G3.
Pass: each camera source is `camera:<label>` with `camera_key`, `video_filename` and
`timing_filename` that name files of the take, and no nominal rate. Each model has
`tracker_connections` whose names are in `tracker_keypoint_names`, and a `segment_topology`. No
`tracker_schema.json` exists.

**SFT-751** Writer: runs and realtime runs
Checks: SFF-833, SFF-834, SFF-844
Input: G13, then a posthoc run on it; a fold of G13 with unfinished timing sidecars (no fit), then a
repair that rewrites the times of the realtime run.
Pass: the fold gives a run with `origin` `realtime`, a `coverage` object and no checkpoints. Skipped
frames have null `x`, `y` and `visibility`. `timestamp_s` of each row of the realtime run and the
value of each of its `TIMESTAMPS` rows equal the player times that the timing sidecars give at the
time of the fold. With no fit, these are the arrival times. The posthoc run gets
a new `run_id`, and the realtime run is unchanged, byte for byte in its rows. After the repair, the
times of the realtime run equal the fitted times of the repaired sidecars. Only `timestamp_s` and the
values of the `TIMESTAMPS` rows of the realtime run differ: each other value of the run is unchanged.

**SFT-752** Reader: the realtime warning
Checks: SFF-835
Input: G13.
Pass: the take has the warning `realtime_run`, with the counts of the coverage.

**SFT-753** Writer: ChArUco observations
Checks: SFF-836
Input: G14 (the calibration take).
Pass: the ChArUco corners are `OVERLAY_2D` rows of a `charuco_detector` source. No other file holds
them.

**SFT-754** Reader: geometry against the TOML
Checks: SFF-837
Input: G3 with a TOML whose camera 0 is moved 10 mm.
Pass: the run uses its stored geometry, and the take has the warning `calibration_mismatch`.

**SFT-755** Writer: Parquet publication
Checks: SFF-838
Input: a freemocap run, with the file system calls traced.
Pass: the Parquet is written as a `.tmp` and replaced while `.processing.lock` is held, then the
processing info JSON, then the manifest.

### Realtime journal (section 17)

**SFT-756** Writer: journal records
Checks: SFF-839, SFF-840, SFF-841, SFF-842
Input: a realtime session of 60 s with the journal on.
Pass: the first record is the header. Each record has a correct magic, length and CRC. Each channel is
declared before its data, with the `dtype` `float32`. Missing values are NaN. Each result kind of SFF-842 that the session
made is in the journal.

**SFT-757** Reader: damaged journals
Checks: SFF-843
Input: G13; G13 with a header that declares one channel with the `dtype` `float64`; a copy of the
G13 journal with only good records and a torn tail; a copy with only good records and no end record.
Pass: the reader skips the record with a wrong CRC, finds the next record after the zero hole and
stops at the torn tail. The `folder_files` item of the journal has the three counts of the committed
result: the good records, the rejected records and `torn_bytes`. Its state is `damaged`, with the
reason `crc_mismatch`. Each of the two copies is `unfinished`. The journal with the `float64`
channel is `invalid` with the reason `bad_schema`.

**SFT-758** Writer: the journal after the fold
Checks: SFF-845
Input: G13; G13 with a forced failure of the read-back check; a take folder with a left-over journal
at start-up.
Pass: the journal is deleted only after a fold whose check passes. After the forced failure, it is
kept. At start-up, freemocap folds the left-over journal.

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
Input: G3 with an extra `.mkv` with no sidecar, and a sidecar with no media file.
Pass: both extra files are in `other_files` as `not_in_format`, with the warning `orphan_file`.

**SFT-762** Reader: takes and counts
Checks: SFF-866, SFF-869, SFF-870, SFF-871
Input: G9; a folder with two takes; G3 with a camera missing; G3 with two cameras that have one label;
G3 with sidecars that disagree on `clock`.
Pass: each take is reported. Two takes give `multiple_takes`. The missing camera gives `incomplete` and
`incomplete_take`. One label gives `duplicate_label`. The disagreement gives `take_fact_mismatch`,
and the values of `group_position` 0 are used.

**SFT-763** Reader: link checks
Checks: SFF-872, SFF-873, SFF-874
Input: G3; G9; G3 with one `camera_key` 0.
Pass: G3 has each link `ok`. Each vector of G9 gives `mismatch` in its check, and the stale
`parquet_sha256` gives `stale_processing_info`. The key 0 camera is linked by label, with
`camera_key_zero`.

### Legacy folders (section 21)

**SFT-764** Reader: legacy recognition
Checks: SFF-875, SFF-876, SFF-877, SFF-878, SFF-879
Input: G15.
Pass: each folder has `folder_state` `legacy`, and the family, the release range, `ambiguous` and the
warnings of the committed result. The pre-v1 folders have the family `pre_v1`.

**SFT-765** Reader: calibration lookup in v1 folders
Checks: SFF-880
Input: v1 folders with an exact TOML name, one TOML with `calibration` in its name, and two such TOMLs.
Pass: the reader finds the TOML in the first two cases and reports `ambiguous` in the third.

### Privacy and safety (section 22)

**SFT-766** Writer and reader: the privacy list
Checks: SFF-881, SFF-882, SFF-883
Input: G3 with a user camera name and a device serial; G7.
Pass: the manifest `privacy` list has each field of a private kind, sorted, and `media_shows_people`
true. The reader result has `may_contain_private_data` true, also with no manifest.

**SFT-767** Reader: no code in files
Checks: SFF-884
Input: G16.
Pass: the reader does not load the pickle or the object array. Each is `invalid` with
`code_in_file`. No code from the files runs (a canary file is not created).

### The reader result (section 23)

**SFT-768** Reader: the reader result, Python and JS
Checks: SFF-885, SFF-886, SFF-887, SFF-888, SFF-889, SFF-890, SFF-891
Input: every golden folder of Appendix A.
Pass: each result is valid JSON in the canonical form of RFC 8785, with each member of SFF-885.
The states follow the order of SFF-886, and each code is from SFF-887. The sort orders are
those of SFF-890. The Python and JS results are equal to the committed result, byte for byte, for
the parts that the JS reader reads.

**SFT-769** Reader: the JavaScript reader scope
Checks: SFF-892
Input: G3.
Pass: in the JS result, the TOML, the Parquet and the journal are `not_checked`, and so is each link
check that needs them. All other members equal the Python result.
