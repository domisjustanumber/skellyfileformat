# skellyfileformat specification

Status: **draft v2 (the whole take folder), for review at gate 1**
([AGENTS.md section 4](../AGENTS.md#4-project-rules)). No format version is released yet. Draft v1
(the MCAP profile) was withdrawn before gate 1, because the freemocap Blender addon needs real video
files ([ADR-6RSB](../decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). Draft v0 (MKV
with binary sidecars) was withdrawn earlier. Their IDs stay in section 0, marked withdrawn. A
requirement marked `(provisional)` names the open item that it waits for
([open-work.md](../decisions/open-work.md)).

This specification is normative, with its part [parts/parquet-descriptor.md](parts/parquet-descriptor.md).
The [legacy annex](legacy-annex.md) and Appendix B are informative. The license of the spec text is
CC-BY-4.0 ([LICENSE](LICENSE)).

## 0. Withdrawn requirements

The requirements of draft v0 and draft v1 are withdrawn. Their IDs are not reused.

<details>
<summary>Withdrawn IDs SFF-001 to SFF-680</summary>

**SFF-001** (withdrawn) Draft v0.

**SFF-002** (withdrawn) Draft v0.

**SFF-003** (withdrawn) Draft v0.

**SFF-004** (withdrawn) Draft v0.

**SFF-005** (withdrawn) Draft v0.

**SFF-006** (withdrawn) Draft v0.

**SFF-007** (withdrawn) Draft v0.

**SFF-008** (withdrawn) Draft v1.

**SFF-009** (withdrawn) Draft v1.

**SFF-010** (withdrawn) Draft v1.

**SFF-011** (withdrawn) Draft v1.

**SFF-012** (withdrawn) Draft v1.

**SFF-013** (withdrawn) Draft v1.

**SFF-050** (withdrawn) Draft v0.

**SFF-051** (withdrawn) Draft v0.

**SFF-052** (withdrawn) Draft v0.

**SFF-053** (withdrawn) Draft v0.

**SFF-054** (withdrawn) Draft v0.

**SFF-055** (withdrawn) Draft v0.

**SFF-056** (withdrawn) Draft v0.

**SFF-057** (withdrawn) Draft v0.

**SFF-058** (withdrawn) Draft v0.

**SFF-059** (withdrawn) Draft v1.

**SFF-060** (withdrawn) Draft v1.

**SFF-061** (withdrawn) Draft v1.

**SFF-062** (withdrawn) Draft v1.

**SFF-063** (withdrawn) Draft v1.

**SFF-064** (withdrawn) Draft v1.

**SFF-065** (withdrawn) Draft v1.

**SFF-066** (withdrawn) Draft v1.

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

**SFF-114** (withdrawn) Draft v1.

**SFF-115** (withdrawn) Draft v1.

**SFF-116** (withdrawn) Draft v1.

**SFF-117** (withdrawn) Draft v1.

**SFF-118** (withdrawn) Draft v1.

**SFF-119** (withdrawn) Draft v1.

**SFF-120** (withdrawn) Draft v1.

**SFF-121** (withdrawn) Draft v1.

**SFF-122** (withdrawn) Draft v1.

**SFF-123** (withdrawn) Draft v1.

**SFF-124** (withdrawn) Draft v1.

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

**SFF-181** (withdrawn) Draft v1.

**SFF-182** (withdrawn) Draft v1.

**SFF-183** (withdrawn) Draft v1.

**SFF-184** (withdrawn) Draft v1.

**SFF-185** (withdrawn) Draft v1.

**SFF-186** (withdrawn) Draft v1.

**SFF-187** (withdrawn) Draft v1.

**SFF-188** (withdrawn) Draft v1.

**SFF-189** (withdrawn) Draft v1.

**SFF-190** (withdrawn) Draft v1.

**SFF-191** (withdrawn) Draft v1.

**SFF-192** (withdrawn) Draft v1.

**SFF-200** (withdrawn) Draft v0.

**SFF-201** (withdrawn) Draft v0.

**SFF-202** (withdrawn) Draft v0.

**SFF-203** (withdrawn) Draft v0.

**SFF-204** (withdrawn) Draft v0.

**SFF-205** (withdrawn) Draft v0.

**SFF-206** (withdrawn) Draft v0.

**SFF-207** (withdrawn) Draft v0.

**SFF-208** (withdrawn) Draft v0.

**SFF-209** (withdrawn) Draft v1.

**SFF-210** (withdrawn) Draft v1.

**SFF-211** (withdrawn) Draft v1.

**SFF-212** (withdrawn) Draft v1.

**SFF-213** (withdrawn) Draft v1.

**SFF-214** (withdrawn) Draft v1.

**SFF-215** (withdrawn) Draft v1.

**SFF-216** (withdrawn) Draft v1.

**SFF-217** (withdrawn) Draft v1.

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

**SFF-264** (withdrawn) Draft v1.

**SFF-265** (withdrawn) Draft v1.

**SFF-266** (withdrawn) Draft v1.

**SFF-267** (withdrawn) Draft v1.

**SFF-268** (withdrawn) Draft v1.

**SFF-269** (withdrawn) Draft v1.

**SFF-270** (withdrawn) Draft v1.

**SFF-271** (withdrawn) Draft v1.

**SFF-272** (withdrawn) Draft v1.

**SFF-273** (withdrawn) Draft v1.

**SFF-274** (withdrawn) Draft v1.

**SFF-300** (withdrawn) Draft v0.

**SFF-301** (withdrawn) Draft v0.

**SFF-302** (withdrawn) Draft v0.

**SFF-303** (withdrawn) Draft v0.

**SFF-304** (withdrawn) Draft v0.

**SFF-305** (withdrawn) Draft v1.

**SFF-306** (withdrawn) Draft v1.

**SFF-307** (withdrawn) Draft v1.

**SFF-308** (withdrawn) Draft v1.

**SFF-309** (withdrawn) Draft v1.

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

**SFF-369** (withdrawn) Draft v1.

**SFF-370** (withdrawn) Draft v1.

**SFF-371** (withdrawn) Draft v1.

**SFF-372** (withdrawn) Draft v1.

**SFF-373** (withdrawn) Draft v1.

**SFF-374** (withdrawn) Draft v1.

**SFF-375** (withdrawn) Draft v1.

**SFF-376** (withdrawn) Draft v1.

**SFF-377** (withdrawn) Draft v1.

**SFF-400** (withdrawn) Draft v0.

**SFF-401** (withdrawn) Draft v0.

**SFF-402** (withdrawn) Draft v0.

**SFF-403** (withdrawn) Draft v0.

**SFF-404** (withdrawn) Draft v0.

**SFF-405** (withdrawn) Draft v0.

**SFF-450** (withdrawn) Draft v0.

**SFF-451** (withdrawn) Draft v0.

**SFF-452** (withdrawn) Draft v0.

**SFF-453** (withdrawn) Draft v0.

**SFF-454** (withdrawn) Draft v0.

**SFF-455** (withdrawn) Draft v0.

**SFF-500** (withdrawn) Draft v0.

**SFF-501** (withdrawn) Draft v0.

**SFF-502** (withdrawn) Draft v0.

**SFF-503** (withdrawn) Draft v0.

**SFF-504** (withdrawn) Draft v0.

**SFF-550** (withdrawn) Draft v0.

**SFF-551** (withdrawn) Draft v0.

**SFF-552** (withdrawn) Draft v0.

**SFF-553** (withdrawn) Draft v0.

**SFF-554** (withdrawn) Draft v1.

**SFF-555** (withdrawn) Draft v1.

**SFF-556** (withdrawn) Draft v1.

**SFF-557** (withdrawn) Draft v1.

**SFF-600** (withdrawn) Draft v0.

**SFF-601** (withdrawn) Draft v0.

**SFF-602** (withdrawn) Draft v0.

**SFF-603** (withdrawn) Draft v0.

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

**SFF-669** (withdrawn) Draft v1.

**SFF-670** (withdrawn) Draft v1.

**SFF-671** (withdrawn) Draft v1.

**SFF-672** (withdrawn) Draft v1.

**SFF-673** (withdrawn) Draft v1.

**SFF-674** (withdrawn) Draft v1.

**SFF-675** (withdrawn) Draft v1.

**SFF-676** (withdrawn) Draft v1.

**SFF-677** (withdrawn) Draft v1.

**SFF-678** (withdrawn) Draft v1.

**SFF-679** (withdrawn) Draft v1.

**SFF-680** (withdrawn) Draft v1.

</details>

## 1. Scope and terms

This spec describes one **take folder**: the files of one synchronised capture and every file that
the programs add to it later ([ADR-2C9V](../decisions/entries/2C9V-whole-take-folder-scope-and-package.md)).
It gives the names, the layouts, the meaning of each field, the clocks, the writing rules, the rules
for crashed and repaired files, and how a reader opens a folder. Another program can implement the
format from this spec and the standards that it names (Matroska, JPEG, ISO BMFF, Opus, CSV, JSON,
TOML, Apache Parquet).

For a file in a format of another project (`.blend`, MP4, NPY, NPZ, a notebook, a log), this spec
gives the name, the container and the codec, and the content mapping. It does not re-specify the
outside format.

Names, columns, keys and values that the decision entries do not fix are proposed in
[ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md). Gate 1 reviews them.

Terms:

| Term | Meaning |
|---|---|
| take | The files of one synchronised capture. They hold the same `take_uuid`. |
| take folder | The folder that holds one take. A user can rename it (section 4). |
| `<rec>` | The recording name: the name of the take when the writer started it. It does not change when the take folder is renamed (section 4). |
| media folder | The subfolder `synchronized_videos/` of a take folder. |
| camera file | An MKV file of this format with one JPEG video track (section 6). |
| audio file | An MP4 file of this format with one Opus track (section 9). |
| media file | A camera file or an audio file. |
| timing sidecar | The CSV file that holds the timing of one media file (sections 7, 8 and 10). |
| device pair | A media file and its timing sidecar. |
| folder file | A file of the take folder that is not in a device pair: the manifest, the info JSONs, the calibration TOML, the Parquet, the journal and the files of section 18. |
| file of this format | A file with a mark of this format. SFF-875 gives the list. |
| multi-camera frame | The frames of the cameras of a take that have the same position. Row k of each video sidecar of a take is multi-camera frame k (SFF-754). |
| finished file | A file that its writer closed normally. A finished CSV ends with an `# end` line. |
| unfinished file | A file that its writer did not close, for example after a crash (section 12). |
| repaired file | An unfinished file that a repair changed into a finished file (section 12). |
| writer | A program that writes files of this format. A writer with live capture is a **capture writer** (skellycam). A writer that makes files from other files is a **conversion writer** (the skellycam converter, skellysync). freemocap writes the folder files. |
| reader | A program that reads files of this format. A player is a reader. |
| host clock | The monotonic clock of the computer that recorded the take (section 11). |
| take start | The time `take_start_host_ns`. Times in the CSV rows are relative to it. |
| arrival time | The host-clock time at which the writer received a frame or an audio block. |
| sample time | The host-clock time that the capture driver gives for a frame or an audio block. |
| fitted time | The writer's estimate, on the host clock, of the regular lattice of a camera or of the sample clock (section 11). It is not corrected for latency. |
| player time | The time that a reader uses to place a frame or a sample (section 11). |
| position | The place of a frame in its camera file, or of a row in its CSV: 0, 1, 2 and so on, in file order. |
| source frame number | The frame number that the camera or the source gives. A gap shows a dropped frame. |
| nominal rate | The requested or configured frame rate of a camera, as a rational number. |
| fit segment | A part of a file in which the fitted time is a straight line (section 11). |

## 2. Conventions

- The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY have the meanings of RFC 2119 and
  RFC 8174, when they are in capital letters.
- A requirement starts on a new line with its ID in bold. The ID has three digits. A requirement has
  one ID. An ID is not reused or renumbered.
- The IDs of draft v0 and draft v1 are withdrawn. They stay in section 0. The requirements of draft
  v2 start at SFF-700 and are numbered in file order. A new requirement in a later draft gets the
  next free ID after the last ID of the file. The tests in [conformance.md](conformance.md) follow the
  same rule from SFT-700.
- A provisional requirement has `(provisional)` after its ID and names the open item that it waits
  for. A provisional requirement must be closed before v2.0.0.
- `(writer)` or `(reader)` after an ID tells which program the requirement applies to.
- Each requirement has one or more tests in [conformance.md](conformance.md).
  `tools/check_spec_traceability.py` checks this.
- ⌊a / b⌋ is integer division rounded down, for a ≥ 0 and b > 0.
- A path in this spec is relative to the take folder and uses `/`.

**SFF-700** (writer, reader) Each timing sidecar, JSON file and TOML file of this format, and each
JSON record of the journal, is UTF-8 with no byte order mark and with LF line ends. The exports of
section 18 have their own rules.

**SFF-701** (writer, reader) An integer in a CSV field or in a CSV header value is written in
decimal, with a `-` sign when it is negative, with no `+` sign, no leading zeros (except the value
`0`) and no spaces. A reader refuses a file with an integer in another form (reason `bad_metadata`).
In a data row, each integer that is not a time is from 0 to 2^53 − 1. A reader refuses a file with
another value (reason `bad_metadata`)
([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-702** (writer, reader) A JSON file is RFC 8259 JSON with one object at the top. In it, each
integer that can be outside the range −2^53 to 2^53 is a JSON string in the form of SFF-701. Other
integers are JSON numbers. A writer writes the members in the order that this spec lists them.

**SFF-703** (writer, reader) The text form of a 16-byte ID (`take_uuid`, `calibration_uuid`) is 32
lowercase hexadecimal characters, with no dashes. The ID is a random UUID version 4.

**SFF-704** (writer, reader) CRC-32 is CRC-32/ISO-HDLC (the zlib `crc32`). Its text form is 8
lowercase hexadecimal characters, with leading zeros.

**SFF-705** (writer, reader) Each time is an integer number of nanoseconds on the host clock of
the take. A time in a CSV row is relative to the take start. An absent time is an empty field.

**SFF-706** (reader) A JavaScript reader keeps each 64-bit integer exact (for example with
`BigInt`). It makes a JavaScript number from a time only after it subtracts the take start. It
reports a difference with a magnitude of 2^53 or more as an error (the reason `bad_time`, SFF-887),
not as an inexact number.

## 3. Versioning

The rules of the README section [Versioning](../README.md#versioning-normative) apply
([ADR-9DV4](../decisions/entries/9DV4-format-version-from-freemocap.md)). The format version is the
`major.minor` of the freemocap release that last changed any file of the folder.

**SFF-707** (writer) These files record the format version as `format_version` (the text
`major.minor`, for example `2.0`) and `format_prerelease` (an integer): the manifest, each timing
sidecar, the capture info JSON, the processing info JSON, the calibration TOML, the descriptor of the
Parquet, the header record of the journal, the export inventory and the BVH metadata JSON
(section 18). No other file of section 18 records the format version or a writer string
([ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)). `major`, `minor` and
`format_prerelease` are integers from 0 to 65,535. The section of
each file gives the place of these fields. A media file is a standard file with no added field: a
writer writes no version field and no writer string of this format into a camera file or an audio
file. The timing sidecar of a device pair holds the format version and the writer string for its
media file ([ADR-E45D](../decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).

**SFF-708** (reader) A reader MUST refuse a file with a `major` that it does not know (state
`unsupported_version`). It does not report the file as legacy.

**SFF-709** (reader) A reader MUST read a file with a higher `minor` of a `major` that it
knows. It ignores the header keys, columns, JSON members, TOML keys, flag bits and record types that
it does not know.

**SFF-710** (writer) A writer writes only the latest format version. Before v2.0.0 is
released, a writer writes `2.0` and `format_prerelease` = N, where N is the prerelease revision. A
released writer writes `format_prerelease` = 0.

**SFF-711** (reader) A reader MAY refuse a file with `format_prerelease` > 0.

**SFF-712** (writer, reader) Each file that SFF-707 names holds a writer string `writer`, for
example `skellycam 2.1.3`. A media file holds none: the `writer` of its timing sidecar is the writer
string of the device pair. A reader MUST NOT change its behaviour because of a writer string.
skellysync writes the format version that skellyfileformat gives.

**SFF-713** (reader) The version of a container (the Matroska `DocTypeVersion`, the MP4
brands, the Parquet format version) is not the format version. A reader does not use it as the
format version.

**SFF-714** (reader) A reader uses a field or a rule only when the `minor` of the file is equal
to or higher than the minor version that added it. In version 2.0, every field and rule of this spec
has minor 0.

## 4. The take folder: layout and names

A take folder has this layout ([ADR-5XNA](../decisions/entries/5XNA-folder-layout-names-and-manifest.md)).
`<label>` is a camera label (SFF-720).

```
<take folder>/                          any name; a user can rename it
  recording_manifest.json               section 5
  <rec>_info.json                       section 13 (skellycam)
  <rec>_recording_info.json             section 14 (freemocap)
  <rec>_camera_calibration.toml         section 15
  <rec>_data.parquet                    section 16
  <rec>_realtime_journal.bin            section 17 (while it exists)
  <rec>.blend                           section 18
  .processing.lock                      section 12 (the lock file, SFF-789)
  synchronized_videos/
    <rec>.<label>.mkv                   section 6, one for each camera
    <rec>.<label>.csv                   section 8
    <rec>.audio.m4a                     section 9, when the take has audio
    <rec>.audio.csv                     section 10
  annotated_videos/                     section 18
  exports/                              section 18
  blender/                              section 18
  logs/                                 section 18
```

**SFF-715** (writer) `<rec>` is a string of 1 to 128 bytes of UTF-8. It holds no control
character, no `.` and none of `/ \ : * ? " < > |`. It does not start or end with a space. It is not a
reserved device name of Windows (`CON`, `PRN`, `AUX`, `NUL`, `COM1` to `COM9`, `LPT1` to `LPT9`), in
any case. The capture writer fixes `<rec>` when the take starts. No writer changes it later.

**SFF-716** (writer) A writer gives each file and subfolder of the layout above its exact name. It
does not write a file of this spec under another name or in another subfolder.

**SFF-717** (writer, reader) A program MUST NOT rename a file or a subfolder inside a take
folder. A program MAY rename the take folder. A reader finds `<rec>` in the manifest. When it
rebuilds the links, it finds `<rec>` in the name of a timing sidecar file (SFF-868). It never finds
`<rec>` in the name of the take folder.

**SFF-718** (reader) A reader finds a folder file by its exact name, built from `<rec>`. It does
not search with a glob pattern. It also uses exact names in the manifest rebuild (SFF-731). The only
exception is the legacy reads of section 21
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-719** (writer) A writer puts one take in one take folder. It puts no file of another take
in it.

**SFF-720** (writer) The `camera_label` of a camera is the first 6 hexadecimal characters of
its `camera_key` (section 8). When two cameras of the take have the same 6 characters, the writer
uses 7, then 8 characters for every camera of the take, until each label is different. A camera with
`camera_key` 0 gets the label `cam<N>`, where N is its `group_position` (section 8).

**SFF-721** (reader) A reader scans only the root of the take folder and the media folder. It
finds the files of the other subfolders through the manifest, or by their fixed names. To find a
file by its fixed name, a reader MAY test one exact path of section 18 that it builds from `<rec>`,
for example `annotated_videos/<rec>.<camera_label>.annotated.mp4`. It does not list another
subfolder. It does not search another subfolder with a glob pattern. It does not look inside other
subfolders for files of this format.

**SFF-722** (writer) A writer of this format does not write `synchronized_videos_README.md`.

## 5. The recording manifest

The manifest `recording_manifest.json` links the files of the take
([ADR-5XNA](../decisions/entries/5XNA-folder-layout-names-and-manifest.md)). It is a JSON file
(SFF-702) with these members, in this order:

| Member | Value |
|---|---|
| `skellyfileformat` | `"recording_manifest"` |
| `format_version`, `format_prerelease` | The format version (section 3) |
| `writer` | The writer string of the program that wrote this version of the file |
| `take_uuid` | The ID of the take (SFF-703) |
| `recording_name` | `<rec>` |
| `purpose` | `"motion_capture"` or `"calibration"` |
| `state` | `"recording"` while the capture writer records, `"finished"` after it ends the take |
| `cameras` | An array, in order of `group_position`. Each item: `camera_key`, `camera_label`, `group_position`, `video` (path of the camera file), `timing` (path of its CSV), `calibration_camera` (the name of its camera table in the calibration TOML, or null) |
| `audio` | null, or an object with `audio` (path of the audio file) and `timing` (path of its CSV) |
| `calibration` | null, or an object with `calibration_uuid`, `file` (`<rec>_camera_calibration.toml`) and `sha256` (64 lowercase hexadecimal characters of the SHA-256 of the file) |
| `files` | An array of the other files of the take, in order of `path`. Each item: `path`, `role`, `owner` (`skellycam`, `freemocap` or `blender_addon`), `sha256` (a SHA-256 or null, SFF-723) |
| `warnings` | An array of warning objects (SFF-727) |
| `privacy` | The privacy list (section 22) |
| `summary` | The informative overview (SFF-728) |

The roles of `files` are `capture_info`, `processing_info`, `tracking`, `realtime_journal`, `blend`,
`blender_output`, `annotated_video`, `export` and `log`.

**SFF-723** (writer) The manifest has each member of the table, in the order of the table. Each
path is relative to the take folder, with `/`. `sha256` of a `files` item is the SHA-256 of the file
(64 lowercase hexadecimal characters) for the roles `capture_info`, `processing_info`, `blend`,
`blender_output` and `annotated_video`. It is null for the role `tracking` (the home of that hash is
`parquet_sha256`, section 14), for the role `export` (the home is the export inventory) and for the
roles `realtime_journal` and `log`
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-724** (writer) The capture writer writes the manifest before it writes the first frame or
sample of the take, with `state` = `"recording"`. It lists each camera and the audio file that it
starts. It writes the manifest again after it closes the last media file, with `state` =
`"finished"` and the warnings of SFF-727. For each write, it reads the manifest (when the file
exists), changes it and writes it while it holds `.processing.lock` (SFF-789). It keeps each member
and each item that freemocap owns
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-725** (writer) freemocap updates the manifest when it adds, replaces or deletes a file of
the take. It reads the manifest, changes it and writes it while it holds `.processing.lock`
(SFF-789). It keeps each member and each item that skellycam owns, and each member that it does not
change. It sets `writer` to its own writer string.

**SFF-726** (writer) Each write of the manifest replaces the whole file (SFF-786).

**SFF-727** (writer) Each item of `warnings` has `code`, `source` (`skellycam` or `freemocap`),
`camera_key` (or null) and `detail` (a text for people, or null). skellycam writes
`camera_gap` (a camera has one or more gaps), `control_mismatch` (a control reads back a value that
differs from the value that it set) and `awb_not_settled` (auto white balance did not settle before
the take). A program adds its warnings. It does not remove the warnings of another program.

**SFF-728** (writer) The `summary` member is an informative overview for people. It holds:
`take_start_utc` (ISO 8601 UTC text); `duration_s`; `cameras` (each with `camera_label`, `user_name`,
`model`, `stored_px` (`"<width>x<height>"`), `display_rotation`, `nominal_fps`, `gaps`, `filled` and
`exposure_us`, a number or null); `audio` (null, or `{file, sample_rate, channels, duration_s}`);
`calibration` (the `calibration_uuid` and the source take); `processing_runs` (each item is
`{run_id, origin, recorded_at}`, with the latest `recorded_at` of the stage provenances of the run);
and `warnings` (the codes of the manifest `warnings`, each one time, sorted). `nominal_fps` is
`num/den` of the nominal rate, rounded half up to 3 decimal places. The writer of the manifest
computes the summary from the files
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-729** (reader) A reader MUST NOT use a value of `summary` for processing. When
`summary` does not agree with the home of a value, the home wins, and a reader gives the take
warning `summary_stale`. A reader gives this warning when `camera_label`, `display_rotation` or
`nominal_fps` (after the rounding of SFF-728) of a summary camera differs from the timing sidecar of
the camera, or when `gaps` or `filled` differs from the `# end` line of a finished or repaired
sidecar.

**SFF-730** (reader) A reader uses the manifest to find the files of the take. It checks
each link against the files (section 20). It does not check `sha256` of a `files` item.

**SFF-731** (reader) When `recording_manifest.json` is missing, is not valid JSON, or is not a
manifest of this format, a reader rebuilds the links by a scan. It finds the device pairs in the media
folder by their content (section 20). It takes `<rec>` from the timing sidecars (SFF-868). Then it
tests these exact names in the root: `<rec>_info.json`, `<rec>_recording_info.json`,
`<rec>_camera_calibration.toml`, `<rec>_data.parquet`, `<rec>_realtime_journal.bin` and
`<rec>.blend`. It does not match a suffix
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)). The scan does not
find the files of the other subfolders (SFF-721). It gives the take
warning `manifest_missing`. It does not write a manifest.

## 6. Camera files

A camera file is a Matroska file ([RFC 9559](https://www.rfc-editor.org/rfc/rfc9559)) with DocType
`matroska` ([ADR-6RSB](../decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). It
holds no version field and no writer string of this format: its timing sidecar holds them (SFF-707).

**SFF-732** (writer) A camera file has exactly one track: a video track with CodecID `V_MJPEG`
and a track number below 128. It has no other track.

**SFF-733** (writer) Each frame is one JPEG image in one `SimpleBlock` with the keyframe flag.
No block is laced. The frames are in position order.

**SFF-734** (writer) A capture writer stores the JPEG bytes that an MJPEG camera sent,
unchanged. For a camera that sends raw frames, it encodes each frame to JPEG
([ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md)). It does not capture H.264. It
refuses a request for H.264 capture.

**SFF-735** (writer) A writer stores each frame in the orientation of the sensor. It does not
rotate the pixels. It writes no rotation element (for example `Projection` or `ProjectionPoseRoll`)
and no EXIF orientation tag ([ADR-DE9S](../decisions/entries/DE9S-rotation-in-the-video-csv-header.md)).

**SFF-736** (writer) The TimestampScale is 1,000,000 (1 ms). The container timestamp of the
frame at position k is ⌊(2 × k × `den` × 1000 + `num`) / (2 × `num`)⌋ ms, where `num/den` is the
nominal rate (k / nominal rate, rounded half up). The track `DefaultDuration` is the nominal frame
period in nanoseconds, rounded half up. A writer MUST NOT store measured times in the container. A
writer refuses a nominal rate above 1000 frames per second.

**SFF-737** (writer) A writer stores no timing data, no overlay and no burned-in text in a
frame, for example in an APPn segment of the JPEG. A take folder holds no overlay file
([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-738** (reader) A reader MUST NOT require a JFIF or APP0 segment, a DHT segment or a
fixed marker order in a JPEG. It MUST accept bytes after the entropy-coded data. A frame is the bytes
of its block payload. A reader ignores an EXIF orientation tag.

**SFF-739** (reader) A reader finds a block payload by parsing the block header: the track
number as an EBML variable-size integer, then 2 bytes of timestamp, then 1 byte of flags. It MUST NOT
assume a fixed header length.

**SFF-740** (reader) An unfinished camera file can have no Cues and elements of unknown size. A
reader of an unfinished camera file finds its frames from the byte positions of its CSV rows, or by a
walk of the elements from the start of the Segment data. Row k of the sidecar belongs to the k-th
complete block of the camera file, in file order. A frame is usable when its row is usable (SFF-746)
and its block is complete. A reader uses no row after the last complete block, and no block after the
last usable row ([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

## 7. CSV timing sidecars: common rules

Each media file has one timing sidecar, a CSV file with the same name stem and the suffix `.csv`
([ADR-6RSB](../decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). A timing sidecar
has, in this order: header lines, one column line, data rows, and footer lines.

```
# skellyfileformat=video_timing
# format_version=2.0
# format_prerelease=3
# writer=skellycam 2.0.0
# take_uuid=6f1c2c1e1d7e4c479a3e2f2b3c4d5e6f
...
frame,source_frame_number,arrival_ns,sample_ns,flags,byte_offset,byte_size,crc32
0,1000,1203311,1180002,0,4127,61234,5b1e0c2a
...
# fit_segment pos_first=0 pos_last=18341 t0_ns=1190001 period_ps=33366700000
# end rows=18342 gaps=2 filled=0 encode_skips=0
```

**SFF-741** (writer) A timing sidecar is a text file (SFF-700). Fields are separated by
`,`. A field holds no `,`, no quote, no space and no line end. No field is quoted.

**SFF-742** (writer) A header line has the form `# <key>=<value>`, with one key on each line.
A key holds only `a`–`z`, `0`–`9` and `_`. A value holds no line end. The first header line is
`# skellyfileformat=video_timing` or `# skellyfileformat=audio_timing`. The header holds each key that
section 8 or 10 lists for its kind, in the order of that list.

**SFF-743** (writer) After the header lines, the column line holds the column names of
section 8 or 10, in that order. The last column is `crc32`.

**SFF-744** (writer) Each data row has one field for each column. The `crc32` field is the CRC-32
(SFF-704) of the bytes of the row before the comma that precedes it. A writer writes each row in one
write, with its LF, and flushes it (section 12).

**SFF-745** (writer) Footer lines follow the last data row. A footer line is `# <word>`, then zero
or more ` <key>=<value>`, each after one space. A writer writes the keys in the order of this spec.
Only the value of the last key of a line can hold a space. That value ends at the line end. A later
minor version adds a key before the last key of a line. A writer writes footer lines only when it
ends the file normally, or in a repair. The last line of a finished file is `# end` followed by the
counts of section 8 or 10 ([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-746** (reader) A reader reads a timing sidecar strictly. It uses a data row only when
the row ends with LF, has the right number of fields and its CRC is correct. A last line with no LF is
torn: it ends the read, and its bytes count in `torn_bytes`. A complete row with a wrong CRC makes the
file `damaged` (reason `crc_mismatch`), and the read stops at that row.

**SFF-747** (reader) A timing sidecar that does not end with an `# end` line is unfinished.
A reader uses its complete rows.

**SFF-748** (reader) A reader refuses a timing sidecar (state `invalid`) whose header lacks a
key that its kind requires (reason `missing_metadata`), or has a value in a wrong form (reason
`bad_metadata`).

## 8. Video timing sidecar

The header of a video timing sidecar holds these keys, in this order:

| Key | Value |
|---|---|
| `skellyfileformat` | `video_timing` |
| `format_version`, `format_prerelease` | Section 3. They apply to the device pair (SFF-707). |
| `writer` | The writer string. It applies to the device pair (SFF-712). |
| `take_uuid` | The ID of the take (SFF-703) |
| `take_start_host_ns` | The take start on the host clock (absolute) |
| `take_start_utc_ns` | The take start in UTC, in nanoseconds since 1970-01-01T00:00:00Z |
| `utc_offset_min` | Local time minus UTC at the take start, in minutes |
| `clock` | The host clock (section 11) |
| `clock_hz` | The frequency of the host clock counter, or empty. For diagnostics only. |
| `group_size` | The number of cameras of the take |
| `audio_count` | 1 when the take has an audio file, else 0 |
| `group_position` | The place of this camera in the take, from 0 to `group_size` − 1 |
| `camera_key` | 16 lowercase hexadecimal characters, or `0` |
| `camera_label` | The label (SFF-720) |
| `nominal_rate` | `num/den` |
| `display_rotation` | 0, 90, 180 or 270 |

The columns are:

| Column | Value |
|---|---|
| `frame` | The position of the frame |
| `source_frame_number` | The source frame number, or empty |
| `arrival_ns` | The arrival time (relative) |
| `sample_ns` | The sample time (relative), or empty |
| `flags` | The flags of the frame (SFF-756) |
| `byte_offset` | The offset of the JPEG payload from the start of the camera file |
| `byte_size` | The number of bytes of the JPEG payload |
| `crc32` | The row CRC (SFF-744) |

The footer of a finished file has zero or more `# fit` and `# fit_segment` lines (section 11), then
`# end rows=<R> gaps=<G> filled=<F> encode_skips=<E>`.

**SFF-749** (writer) The take keys (`take_uuid` to `audio_count`) have the same values in each
timing sidecar of a take.

**SFF-750** (writer, reader) In `nominal_rate`, `num` and `den` are integers from 1 to 2^20. A
reader refuses another value (reason `bad_rate`).

**SFF-751** (writer, reader) `display_rotation` is the clockwise rotation in degrees that a reader
applies to the stored frame to show it upright. A reader refuses another value (reason
`bad_rotation`).

**SFF-752** (writer) `camera_key` is the first 8 bytes of the SHA-256 of the identity string of the
camera, as 16 lowercase hexadecimal characters. The identity string is
`<vendor_id>:<product_id>:serial:<serial>`, or `<vendor_id>:<product_id>:port:<port_path>` when the
device gives no serial. The four values are the texts of `device` in the capture info JSON
(section 13), with `0000` for a vendor ID or a product ID that is null. The hash input is the UTF-8
bytes of the identity string ([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)). A
capture writer MUST write a `camera_key` that is not 0. A conversion writer MAY write `0`.

**SFF-753** (reader) A reader refuses a sidecar whose `camera_label` does not have the form
of SFF-720 (reason `bad_label`).

**SFF-754** (writer) There is one row for each frame of the camera file, in position order.
`frame` is 0 in the first row and increases by 1 in each row. Row k of each video sidecar of a take
is multi-camera frame k. The finished camera files of one take have the same number of rows
([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md)). A camera file has at most 2^31
frames.

**SFF-755** (writer) `arrival_ns` is the host-clock time at which the writer received the frame,
minus the take start. `sample_ns` is the time that the capture driver gives for the frame, on the host
clock, minus the take start. It is empty when the driver gives none. A conversion writer writes an old
per-frame time as `arrival_ns`.

**SFF-756** (writer) `flags` is a decimal integer of bits. Bit 0 (1): `gap`, the source frame
number is not the source frame number of the row before plus 1, and it is not equal to the source
frame number of the row before. `gap` is 0 in the first row, and when the row or the row before has
an empty `source_frame_number`. Bit 1 (2): `filled` (provisional: the slot assembly of the skellycam
plan, row 2.2, and desk tests DT4 and DT7), the writer copied the JPEG of the row before, because
the camera gave no new frame for this multi-camera frame
([ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md)). A writer of version 2.0 writes 0
to bit 1, because it copies no frame. Bit 2 (4): `encode_skip`, the writer did not store one or more
frames before this frame because the JPEG encoder failed. Bit 3 (8): `repeat`, the source frame
number is equal to the source frame number of the row before. A writer writes 0 to the other bits
([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md),
[ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-757** (writer) (provisional: live byte offsets, desk test DT5) `byte_offset` and
`byte_size` give the JPEG payload of the block of the frame in the camera file. They are correct while
the file is live, and they do not change when the file is closed.

**SFF-758** (writer) In the `# end` line, `rows` is the number of data rows, `gaps` the number of
rows with the `gap` flag, `filled` the number with the `filled` flag, and `encode_skips` the number
of rows with the `encode_skip` flag. A repair computes each count from the rows
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-759** (reader) The number of rows of a finished video sidecar is the number of blocks of its
camera file. On a mismatch, a reader refuses the pair (state `invalid`, reason `bad_metadata`).

## 9. Audio file

The audio file is Opus ([RFC 6716](https://www.rfc-editor.org/rfc/rfc6716)) in a fragmented ISO BMFF
file (ISO/IEC 14496-12), with the Opus mapping of the "Encapsulation of Opus in ISO Base Media File
Format" specification ([ADR-92TM](../decisions/entries/92TM-opus-audio-in-fragmented-mp4.md)). It
holds no version field and no writer string of this format: its timing sidecar holds them (SFF-707).

**SFF-760** (writer) The audio file starts with `ftyp` and a `moov` that holds one `trak` with
an `Opus` sample entry and its `dOps` box, and an `mvex` box. The `moov` lists no samples. The audio
follows as `moof` and `mdat` pairs. Each `moof` has one `traf` with a `tfhd` that has the flag
`default-base-is-moof`, a `tfdt` of version 1 and one `trun`. The media timescale is 48000.

**SFF-761** (writer) Each fragment holds the Opus packets of about 1 s of audio, except the last
fragment, which can hold less. The `tfdt` of the first fragment is 0. It includes the pre-skip
samples.

**SFF-762** (writer) The encoder is libopus. The settings are: the channels of the microphone, 1
or 2 (a writer downmixes a device with more); 48 kHz; 20 ms packets (960 samples); application
`audio`; VBR; 128 kbit/s for 1 channel and 256 kbit/s for 2; complexity 10. The `dOps` output gain is
0. The pre-skip is the value that the encoder gives.

**SFF-763** (writer) Before a release, a check confirms that the Opus encoder of the writer is
libopus, not another encoder.

**SFF-764** (writer) The writer flushes the file after each packet that the muxer gives to it.
When it ends the take normally, it closes the muxer, which writes the last fragment and an `mfra`
box.

**SFF-765** (writer) When the device drops samples, the writer inserts that number of samples
of silence and marks the row in the CSV (SFF-768). So the sample index of the decoded stream is
the device sample index.

**SFF-766** (reader) A reader drops the pre-skip samples of `dOps` at the start of the stream.
It does not apply an output gain. Sample 0 of the decoded stream is the first sample after the
pre-skip.

## 10. Audio timing sidecar

The header of the audio timing sidecar holds, in this order: `skellyfileformat` (`audio_timing`),
`format_version`, `format_prerelease`, `writer`, the take keys of section 8 (`take_uuid` to
`audio_count`), and these keys. The version keys and `writer` apply to the device pair, as in
section 8:

| Key | Value |
|---|---|
| `sample_rate` | 48000 |
| `channels` | 1 or 2 |
| `codec` | `opus` |
| `file_sample_offset` | The number of samples that a reader adds to a decoded sample index to get the CSV sample index. 0 for this version. |
| `audio_latency_ns` | (provisional) The time from the sound at the microphone to its ADC time, or empty |

The columns are:

| Column | Value |
|---|---|
| `block` | The position of the row |
| `first_sample` | The sample index of the first sample of the block |
| `n_samples` | The number of samples of the block |
| `host_ns` | The arrival time of the callback block (relative) |
| `adc_ns` | The ADC time that the audio driver gives for the first sample, on the host clock (relative), or empty |
| `flags` | SFF-768 |
| `crc32` | The row CRC |

The footer of a finished file has zero or more `# fit` and `# fit_segment` lines (section 11), then
`# end rows=<R> samples=<S> gaps=<G> silence_samples=<Z>`.

**SFF-767** (writer) There is one row for each capture callback block, in order. The
`first_sample` of a row is the `first_sample` plus the `n_samples` of the row before. The first row
has `first_sample` 0.

**SFF-768** (writer) Bit 0 (1): `overflow`, the device reported an input overflow. Bit 1 (2):
`silence`, the writer inserted this block as silence for samples that the device dropped. A writer
writes 0 to the other bits.

**SFF-769** (writer) In the `# end` line, `rows` is the number of data rows, `samples` the sum of
`n_samples`, `gaps` the number of rows with the `silence` flag and `silence_samples` their samples.

**SFF-770** (writer) The audio sidecar does not hold the name of the microphone. It is in the
capture info JSON (section 13).

**SFF-771** (provisional: microphone latency test, A3 of the skellycam plan) When
`audio_latency_ns` is L, the time at the microphone of a sample with fitted time t is t − L.

## 11. Clocks, the fit and reader timing

The `clock` header key names the host clock of the take:

| `clock` | Clock |
|---|---|
| `windows_qpc` | Windows `QueryPerformanceCounter`, in nanoseconds (Python `time.perf_counter_ns`) |
| `linux_monotonic` | Linux `CLOCK_MONOTONIC`, in nanoseconds |
| `macos_uptime_raw` | macOS `mach_absolute_time` converted to nanoseconds with `mach_timebase_info` (`CLOCK_UPTIME_RAW`) |
| `synthetic` | The timeline of a conversion writer (skellysync). Time 0 is the start of the output. |

Fit lines of a footer:

```
# fit fitter=skellycam-lattice fitter_version=1.0.0 fitter_params={"outlier_reject_ms":5}
# fit_segment pos_first=0 pos_last=5005 t0_ns=1190001 period_ps=33366700000
# fit_segment pos_first=5006 pos_last=18341 t0_ns=167201004000 period_ps=33366700000
```

In an audio sidecar, a segment line is
`# fit_segment row_first=<a> row_last=<b> n0=<n> t0_ns=<t> period_fs=<p>`, where `period_fs` is the
fitted sample period in femtoseconds.

**SFF-772** (writer) All files of a take have the same `clock`, from the table. All their times are
on that clock. A reader refuses another value (reason `bad_metadata`).

**SFF-773** (provisional: Linux and macOS timing tests, T-S7 of the skellycam plan) The `clock`
values `linux_monotonic` and `macos_uptime_raw` are provisional.

**SFF-774** (writer) A capture writer reads `take_start_host_ns` and `take_start_utc_ns` one
after the other, with no other work between the two reads, before the first frame or sample of any
file of the take. `utc_offset_min` is the local offset at that moment. A writer MUST NOT write a
time-zone name.

**SFF-775** (writer) When a capture writer ends a take normally, it writes the fit of each
timing sidecar in its footer: one `# fit` line with `fitter`, `fitter_version` and `fitter_params` (a
JSON object on one line), then one or more `# fit_segment` lines. `fitter_params` is the last key of
the `# fit` line (SFF-745). The fitting method is the writer's choice. A conversion writer MAY write
a fit.

**SFF-776** (writer) In a video sidecar, the segments are in position order, with no gap and no
overlap, and together they hold each position of the file. `t0_ns` is the fitted time of the frame at
`pos_first`, relative to the take start. `period_ps` is the fitted frame period in picoseconds, an
integer greater than 0. A new segment starts where the camera stalls, restarts or changes rate.

**SFF-777** (reader) The fitted time of the frame at position p in a video segment is
`t0_ns` + ⌊d × `period_ps` / 1000⌋. d is the source frame number of p minus the source frame number
of `pos_first`, when both rows have one. Else d is p − `pos_first`. A reader computes it with integers
of unlimited size (Python `int`, JavaScript `BigInt`).

**SFF-778** (writer) In an audio sidecar, the segments are in row order, with no gap and no
overlap, and together they hold each row. `n0` is the `first_sample` of `row_first`. `t0_ns` is the
fitted time of sample `n0`, relative to the take start. `period_fs` is an integer greater than 0.

**SFF-779** (reader) The fitted time of sample n in an audio segment is
`t0_ns` + ⌊(n − `n0`) × `period_fs` / 10^6⌋, computed with integers of unlimited size.

**SFF-780** (reader) A reader MUST NOT change its behaviour because of `fitter`,
`fitter_version` or `fitter_params`. A reader does not parse `fitter_params`.

**SFF-781** (reader) The player time of each frame of a camera file is its fitted time, when the
sidecar is finished or repaired and has a fit that holds each position. Otherwise it is
`arrival_ns`, for every frame of the file, and the reader gives the warning `missing_fit`. A reader
does not mix the two in one file.

**SFF-782** (writer, reader) The player time never decreases from one position to the next in one
file. The times that a reader gives to freemocap for a camera strictly increase. With the player
times p, the strict player time is s(0) = p(0), and s(k) is the larger of p(k) and s(k − 1) + 1 ns.
A reader gives s to freemocap, and SFF-828 uses s. The `records` of the reader result hold p
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-783** (reader) A player shows, at take time t, the last frame of each camera whose player
time is at or before t. It MUST NOT compute a frame from its index and the frame rate. A player shows
no frame of a camera before the player time of its position 0.

**SFF-784** (reader) A reader maps an audio sample to take time only with the fit of the audio
sidecar (SFF-779). It MUST NOT use the take start and the nominal sample rate. It adds
`file_sample_offset` to a decoded sample index before it uses the fit. When the sidecar has no fit
(for example after a crash), the reader gives the warning `missing_fit` and computes one fit segment
from the rows that it uses (SFF-746), with this method ([ADR-E45D](../decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)):

- The time of a row is its `adc_ns` when that field is not empty, else its `host_ns`.
- A row with the flag `silence` is a usable row for the fit
  ([ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).
- a is the first row that the reader uses, and b is the last. n_a and n_b are their `first_sample`
  values. T_a and T_b are their times.
- `row_first` = the `block` of a, `row_last` = the `block` of b, `n0` = n_a and `t0_ns` = T_a.
- `period_fs` = ⌊(T_b − T_a) × 10^6 / (n_b − n_a)⌋, an integer in femtoseconds, rounded down.
- The reader computes each value with integers of unlimited size, and it evaluates the segment with
  SFF-779 for each sample of the file.

When the reader uses fewer than two rows, or `period_fs` is not greater than 0 (SFF-778), the reader
computes no fit. It then maps no sample of the file to take time.

**SFF-785** (reader) The usable length of an audio file is the smaller of the samples that the
CSV rows hold and the samples that the file holds. The samples that the file holds are the samples
of its complete fragments, minus the pre-skip. A reader schedules no audio after that length.

## 12. Writing, crashed files and repair

The rules of [ADR-G1YG](../decisions/entries/G1YG-writing-crash-reading-and-repair.md) apply.

**SFF-786** (writer) A writer writes each file that it writes whole (the manifest, the info JSONs,
the calibration TOML, the Parquet) as `<name>.tmp` in the same folder, forces it to disk, then
replaces the old file with it in one rename. It does not write the file in place.

**SFF-787** (writer) A writer writes each live file (a camera file, a timing sidecar, the audio
file, the journal) by appends only. It flushes each record (a block, a row, a fragment, a journal
record) after it writes it.

**SFF-788** (writer) (provisional: the cost of fsync) While it records, a writer forces each live
file to disk about once a second.

**SFF-789** (writer, reader) `.processing.lock` is an empty file at the root of the take folder.
The lock is the file lock of the operating system on that file, not the existence of the file. A
lock file that no process holds is not a lock, so no rule for a stale lock is necessary. Each writer
of the manifest, also skellycam, reads the manifest, changes it and writes it while it holds the
lock. The lock covers only whole-file writes (SFF-786): the manifest, the info JSONs, the
calibration TOML, the Parquet and the exports. freemocap holds the lock while it writes one of these
files. A writer does not write one of these files when another program holds the lock. An append to
the journal needs no lock: the journal is a live append-only file (SFF-787), like a camera file. A
reader ignores the lock file
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

**SFF-790** (reader) A reader ignores a file whose name ends in `.tmp`. It gives the folder warning
`stray_tmp` when it finds one or more
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-791** (reader) A reader reads an unfinished file in place. It reads each complete record
in file order and reports the file as `unfinished`. A record that is not complete ends the read, and
its bytes count in `torn_bytes`. `torn_bytes` of an unfinished device pair is the bytes of the torn
last line of the sidecar plus the bytes of the media file after its last complete block or fragment
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)). A reader checks that the read
reached the end of the file or a torn record, because a streaming reader can stop at a torn tail
with no error.

**SFF-792** (reader) In an unfinished audio file, a reader ignores a fragment whose `moof` or
`mdat` goes past the end of the file, and a `trun` entry whose bytes go past the end of the file.

**SFF-793** (writer) When a program (skellycam or freemocap) finds an unfinished file of a take
that it owns, or a manifest of such a take whose `state` is `recording`, it asks the user: "An
incomplete recording was found. Would you like to repair it?" This rule also applies at start-up. No
program repairs a file, folds a journal or changes a file of the take before the user agrees. When
the user agrees, the program repairs the files, and freemocap folds a left-over journal as part of
that repair (SFF-845). When the user does not agree, the program changes nothing, and a reader still
reads the files in place (SFF-791)
([ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

**SFF-794** (writer) A repair never changes a byte before its cut. It cuts the file after its
last complete record. Then it appends what a normal end writes, and a repair line.

**SFF-795** (writer) The repair of a timing sidecar cuts after the last complete row with a
correct CRC. It computes the fit from the rows and appends the fit lines, the line
`# repair cut_bytes=<n> media_cut_bytes=<m> repair_writer=<writer string>`, and the `# end` line.
`cut_bytes` is for the sidecar, and `media_cut_bytes` is for the media file. `repair_writer` is the
last key of the line (SFF-745). A reader reports a sidecar with a repair line as `repaired`
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-796** (writer) The repair of an audio file cuts the file after the last fragment whose
`moof` and `mdat` are complete. It removes a zero-filled tail only when the box walk finds an
incomplete box. It does not remux the file. It writes the repair line in the audio sidecar
(SFF-795).

**SFF-797** (writer) (provisional: the repair of a camera file, desk test DT-R1) The repair of a
camera file keeps each complete block. It changes no byte before its cut.

**SFF-798** (writer) A repair that stops before its end leaves an unfinished file. A new
repair starts again from the same cut and gives the same result, except for `cut_bytes` and
`media_cut_bytes`.

**SFF-799** (reader) A reader never creates, moves, renames or changes a file of the take
folder.

## 13. Capture info JSON

skellycam writes `<rec>_info.json` with the capture facts of the take, and no other facts
([ADR-N6HS](../decisions/entries/N6HS-info-jsons-and-calibration.md)). It is a JSON file
(SFF-702) with these members, in this order:

| Member | Value |
|---|---|
| `skellyfileformat` | `"capture_info"` |
| `format_version`, `format_prerelease` | Section 3 |
| `writer` | The writer string |
| `take_uuid` | The ID of the take |
| `camera_configs` | An object. Each key is a `camera_key` (16 hexadecimal characters, or `0` with the label after it, as `0:<camera_label>`). Each value is a camera config (below). |
| `audio` | null, or an object with `device_name`, `host_api` and `device_channels` |

A camera config has these members:

| Member | Value |
|---|---|
| `camera_label` | The label (a link for people; `camera_key` is the link key) |
| `user_name` | The name that the user gave the camera, or null |
| `device` | `model` (the model text of the device), `os_name` (the device name of the OS), `vendor_id` and `product_id` (4 lowercase hexadecimal characters, or null), `serial` (or null), `port_path` (or null), `backend` (for example `media_foundation`, `v4l2`, `avfoundation`) and `os_index` (the OS index at capture, or null) |
| `requested` | `width`, `height` and `framerate` (a number, or `"camera_default"`), `capture_format` (`MJPG` or `YUYV`) and `exposure_mode` (`auto`, `manual` or `recommend`) |
| `controls` | An object of the control values that the writer read back at the take start. Each key is a control name with its unit (SFF-802). Each value is `{"value": <number or null>, "auto": <true, false or null>}`. |
| `exposure_step` | The result of the exposure step, or null: `selected_exposure_us`, `method` and `samples` (an array of `{exposure_us, mean_luma}`) |

**SFF-800** (writer) The capture info JSON has each member of the tables, in their order. It
has no other member. In particular, it has no `videos`, `camera_timing` or `multiframe_timing` map,
no `recording_name`, `recording_directory`, `recording_uuid`, `mic_device_index` or full timestamp
object, and, in a camera config, no `rotation`, `camera_index`, `use_this_camera`, `resolution`,
`color_channels`, `pixel_format` or `writer_fourcc`.

**SFF-801** (writer) skellycam writes the capture info JSON when the take starts and again when
it ends, each time whole (SFF-786). It is the only writer of this file.

**SFF-802** (writer) The control names are `exposure_us`, `gain`, `white_balance_k`, `focus`,
`zoom`, `pan_deg`, `tilt_deg`, `power_line_hz`, `auto_exposure_priority`, `brightness`, `contrast`,
`saturation`, `sharpness`, `gamma` and `backlight_compensation`. A writer writes each control that the
device has. It writes null for a value that it could not read.

**SFF-803** (reader) A reader links a camera config to its camera only by its key (`camera_key`).

## 14. Processing info JSON

freemocap writes `<rec>_recording_info.json` with the summary of its processing, and no capture facts
([ADR-N6HS](../decisions/entries/N6HS-info-jsons-and-calibration.md)). It is a JSON file (SFF-702)
with these members, in this order:

| Member | Value |
|---|---|
| `skellyfileformat` | `"processing_info"` |
| `format_version`, `format_prerelease` | Section 3 |
| `writer` | The writer string |
| `take_uuid` | The ID of the take |
| `processed` | An object: `schema_version` (1), `parquet_sha256` (the SHA-256 of `<rec>_data.parquet`, 64 lowercase hexadecimal characters), `recording_id` (`<rec>`), `parquet` (`<rec>_data.parquet`), `selected_run_id`, `runs`, `conventions` and `export_inventories` |

In `processed`:
- `runs` is an object with a member for each run (the key is the `run_id` as text). Each run has
  `sensor_groups` (each with `clock_description` and `sample_count`), `cameras` (the camera labels),
  `reference_frames` (as in the descriptor) and `data`: an array of the channels of the kinds
  `LANDMARKS_3D`, `KEYPOINTS_3D`, `RAW_KEYPOINTS_3D`, `OVERLAY_2D`, `SEGMENT_ORIGINS` and
  `ROTATIONS_WORLD`, each with `channel` (the `kind` of the descriptor channel), `source`,
  `sensor_group`, `reference_frame`, `names` and `components`.
- `selected_run_id` is the run to show: an integer, 0 or more, and a key of `runs`. The processing
  info JSON is its only home. The Parquet descriptor does not hold it
  ([ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).
- `conventions` is `{"quaternion_order": "wxyz", "segment_pose": "saved origin and world
  orientation", "units": "per component", "coordinates": "per reference frame", "array_order":
  "frames, names, components"}`.
- `export_inventories` is a sorted array of the paths of the export inventories (section 18).

**SFF-804** (writer) The processing info JSON has each member of the table, in its order, and
no other member. It holds no copy of the capture info JSON.

**SFF-805** (writer) freemocap writes the processing info JSON whole (SFF-786) after each
change of the Parquet and after each export, while it holds `.processing.lock`. It is the only writer
of this file.

## 15. Calibration TOML

A calibration TOML is a TOML 1.0.0 file. It holds the camera geometry of one camera setup
([ADR-N6HS](../decisions/entries/N6HS-info-jsons-and-calibration.md)). The camera model is the
OpenCV pinhole model, P = K [R | t], where R and t map the world to the camera. The distortion model is
Brown–Conrady with k1, k2, p1 and p2.

The file has one table `[metadata]` and one table for each camera:

```toml
[metadata]
format_version = "2.0"
format_prerelease = 3
writer = "freemocap 2.0.0"
calibration_uuid = "0c5e9a3b2d1f4e6a8b7c9d0e1f2a3b4c"
source_take_uuid = "6f1c2c1e1d7e4c479a3e2f2b3c4d5e6f"
reprojection_error_px = 0.41
initial_cost = 0.0
final_cost = 0.41
n_iterations = 0
solver_time_seconds = 12.5
n_observations_used = 5400
n_observations_rejected = 0
aligned = false
solver_method = "anipose"
transformation_history = []

[metadata.board]
squares_x = 5
squares_y = 3
square_length_mm = 54.0
marker_length_ratio = 0.8
aruco_dictionary_enum = 2

[9c41d0]
name = "9c41d0"
id = "9c41d0"
camera_key = "9c41d07a55e2b318"
camera_label = "9c41d0"
index = 0
size = [1280, 720]
matrix = [[900.0, 0.0, 640.0], [0.0, 900.0, 360.0], [0.0, 0.0, 1.0]]
distortions = [0.01, -0.02, 0.0, 0.0, 0.0]
rotation = [0.0, 0.0, 0.0]
translation = [0.0, 0.0, 0.0]
world_orientation = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
world_position = [0.0, 0.0, 0.0]

[9c41d0.controls_at_calibration]
exposure_us = 4000
gain = 32
```

`[metadata]` keys:

| Key | Value |
|---|---|
| `format_version`, `format_prerelease`, `writer` | Section 3 |
| `calibration_uuid` | The ID of this calibration (SFF-703) |
| `source_take_uuid` | The `take_uuid` of the take that made it, when known. It stays when that take is deleted. Absent when not known. |
| `reprojection_error_px`, `initial_cost`, `final_cost`, `n_iterations`, `solver_time_seconds`, `n_observations_used`, `n_observations_rejected` | The solver results |
| `aligned` | true when a ground-plane alignment was applied |
| `solver_method` | `anipose` |
| `alignment_method` | `charuco` or `person`. Only when `aligned` is true. |
| `alignment_recording_id` | The `<rec>` of the alignment take. Only when `aligned` is true. |
| `alignment_result` | A table: `origin` (3 floats, mm), `rotation_matrix` (3 × 3, board to world) and `method` (the same as `alignment_method`). Only when `aligned` is true. |
| `transformation_history` | An array of tables, oldest first: `operation` (`charuco`, `person` or `manual`), `quaternion_wxyz` (4 floats, scalar first) and `translation_mm` (3 floats), in the reconstruction axes (+X right, +Y forward, +Z up) |
| `board` | The ChArUco board: `squares_x`, `squares_y` (integers, 2 or more), `square_length_mm`, `marker_length_ratio` (default 0.8; the marker is shorter than the square) and `aruco_dictionary_enum` (the OpenCV dictionary constant) |

Camera table keys:

| Key | Value |
|---|---|
| `name`, `id` | The `camera_label` |
| `camera_key` | The `camera_key` of the camera |
| `camera_label` | The `camera_label` |
| `index` | The `group_position` of the camera |
| `size` | [width, height] of the stored JPEG frames, in pixels |
| `matrix` | K, as 3 rows: [[fx, 0, cx], [0, fy, cy], [0, 0, 1]] |
| `distortions` | [k1, k2, p1, p2, 0.0] |
| `rotation` | The Rodrigues vector of R (3 floats) |
| `translation` | t (3 floats), in millimetres |
| `world_orientation` | Rᵀ (3 × 3), camera to world |
| `world_position` | −Rᵀt (3 floats), in millimetres |
| `controls_at_calibration` | A table of the control values of the camera when the calibration take was recorded, with the names of SFF-802 |

**SFF-806** (writer) A calibration TOML has the `[metadata]` table first, then one table for
each camera, in order of `index`. The key of a camera table is its `camera_label`. The file has no
other top-level key or table.

**SFF-807** (writer) `[metadata]` has the keys of the table. The alignment keys are present
only when `aligned` is true, and `alignment_result.method` is `alignment_method`. `[metadata]` has no
copy of the capture info JSON and no path.

**SFF-808** (writer) Each camera table has the keys of the table. `size` is the size of the
stored JPEG frames, in sensor orientation. `world_orientation` and `world_position` agree with
`rotation` and `translation`.

**SFF-809** (writer) When `aligned` is false, the world frame is the OpenCV camera frame of the
camera with `index` 0 (its rotation and translation are 0): +X right, +Y down, +Z along the optical
axis. freemocap changes a point (X, Y, Z) of the world of each calibration TOML to the point
(x, y, z) of `calibrated_world` (section 16) with one fixed axis map: x = −Y, y = X and z = Z. The
map is the same for an aligned and an unaligned TOML. The names "forward, left, up" for +X, +Y and
+Z of the TOML world are the labels of that map. They describe the room only after an alignment
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-810** (writer) A new calibration gets a new `calibration_uuid`. A writer that changes the
geometry of a calibration (an alignment or a transform) writes a new `calibration_uuid` and adds the
change to `transformation_history` ([ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md)).
A writer never changes a calibration TOML in place without a new `calibration_uuid`.

**SFF-811** (writer) A take that uses a calibration holds a byte-identical copy of it as
`<rec>_camera_calibration.toml`. The manifest records its `calibration_uuid` and SHA-256. A writer
never changes the copy of a take to point at a newer calibration.

**SFF-812** (writer) freemocap keeps a library copy of each calibration as
`<calibration folder>/<source rec>_camera_calibration.toml`, where the calibration folder is
`$FREEMOCAP_BASE_FOLDER/calibrations/`, or `~/freemocap_data/calibrations/` when the variable is not
set. `last_successful_camera_calibration.toml` in that folder is a byte-identical copy of the newest
library file. A take refers to a calibration only by its `calibration_uuid`, never by that name. A
calibration TOML outside a take is a file of this format.

**SFF-813** (writer) A writer writes each calibration TOML whole (SFF-786): the copy of the
calibration take, the library copy and `last_successful_camera_calibration.toml`.

**SFF-814** (reader) A reader finds the calibration of a take of this format through the
manifest (`calibration.file`). It checks that the `calibration_uuid` of the TOML is the one of the
manifest, and that its SHA-256 is the `sha256` of the manifest (section 20). It does not look for
another TOML. The only exception is the manifest rebuild (SFF-731): the reader then uses
`<rec>_camera_calibration.toml`.

**SFF-815** (reader) A reader links a camera table to its camera by `camera_key`. It reads the
camera tables in the order of `index`, not of their keys.

## 16. Tracking Parquet

`<rec>_data.parquet` holds the 2D and 3D tracking data of the take, the ChArUco observations and the
diagnostics ([ADR-P76Y](../decisions/entries/P76Y-tracking-parquet.md)). It is an Apache Parquet file
(parquet-format 2.8.0 or later) with an Arrow schema. freemocap writes it. skellycam writes no Parquet
file. The descriptor and its models are in [parts/parquet-descriptor.md](parts/parquet-descriptor.md),
which is normative. SFF-893 gives what a reader checks in a model of the descriptor. The current
writer is freemocap `development-streaming` at c27fc299, with the
changes of this section (descriptor `schema_version` 2).

The file is a tall table: one row for each value (a frame × a name × a component). Its columns are,
in this order:

| # | Column | Arrow type | Null | Value |
|---|---|---|---|---|
| 1 | `timestamp_s` | float64 | no | The time of the sample in seconds from the take start |
| 2 | `sensor_group` | string | no | The sampling grid, a key of `runs[run_id].sensor_groups` |
| 3 | `frame_number` | int32 | no | The sample number on that grid, 0 or more |
| 4 | `source` | string | no | The producer, a key of `runs[run_id].sources` |
| 5 | `reference_frame` | string | yes | A key of `runs[run_id].reference_frames`, or null |
| 6 | `channel` | string | no | The channel kind (parts/parquet-descriptor.md) |
| 7 | `name` | string | no | A name of the channel's `names` |
| 8 | `component` | string | no | A key of the channel's `components` |
| 9 | `value` | float32 | yes | The value, for a channel of `dtype` `float32` |
| 10 | `value_f64` | float64 | yes | The value, for a channel of `dtype` `float64` |
| 11 | `units` | string | no | The units of the component |
| 12 | `run_id` | int32 | no | The run, a key of `runs`, 0 or more |

**SFF-816** (writer) The Arrow schema of the file has exactly the columns of the table, in this
order, with these types and this nullability. A string column is `string`, not `large_string` or a
dictionary type. A required column has no null.

**SFF-817** (writer) The Arrow schema metadata has the key `freemocap.recording`. Its value is the
UTF-8 JSON of the descriptor `RecordingMetadata` (parts/parquet-descriptor.md), with
`schema_version` 2.

**SFF-818** (writer) The file uses ZSTD compression at level 3. The columns `value` and
`value_f64` use the `BYTE_STREAM_SPLIT` encoding and no dictionary. A writer MUST NOT use LZ4,
LZ4_RAW or Brotli. A writer MAY use a dictionary on the string columns.

**SFF-819** (reader) A reader of this file supports `BYTE_STREAM_SPLIT` on FLOAT and DOUBLE
columns and ZSTD compression. A reader MUST also accept the Arrow type int64 in the columns
`frame_number` and `run_id`. Files of an earlier writer have this type. A reader does not refuse
such a file (reason `bad_schema`).

**SFF-820** (writer) Each channel declares `dtype`: `float32` (the default) or `float64`.
`TIMESTAMPS` channels are `float64`. A row of a `float32` channel has its value in `value` and null in
`value_f64`. A row of a `float64` channel has its value in `value_f64` and null in `value`. A missing
value is null in both. A reader uses the column that the `dtype` of the channel names, not the column
that is not null.

**SFF-821** (writer) A missing value is null, never NaN. A writer MUST NOT write NaN or an
infinite value.

**SFF-822** (writer) A writer writes a file only when it obeys each rule of
parts/parquet-descriptor.md section "Row rules": each row's channel, name, component and units are
declared; each trajectory has exactly the `sample_count` rows of its sensor group, with strictly
increasing `frame_number` and `timestamp_s`; the trajectories of one context share one
(`frame_number`, `timestamp_s`) grid; each quaternion is a unit quaternion or all null.

**SFF-823** (writer) Each row group holds the rows of one channel and whole frames, as the
writer makes them. A writer does not merge the rows of two channels into one row group.

**SFF-824** (writer, reader) `recording_id` of the descriptor is `<rec>`. A reader checks it
against `<rec>` of the take, not against the name of the take folder. A wrong `recording_id` makes
the `folder_files` item of the Parquet `invalid`, with the reason `take_fact_mismatch`
([ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-825** (writer) The descriptor holds `take_uuid`, `format_version`, `format_prerelease` and
`writer`.

**SFF-826** (writer) Each camera source is `camera:<camera_label>`, with the definition of
parts/parquet-descriptor.md: `camera_key`, `camera_label`, `video_filename`, `timing_filename`,
`timing_method` and `inferred_offset_s`. The definition holds no nominal frame rate: the timing sidecar is its home.

**SFF-827** (writer) `frame_number` of a camera row is the position of the frame in its camera
file. All cameras of a sensor group use the same `frame_number` for one multi-camera frame
(SFF-754).

**SFF-828** (writer) `timestamp_s` of a capture `TIMESTAMPS` row, and of the `OVERLAY_2D` and
`BOXES_2D` rows of a camera, is the strict player time of the frame (SFF-782) divided by 10^9. The
camera's `timing_method` is `recorded`. The group `TIMESTAMPS` (`synchronized`) of frame f is the mean
of the strict player times of the cameras at frame f, divided by 10^9, with the method
`mean_camera_times`. The 3D, reconstruction and diagnostic rows use the group times.

**SFF-829** (writer) 2D values are pixels of the stored JPEG, in sensor orientation, before
`display_rotation`. The `width` and `height` of each camera image reference are the width and height
of the stored JPEG frames.

**SFF-830** (writer) 3D points of a take with two or more cameras are in millimetres in the
reference frame `calibrated_world`, with the basis `blender_x_right_y_forward_z_up` (+X right, +Y
forward, +Z up, right-handed). A take with one camera uses `camera_plane`, in pixels.

**SFF-831** (writer) The confidence of a 2D point is the component `visibility` of `OVERLAY_2D`,
from 0 to 1. A point that the tracker did not detect on a frame has `x` and `y` null and
`visibility` 0.

**SFF-832** (writer) Each recorded model of the descriptor has `tracker_keypoint_names`,
`tracker_connections` (pairs of tracker keypoint names, to draw the skeleton) and
`segment_topology`: an array of segments, each with `name`, `parent` (a segment name or null),
`proximal` and `distal` (keypoint names). Each name of `tracker_connections` is in
`tracker_keypoint_names`. A writer omits `tracker_connections` when it has no pair
([ADR-W5JC](../decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md)). A take folder
has no `tracker_schema.json`.

**SFF-833** (writer) The file holds each retained run. `selected_run_id` of the processing info
JSON (section 14) names the run to show. The descriptor does not hold it, so a change of the selected
run does not rewrite the Parquet. A new posthoc run gets a new `run_id`. A writer never replaces or
changes a run whose `origin` is `realtime`, with one exception. After a repair, freemocap rewrites
the times of a realtime run: `timestamp_s` of its rows and the values of its `TIMESTAMPS` rows. It
does this when it next opens the take and finds that a timing sidecar has a `# repair` line and a
fit that the run did not use. It changes nothing else of a realtime run
([ADR-E45D](../decisions/entries/E45D-spec-draft-v2-corrections-after-review.md),
[ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-834** (writer) A run from the realtime journal (section 17) has, in the stage provenance
of each sensor group, `origin` = `realtime` and a `coverage` object: `frames_in_take`,
`frames_processed`, `skips` (an object of counts by reason), `journal_crc_rejects`, `clean_close`,
`latency_ms` (`p50`, `p99`) and `events`. The latency of a result is `processed_ns` of its journal
record minus the group time of the frame (SFF-828). `p50` and `p99` are nearest-rank percentiles.
`events` is an array of the event objects of the journal that name this stage, in journal order
([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md)). A posthoc run has `origin` =
`posthoc` and `coverage` null. A skipped frame of a realtime run has `x`, `y` and `visibility` all
null. A realtime run has no checkpoints.

**SFF-835** (reader) A reader gives the take warning `realtime_run` one time when a run has a stage
provenance with `origin` = `realtime`. The reader result holds only the code. The text "Realtime
run: N/M frames processed, causal filters, may contain dropped and extrapolated frames" is guidance
for the program that shows the take. That program shows it for each camera sensor group, where N is
`frames_processed` and M is `frames_in_take` of the `coverage` of the stage `observations`
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-836** (writer) The ChArUco observations of a calibration take are rows of the Parquet,
with the channel kinds of parts/parquet-descriptor.md. They are not in a separate file.

**SFF-837** (reader) When the camera geometry stored in a run (`camera_geometry`) does not agree
with the calibration TOML of the take, a reader uses the stored geometry for that run and gives the
take warning `calibration_mismatch`. The two agree when each of these is true for each camera,
linked by `camera_key`: the image size is equal; `fx`, `fy`, `cx`, `cy`, `k1`, `k2`, `p1` and `p2`
each differ by 1e-6 or less; and the pose relative to the camera with `index` 0 differs by 1e-6 or
less in each value of the rotation matrix and in each value of the translation in millimetres. A
rigid change of the world does not change a relative pose. So an alignment by `person` or `charuco`
gives no `calibration_mismatch`
([ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-838** (writer) freemocap writes the Parquet whole (SFF-786), while it holds
`.processing.lock`, then writes the processing info JSON (section 14), then updates the manifest.

## 17. Realtime journal

freemocap writes the realtime tracking results of a take to `<rec>_realtime_journal.bin` while the
take runs, and folds it into a Parquet run at the end
([ADR-Q9X2](../decisions/entries/Q9X2-realtime-tracking-journal.md)). The journal is a binary file of
framed records. Each multi-byte integer and float in it is little-endian.

| Bytes | Field |
|---|---|
| 4 | `magic`: the ASCII bytes `SKRJ` |
| 4 | `length`: `u32`, the number of bytes of `type` and `payload` |
| 1 | `type`: `u8`, the record type |
| `length` − 1 | `payload` |
| 4 | `crc32`: `u32`, the CRC-32 of the bytes of `type` and `payload` |

Record types:

| `type` | Record | Payload |
|---|---|---|
| 1 | header | UTF-8 JSON (SFF-702): `skellyfileformat` (`"realtime_journal"`), `format_version`, `format_prerelease`, `writer`, `take_uuid`, `origin` (`"realtime"`) and `channels`: an array of channel declarations, each with `channel_index` and the members of a Parquet channel (section 16) |
| 2 | data | `channel_index` (`u16`), `frame_number` (`i32`, the Parquet `frame_number` of SFF-827), `processed_ns` (`i64`, the host-clock time at which the pipeline finished the result, relative to the take start), `n` (`u32`, the number of names), `k` (`u32`, the number of components), then n × k `f32` values in name order, then component order |
| 3 | event | UTF-8 JSON: a parameter change, with `time_ns`, `stage`, `parameter` and `value` |
| 4 | end | UTF-8 JSON: `records` (the number of data records) and `clean_close` (`true`) |

**SFF-839** (writer) The first record of a journal is the header record. A writer writes the
header record before the first data record, and declares each channel before it writes a data record
of that channel.

**SFF-840** (writer) Each record has the fields of the table, with no padding between them. A data
payload has 22 + 4 × n × k bytes. `length` is from 1 to 2^26. A writer writes each record in one
write and flushes it (SFF-787).

**SFF-841** (writer) A data value is `f32`. A missing value is a quiet NaN. The fold writes it as
null (section 16). Each channel of a journal declares the `dtype` `float32`. A journal holds no time
as a data value: a journal header MUST NOT declare a channel of the kind `TIMESTAMPS`.
`frame_number` of a data record is the Parquet `frame_number` of SFF-827: the position of the
multi-camera frame in the camera files of the take. A writer writes no data record for a frame
outside the take ([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md)).

**SFF-842** (writer) The journal holds each result that the realtime pipeline computes: the raw
2D for each camera with its visibility; the filtered 2D where it exists; the raw 3D; the filtered
3D; the skeleton reconstructions; the ChArUco observations; the reprojection diagnostics; and the
parameter-change events (as event records).

**SFF-843** (reader) A reader scans the journal from its start. At each offset it looks for
`magic`. It checks `length` and `crc32`. It uses a record only when both are correct. It skips a bad
record by a scan for the next `magic`. It stops at a torn tail. It reports the number of good
records (`records`), the number of rejected records (`rejected_records`) and `torn_bytes` in the
`folder_files` item of the journal (SFF-885). A rejected record is a record with a correct `magic`
and a wrong `length` or `crc32`. A hole of zeros, for example of 4 KiB, holds no `magic`, so it is
not a rejected record. A journal with one or more rejected records is `damaged` (reason
`crc_mismatch`, also when the cause is a wrong `length`). A
journal with a torn tail, or with no end record, is `unfinished` (SFF-791). When both apply, the
journal is `damaged` (SFF-886). A reader refuses a journal whose header declares a channel with a
`dtype` that is not `float32`, or a channel of the kind `TIMESTAMPS` (state `invalid`, reason
`bad_schema`) ([ADR-E45D](../decisions/entries/E45D-spec-draft-v2-corrections-after-review.md),
[ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-844** (writer) At the end of the take, freemocap folds the journal into a new Parquet run
with `origin` = `realtime` and its coverage block (section 16). freemocap starts the fold only after
`state` of the manifest is `finished` (SFF-724). The one exception is the fold of a left-over
journal as part of a repair that the user agreed to (SFF-793,
[ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).
The fold writes each event record into
`coverage.events` of the stage that the event names, for each sensor group (SFF-834). The fold takes
`timestamp_s` of each
row and the value of each `TIMESTAMPS` row from the timing sidecars of the take (SFF-828), not from
the journal. The fold uses the player times that the sidecars give at the time of the fold. For a
sidecar with no fit, for example after a crash, that time is the arrival time (SFF-781). A later
repair adds a fit to the sidecar, and freemocap then rewrites the times of the run (SFF-833).

**SFF-845** (writer) freemocap deletes the journal only after it has read the new Parquet run
back and compared the count and the digest of the folded values with the journal. The digest is the
SHA-256 of these bytes: for each channel in order of `channel_index`, for each `frame_number` in
increasing order, the n × k values in record order, each as a little-endian float32. When two
records have the same channel and frame, only the last in file order counts. A missing value (NaN in
the journal, null in the Parquet) is the bytes `00 00 C0 7F`. The count is the number of these
values. A null row of a frame with no record is not in the count or the digest
([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md)).
When the fold or the check fails, freemocap keeps the journal. No program folds a journal
automatically at start-up. freemocap folds a left-over journal of an unfinished take only as part of
a repair that the user agreed to (SFF-793). When the user does not agree, freemocap keeps the journal
and changes no file
([ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

**SFF-846** (provisional: the journal load test and the kill test DT11) Before freemocap writes
the journal in a release, a load test runs a full realtime session with the journal writer on and
off and compares the aggregator latency and the dropped frames, and a kill test with real data
passes.

## 18. Blender outputs, annotated videos, exports and logs

These files are in formats of other projects. For each, this section gives the name, the container
and codec, and the content mapping ([ADR-QS7B](../decisions/entries/QS7B-blender-outputs-and-exports.md)).

A name with no run number is always a name of run 0. Each file of a run N other than 0 has `run-<N>`
in its name. Each subsection gives the place of `run-<N>` for its files. A writer does not rename or
replace a file of this section when the selected run changes. `selected_run_id` of the processing info JSON
(section 14) names the selected run ([ADR-E45D](../decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).
Of the files of this section, only the export inventory and the BVH metadata JSON hold the version
fields and the writer string (SFF-707).

### 18.1 Blender

| Path | Content |
|---|---|
| `<rec>.blend` | The Blender scene of run 0 |
| `blender/run-<N>/<rec>.run-<N>.blend` | The scene of run N, for N other than 0 |
| `blender/3d_models/<root>.fbx`, `<root>.bvh` | The rig of run 0 as FBX or BVH, when the user asks for them. `<root>` is `FreeMoCap_<route>`. `<route>` is `parquet_segments` or `parquet_constraints`. |
| `blender/3d_models/<root>.bvh.metadata.json` | The BVH metadata JSON. For a BVH: `format_version`, `format_prerelease`, `writer` (section 3), `import_route`, `run_id`, `sensor_group`, `source`, `missing_sample_policy` and `missing_frames_by_bone` |

A 3D model file of a run N other than 0 is in the folder `run-<N>/` inside `blender/3d_models/`, and
it has `.run-<N>` before the last suffix of its file name.

**SFF-847** (writer) The freemocap Blender addon writes only the files of the table. It writes
no pickle, no `saved_data/`, no `output_data/` file and no `video_export/` file into a take of this
format. It reads the tracking data from the Parquet.

**SFF-848** (provisional: the `.blend` scene contents, future freemocap work) The scene of
`<rec>.blend` has a root empty `FreeMoCap_<route>` with the custom properties `timestamps_s`,
`model_snapshot`, `scene_build_report` and `animation_cleanup`; a rig `<root>_Blender_skeleton_rig`;
a camera `Capture_<camera_label>` for each camera, from the camera geometry of the run, in metres,
with a `calibration` property; a plane with the video of each camera; the camera
`FreeMoCap_overview` and the light `FreeMoCap_light`; and the scene property
`freemocap_source_sha256` (the SHA-256 of the Parquet). The addon rotates each video plane by the
`display_rotation` of its camera.

**SFF-849** (reader) A reader ignores a Blender backup file `<rec>.blend1`. The file is in no list
of the reader result.

### 18.2 Annotated videos

| Path | Content |
|---|---|
| `annotated_videos/<rec>.<camera_label>.annotated.mp4` | A copy of the camera video with the 2D tracking of run 0 drawn on it |
| `annotated_videos/run-<N>/<rec>.<camera_label>.annotated.run-<N>.mp4` | The same for run N, for N other than 0 |

**SFF-850** (writer) An annotated video is H.264 (libx264, `yuv420p`, CRF 18) in MP4, at the
nominal rate of the camera, with one frame for each frame of the camera file, in position order, and
index timestamps. Its frames have the orientation of the stored frames. Its container comment is
`skellycam.video_derivation:` followed by the JSON `{"source_video": <path>, "frame_count": <n>}`.

**SFF-851** (writer) An annotated frame shows the 2D keypoints and the connections of each
tracker of the run, coloured by body region (centre, left, right, hands, face), and the detected
ChArUco corners. It shows no time stamp or frame number.

**SFF-852** (writer) The writer writes an annotated video as
`annotated_videos/.<file name>.partial.mp4`, then renames it. A reader ignores a file whose name starts
with `.`.

**SFF-853** (reader) An annotated video is derived output. A reader of this format does not
read tracking data from it.

### 18.3 Exports

| Path | Content |
|---|---|
| `exports/csv/<prefix>.<table>.csv` | A wide CSV table |
| `exports/csv/<prefix>.tall.csv`, `exports/csv/<prefix>.static.tall.csv` | The tall CSV and its static part |
| `exports/npy/<prefix>.<table>.npy`, `exports/npy/<prefix>.frames.npy`, `exports/npy/<prefix>.timestamps.npy` | NumPy arrays |
| `exports/<prefix>.npz` | All arrays in one ZIP |
| `exports/<prefix>.explorer.ipynb` | A Jupyter notebook that reads the Parquet |
| `exports/<prefix>.export_inventory.json` | The export inventory |
| `exports/calibration_copies/<file>.toml` | Copies of aligned calibrations |
| `exports/README.md`, `exports/csv/README.md`, `exports/npy/README.md` | Guides for people |

`<prefix>` is `<rec>` for run 0, and `<rec>.run-<N>` for a run N other than 0. The exports of each
run are in the same folders: an export has no `run-<N>/` folder. `<table>` is `<label>--<source name after its
first ':'>`, and for `OVERLAY_2D` also `--<camera_label>`. The labels are `2d_overlay`
(`OVERLAY_2D`), `3d_keypoints_raw` (`RAW_KEYPOINTS_3D`), `3d_keypoints_filtered` (`KEYPOINTS_3D`),
`3d_landmarks` (`LANDMARKS_3D`) and `3d_segment_poses` (`SEGMENT_ORIGINS` with `ROTATIONS_WORLD`).

**SFF-854** (writer) A wide CSV is UTF-8 with a byte order mark, comma-separated, with CRLF line
ends and minimal quoting. Its header is `frame_number,timestamp_s,<name>.<component>,…`. The
components are in the order `x,y,z`, or `w,x,y,z` for a quaternion, else the order of the descriptor.
A segment pose has the components `x,y,z,qw,qx,qy,qz`. `OVERLAY_2D` `visibility` is the column
component `confidence`. A null value is `NaN`. A sample that the run does not have is an empty field.
A file holds at most 500,000 rows and 1,024 value columns. A longer table continues in files with
`.rows-<k>` and `.columns-<k>` before `.csv`.

**SFF-855** (writer) An export writes a float32 value in the shortest decimal form that reads
back as the same float32 (for example `0.1`), and a float64 value in the shortest form that reads back
as the same float64. The check of an export compares float32 values as float32.

**SFF-856** (writer) The tall CSV is UTF-8 with a byte order mark. Its columns are those of the
Parquet (section 16), with one column `value` that holds the value of `value` or `value_f64`. The
static file has no `timestamp_s` and no `frame_number` column.

**SFF-857** (writer) Each NPY array of a table has the shape (frames, names, components) and the
`dtype` of its channel, with NaN for a value that is not available. `frames.npy` is int32 and
`timestamps.npy` is float64: the sorted frame numbers of the table and their times. An NPY or NPZ file
holds no object array (SFF-884). The NPZ file holds `<table>.values.npy`, `frames.npy`,
`timestamps.npy` and `recording_info.json`.

**SFF-858** (writer) The export inventory is a JSON file with `format_version`,
`format_prerelease`, `writer` (section 3), `version` (5), `status` (`complete`),
`artifacts` (each export file with `filename`, `location` (`exports`), `sha256`, `rows`, `columns`,
`source_sha256`, `run_id` and `format`), `snapshots` and `csv`. `format` is one of `tall_csv`,
`static_tall_csv`, `wide_csv`, `static_wide_csv`, `npy`, `npz`, `notebook` and `metadata`.
`snapshots` is an object with one snapshot for each `source_sha256`, which is the key. A snapshot has
`revision`, `exported_at` (ISO 8601 UTC text), `recording_id`, `run_id`, `source_sha256`,
`source_file`, `conventions` (`quaternion_order`, `segment_pose` and `missing_values`),
`reference_frames`, `channels`, `selection` and `numpy_timeline`. Each item of `channels` has
`context`, `names`, `components`, `source_components`, `units`, `shape`, `axes`, `missing_values`,
`numpy_key` and `timing` (`frame_count`, `first_frame`, `last_frame`, `first_timestamp_s` and
`last_timestamp_s`). `csv` holds the CSV conventions:
`{encoding, delimiter, absent, null, float_precision, column_order}`. The exporter writes the
inventory last ([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-859** (writer) The exporter writes the exports of one request in `exports/.staging-*/`,
then moves each file to its place, then writes the inventory. It holds `exports/.exports.lock` while it
does this.

**SFF-860** (reader) A reader ignores the files and folders of `exports/` whose names start with
`.`.

### 18.4 Logs

**SFF-861** (writer) A program that writes a log into a take writes it to `logs/<program>.log`, as
UTF-8 text with LF line ends. The content is not specified.

## 19. skellysync folders

A skellysync folder is a take folder with the device pairs of skellysync and a manifest. It has no
info JSON, Parquet or calibration ([ADR-VPD9](../decisions/entries/VPD9-spec-draft-v2-details.md)).

**SFF-862** (writer) (provisional: the skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO)
skellysync writes one camera file and its sidecar for each camera, and,
when its input has audio, one audio file and its sidecar, with the rules of sections 6 to 10. Its
`clock` is `synthetic`. Its `camera_key` can be 0.

**SFF-863** (reader) (provisional: the skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO)
A reader does not give the warning `missing_fit` for a file whose `clock`
is `synthetic`.

## 20. Opening a folder

**SFF-864** (reader) A device pair is a file in the media folder whose name ends in `.csv` and
whose first line is `# skellyfileformat=video_timing` or `# skellyfileformat=audio_timing`, with the
media file of the same stem and the suffix `.mkv` (video) or `.m4a` (audio). A camera file starts with
the EBML magic `1A 45 DF A3`. An audio file has `ftyp` as its first box.

**SFF-865** (reader) A media file of the media folder with no timing sidecar of this format, and a
timing sidecar with no media file, are not in a device pair. A media file alone has no mark of this
format. A reader lists it in `other_files` with the state `not_in_format`. A timing sidecar alone,
with a `take_uuid` that the reader can read, is in the `files` of its take when that take exists
(SFF-866). Its `name` is the path of the missing media file. Its state is `invalid`, with the reason
`missing_media`. It does not count as a camera file or an audio file in SFF-869. When no such take
exists, the item is in `other_files`, with the same state and reason. For each of these files, the
reader gives the folder warning `orphan_file`
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-866** (reader) A reader groups the device pairs by `take_uuid`. A take exists for each
`take_uuid` that one or more device pairs hold. When the folder holds more
than one `take_uuid`, it reports each take and gives the folder warning `multiple_takes`.

**SFF-867** (reader) A manifest belongs to the take whose `take_uuid` it holds. When no
device pair has that `take_uuid`, the reader reports the manifest with the state `invalid` (reason
`take_fact_mismatch`) and rebuilds the links (SFF-731).

**SFF-868** (reader) A reader takes `<rec>` from the manifest. When it rebuilds the links, it
takes `<rec>` from the name of a timing sidecar file. For a camera sidecar, `<rec>` is the name
without the suffix `.<camera_label>.csv`. For an audio sidecar, `<rec>` is the name without the
suffix `.audio.csv`. A take with only an audio sidecar uses the audio sidecar name. When the
sidecars give two values, it gives the take warning `take_fact_mismatch`.

**SFF-869** (reader) When a take has fewer camera files than `group_size`, or fewer audio files
than `audio_count`, the reader reports the take as `incomplete`, with the warning `incomplete_take`,
and it opens the other files. When it has more, it gives the warning `extra_files`.

**SFF-870** (reader) When two camera files of one take have the same `camera_label`, the reader
gives the warning `duplicate_label` and keeps both files.

**SFF-871** (reader) When the timing sidecars of one take disagree on a take key
(SFF-749), the reader gives the warning `take_fact_mismatch` and uses the values of the
camera with the lowest `group_position`.

**SFF-872** (reader) A reader checks the links of the take and reports each check (section 23):

| Check | Rule |
|---|---|
| `take_uuid` | The manifest, each timing sidecar, both info JSONs, the Parquet descriptor and the journal header hold the take's `take_uuid` |
| `camera_key` | The `camera_key` of each manifest camera is in exactly one video sidecar, in `camera_configs` of the capture info JSON, in one camera table of the calibration TOML (when the take has one) and in one camera source of the Parquet (when it has one) |
| `frames` | Each Parquet `frame_number` of a camera is from 0 to the number of rows of its video sidecar minus 1. The finished camera files of the take have the same number of rows |
| `dimensions` | The image width and height of each Parquet camera source are the width and height of the stored JPEG frames of that camera |
| `rotation` | The capture info JSON holds no rotation. The `display_rotation` of the summary agrees with the sidecar |
| `files` | Each path of the manifest, and each file name of the Parquet camera sources, names a file that exists |
| `hashes` | The `sha256` of the manifest calibration is the SHA-256 of the TOML. `parquet_sha256` of the processing info JSON is the SHA-256 of the Parquet |
| `calibration` | The `calibration_uuid` of the manifest is the `calibration_uuid` of the TOML |

`frames` is also `mismatch` when the finished camera files of a take have different numbers of rows
(SFF-754). In an unfinished take, the numbers can differ. A reader then uses the frames from 0 to
the smallest number minus 1 as the multi-camera frames
([ADR-W6HV](../decisions/entries/W6HV-spec-v2-details-part-3.md)).

A check has one part for each pair of files that its rule compares. A reader does not evaluate a
part when a file that the part needs is absent, is `invalid`, or is a file that this reader does not
read. The state of a check is `mismatch` when an evaluated part fails, `ok` when one or more parts
are evaluated and none fails, and `not_checked` when no part is evaluated. So, with no manifest,
`calibration` is `not_checked`, `hashes` has only its Parquet part and `files` has only its Parquet
part ([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-873** (reader) When a camera has `camera_key` 0, a reader links it by `camera_label` and
gives the warning `camera_key_zero`.

**SFF-874** (reader) A `hashes` mismatch of `parquet_sha256` gives the warning
`stale_processing_info`. It does not make the take or the Parquet invalid. (freemocap replaces the
Parquet and the processing info JSON one after the other, and a crash between the two leaves a stale
hash.)

## 21. Legacy folders

The rules of [ADR-CZQ9](../decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md)
apply. This section tells how a reader recognises a legacy folder and what it reports. The code that
reads the old files is in skellycam and freemocap. The informative
[legacy annex](legacy-annex.md) describes the files of each layout.

**SFF-875** (reader) A file of this format is one of these: a timing sidecar with the first line of
SFF-864; a JSON file whose `skellyfileformat` member has a value of this spec; a TOML file with
`[metadata].calibration_uuid`; a Parquet file with a `freemocap.recording` descriptor of
`schema_version` 2; a journal with a header record; and a media file in a device pair. A media file
alone has no mark of this format (SFF-865)
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md)). A folder is legacy when it has no
file of this format, and it has one or more
regular files. A reader then reports the folder state `legacy` and does not change the folder. A
folder with a file of this format and no take is `unreadable` (SFF-888), not legacy. Examples are a
folder with only a timing sidecar of this format, and a folder with only `<rec>_data.parquet` of this
format.

**SFF-876** (reader) A reader reports the family `pre_v1` and the note "freemocap pre-v1 layout,
unsupported" for a folder with one of these: a `SyncedVideos/` or `RawVideos/` subfolder and a
`<name>_config.yaml` or `sessionSettings.txt` file (v0.0.x); or a `synchronized_videos/Camera_NNN.mp4`
file with no `_synchronized` suffix, with `timestamps/Camera_NNN_binary.npy` (v0.1.0).

**SFF-877** (reader) A reader reports the family `v1` for a folder with
`synchronized_videos/*_synchronized.mp4` or `synchronized_videos/timestamps/*_synchronized_binary.npy`.
A legacy folder that is not `v1` and not `pre_v1` has the family `unknown`, with `release_range`
null, `ambiguous` false, and empty `eras` and `warnings`. Version 2.0 does not recognise the layout
of the freemocap development code
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-878** (reader) For a `v1` folder, a reader reports the narrowest release range that the
content proves, from this table. A row matches when each signal of the row is present. "as X" adds
the signals of row X. The rows that say "as" make a chain with the rows that they name: the rows
V1b–V1d and V1b–V1c are one chain, and the rows from V1e–V1h' to V1h' are one chain. Each other row
is a chain of one row. When the matched rows are in one chain, the reader reports the range of the
last matched row, and `ambiguous` is false. When they are in two or more chains, or no row matches,
the reader reports the range from the lowest first release to the highest last release of the
matched rows (v1.0.25 to v1.8.2 when no row matches), and `ambiguous` is true. It does not guess
([ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

| Era | Releases | Signal |
|---|---|---|
| V1a | v1.0.25 to v1.0.34, and the tag `1.1.0` | `output_data/recording_parameters.json` has `mediapipe_parameters_model` with `skip_2d_image_tracking`; `output_data/raw_data/mediapipeBodyWorld_*` |
| V1b–V1d | v1.1.0 to v1.3.0 | `recording_parameters.json` has `mediapipe_parameters_model` with `run_3d_triangulation` and `run_reprojection_error_filtering`; `output_data/raw_data/mediapipe3dData_numCams_*` |
| V1b–V1c | v1.1.0 to v1.1.1 | as V1b–V1d, and `mediapipe_skeleton_segment_lengths.json` |
| V1e–V1h' | v1.3.1 to v1.7.4 | `recording_parameters.json` has `tracking_parameters_model` and `run_reprojection_error_filtering`; `mediapipe_skeleton_3d.npy` or `mediapipe_2dData_*`; a body CSV whose first column is `body_nose_x` |
| V1f–V1h' | v1.5.0 to v1.7.4 | as V1e–V1h', and `<name>_by_frame.csv` |
| V1g–V1h' | v1.6.0 to v1.7.4 | as V1f–V1h', and a TOML whose `cam_0` rotation is 0 |
| V1h–V1h' | v1.7.0 to v1.7.4 | as V1g–V1h', and a TOML with `world_position`, `groundplane_calibration` or a board `name` |
| V1h' | v1.7.4 | as V1h–V1h', and a `reprojection_error` column in `<name>_by_frame.csv` |
| V1i | v1.8.0 to v1.8.2 | `recording_parameters.json` has `use_triangulate_outlier_rejection` |

The tag `1.1.0` (with no `v`) is not the release v1.1.0. It is v1.0.34 with one more log line. For a
V1a folder, a reader reports the range v1.0.25 to v1.0.34. The release v1.1.0 starts era V1b.

**SFF-879** (reader) For a `v1` folder, a reader gives each warning of this table whose range
overlaps the reported range:

| Warning | Range | Defect |
|---|---|---|
| `legacy_fake_confidence` | v1.0.25 to v1.0.34 | The 2D third channel is z × width, not a confidence |
| `legacy_marker_order` | v1.1.0 | The hands and the face are mislabelled (marker order) |
| `legacy_nonrigid_alignment` | v1.0.25 to v1.5.4 | The alignment to camera 0 is not a rigid transform |
| `legacy_calibration_unverified` | v1.0.25 to v1.8.2 | The TOML of the folder is not certain to be the calibration of the 3D data |

**SFF-880** (reader) Only to read a `v1` folder, a reader looks for the calibration TOML by
the rule of v1: `<folder name>_camera_calibration.toml`, else the one `.toml` file with
`calibration` in its name. When there are two or more, it reports the calibration as `ambiguous` and
uses none. The member `calibration` of `legacy` (SFF-885) holds the result: `{path, state}`, with
the state `present`, `missing` or `ambiguous`. `path` is null when the state is not `present`.

## 22. Privacy and safety

The rules of [ADR-T8PK](../decisions/entries/T8PK-privacy-notice-and-no-code-in-files.md) apply.
Private data is allowed in any field.

**SFF-881** (writer) The manifest member `privacy` is an object with `fields` and
`media_shows_people`. `fields` is an array, sorted by `file` and then by `field`. Each item has
`file` (a path), `field` (a JSON pointer, a TOML key path or a CSV header key) and `kind`:
`device_name`, `serial_number`, `device_path`, `user_entered_name`, `absolute_path`, `time_zone` or
`other`. `fields` holds exactly the fields of this table, when the file exists and the value is not
null. `<key>` is a key of `camera_configs`, and `<i>` is an index of the summary `cameras`.
`media_shows_people` is `true` when the take has a camera file, an audio file or a Parquet
([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md); the kinds of the manifest fields:
[ADR-1HH0](../decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

| File | Field | Kind |
|---|---|---|
| The capture info JSON | `/camera_configs/<key>/user_name` | `user_entered_name` |
| | `/camera_configs/<key>/device/model` and `/camera_configs/<key>/device/os_name` | `device_name` |
| | `/camera_configs/<key>/device/serial` | `serial_number` |
| | `/camera_configs/<key>/device/port_path` | `device_path` |
| | `/audio/device_name` | `device_name` |
| Each timing sidecar | `utc_offset_min` | `time_zone` |
| The manifest | `/recording_name` | `user_entered_name` |
| | `/summary/cameras/<i>/user_name` | `user_entered_name` |
| | `/summary/cameras/<i>/model` | `device_name` |
| The calibration TOML | `metadata.alignment_recording_id` | `user_entered_name` |

**SFF-882** (writer) Each writer that writes a field of the table of SFF-881 adds it
to the `privacy` list when it writes the manifest.

**SFF-883** (reader) The reader result has `may_contain_private_data` = true when the
`privacy` list has one or more items or `media_shows_people` is true. When the manifest is missing, it
is true when the take has a camera file, an audio file or a Parquet.

**SFF-884** (writer, reader) No file of the take folder uses a format whose loading runs code,
for example Python pickle. A NPY or NPZ file holds no object array. A reader never runs the content of
a file, and it loads NPY and NPZ files with pickles not allowed. A reader finds a pickle by the name
suffix `.pkl` or `.pickle`, in any case, in the root and the media folder. It lists the file in
`other_files` with the state `invalid` and the reason `code_in_file`. For each NPY or NPZ file that
the manifest lists, a reader reads only the NPY header. A `descr` of an object type makes the
`folder_files` item `invalid`, with the reason `code_in_file`
([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)).

## 23. The reader result

A reader can give the result of opening a folder as JSON. The conformance tests and the golden files
use this result to compare readers
([ADR-KW3G](../decisions/entries/KW3G-reader-result-for-the-folder.md)).

**SFF-885** (reader) The reader result is a JSON object with these members, serialised with the
JSON Canonicalization Scheme (RFC 8785):

- `result_version`: 2;
- `folder_state`: `ok`, `unreadable`, `legacy` or `empty` (SFF-888);
- `folder_warnings`: an array of warning codes;
- `takes`: an array, in order of `take_uuid`. Each take has `take_uuid`, `recording_name`, `state`
  (`complete` or `incomplete`), `manifest` (`present`, `missing` or `invalid`), `warnings`,
  `may_contain_private_data`, `files`, `folder_files` and `links`;
- each item of `files` (a media file and its sidecar, or a timing sidecar alone, SFF-865): `name`
  (the path of the media file, relative to the take folder, with `/`), `kind` (`camera` or `audio`),
  `state`, `reason`, `camera_key`, `camera_label`, `rows` (the number of data rows that SFF-746 lets
  the reader use), `torn_bytes`, `fit` (true only when the sidecar holds fit lines and the reader
  uses them; false when the reader computes a fit, SFF-784), `warnings` and, when the test asks for
  them, `records`. An audio item has `camera_key` and `camera_label` null. An item with the state
  `invalid` or `unsupported_version` has `rows`, `torn_bytes` and `fit` null. Its `camera_key` and
  `camera_label` are the header values when their form is correct, else null;
- each item of `records`: `[position, source_frame_number, arrival_ns, sample_ns, player_ns]` for a
  camera, and `[block, first_sample, n_samples, host_ns, fitted_ns]` for audio. An absent value is
  null. For an unfinished camera file, `records` holds only the usable frames (SFF-740);
- each item of `folder_files`: `path`, `role`, `state` (`present`, `missing`, `invalid`,
  `not_checked`, `unsupported_version`, `unfinished` or `damaged`), `reason` and `warnings`.
  `folder_files` has one item for each `files` item of the manifest, one for `calibration.file`, and
  one for each root file with a fixed name of SFF-731 that exists. An item is `missing` only when
  the manifest names a path that does not exist. In a rebuild, the list holds only the files that
  the reader finds. The item of the journal also has three integer members: `records` (the number of
  good records), `rejected_records` and `torn_bytes` (SFF-843). Each of the three is null when the
  journal is `not_checked` (SFF-892);
- each item of `links`: `check` (a name of SFF-872), `state` (`ok`, `mismatch` or `not_checked`)
  and `detail`. `detail` is null in the canonical result. A reader can give a text outside the
  result. `links` holds each check of SFF-872 one time, in the order of that table;
- `other_files`: an array of the files of the root and the media folder that are in no take, each
  with `name` (a path relative to the take folder, with `/`), `state` and `reason`. A file whose
  name ends in `.tmp` or starts with `.`, and `<rec>.blend1`, is in no list of the result;
- `legacy`: null, or an object with `family` (`v1`, `pre_v1` or `unknown`), `release_range` (null,
  or an array of two release names, for example `["v1.3.1","v1.7.4"]`), `ambiguous`, `eras` (an
  array of the Era cells of the matched rows of SFF-878, in table order, with `-` in place of the
  dash, for example `"V1e-V1h'"`), `warnings` and `calibration` (SFF-880).

Each member that the list names is present. A member that does not apply is null. A code is at most
one time in a `warnings` array. Times are relative
to the take start, as JSON numbers. They can be negative. Each integer member is a JSON number:
`result_version`, `rows`, `torn_bytes`, `records` and `rejected_records` of the journal item, and
each integer of the `records` of a `files` item (a position, a source frame
number, a sample index, a number of samples and a time). No integer member is a JSON string
(SFF-702). `camera_key` is a text, not an integer
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md),
[ADR-0XX2](../decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-72QQ](../decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-886** (reader) The file states are `unsupported_version`, `invalid`, `damaged`,
`unfinished`, `repaired`, `finished` and `not_in_format`. When two apply, the reader reports the first
in this order: `unsupported_version`, `invalid`, `damaged`, `unfinished`, `repaired`, `finished`. A
file that this spec makes a reader refuse is `invalid`, with one reason code. These are the states of
the items of `files` and `other_files`. A folder file has the states of SFF-885. When two of
`unsupported_version`, `invalid`, `damaged` and `unfinished` apply to a folder file, the reader
reports the first in the same order. A folder file with a `major` that the reader does not know is
`unsupported_version` (SFF-708). Of the folder files, only the journal is a live file (SFF-787):
`unfinished` and `damaged` are states of the journal (SFF-843).

**SFF-887** (reader) The reason codes are `bad_metadata`, `missing_metadata`, `bad_rate`,
`bad_rotation`, `bad_label`, `bad_time`, `crc_mismatch`, `take_fact_mismatch`, `missing_media` (a
timing sidecar with no media file, SFF-865), `bad_schema` (a JSON, TOML or Parquet file, or a journal
header, without the members or the columns of its section, or a journal header with a channel that
SFF-843 refuses; int64 in the Parquet columns `frame_number` and `run_id` is
not a cause, SFF-819) and `code_in_file`. Each reader makes a file `invalid` with `bad_time` when a
row time or a fitted time has a magnitude of 2^53 ns or more. The take warnings are
`incomplete_take`, `duplicate_label`, `take_fact_mismatch`, `extra_files`, `manifest_missing`,
`camera_key_zero`, `stale_processing_info`, `summary_stale`, `calibration_mismatch`
and `realtime_run`. The file warnings are `missing_fit`, `encode_skip` and `prerelease`. A reader
gives the file warning `encode_skip` when one or more usable rows have that flag. The folder
warnings are `multiple_takes`, `stray_tmp` and `orphan_file`. The legacy warnings are those of
SFF-879. A reader reports each
code that this spec names, and no other
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md),
[ADR-ATW0](../decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-888** (reader) `folder_state` is `ok` when the folder has one or more takes,
`unreadable` when it has no take but one or more files of this format, `legacy` by SFF-875, and
`empty` when it has no regular file.

**SFF-889** (reader) A file of this format (SFF-875) whose `take_uuid` a reader can read is in
the `files` of its take, also when it is `invalid`. A folder file is in the `folder_files` of its
take. Other files are in `other_files`. A folder file of this format with no take is in
`other_files` with the state `invalid` and the reason `take_fact_mismatch`. Each file of this format
that is alone gives the folder warning `orphan_file` (SFF-865)
([ADR-Q4BK](../decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-890** (reader) Takes are in order of `take_uuid`. The camera files are in order of
`group_position`, then by the bytes of the file name, and the audio file is last. `folder_files` and
`other_files` are in order of the bytes of the path. `links` is in the order of the table of
SFF-872. Each `warnings` array is sorted by code point.

**SFF-891** (reader) The Python and JavaScript readers of this package read a file with
`format_prerelease` > 0 and give it the warning `prerelease`. Another reader MAY refuse it as
`unsupported_version`.

**SFF-892** (reader) The JavaScript reader of this package reads the media files, the timing
sidecars and the JSON files. In its result, each `folder_files` item of the TOML, the Parquet and the
journal has the state `not_checked`. With the parts of SFF-872, it gives `not_checked` for the link
checks `frames`, `dimensions`, `hashes` and `calibration`. It evaluates `take_uuid`, `camera_key`,
`rotation` and `files` on the files that it reads. The byte-for-byte comparison of the Python result
and the JavaScript result leaves out a check that is `not_checked` in the JavaScript result
([ADR-DM9S](../decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-893** (reader) This requirement belongs to section 16. The reader of this package checks the
structure of each `RecordedModel` of the descriptor and of its nested types, as
parts/parquet-descriptor.md section "Structure rules and writer rules" gives it: each member is
present, except a member that its row lets the writer omit; each member has its JSON type; and a
closed type has no other member. A structure fault makes the `folder_files` item of the Parquet
`invalid`, with the reason `bad_schema`. In version 2.0, the reader does not check a writer rule of
the part: it does not refuse a model that breaks only a writer rule
([ADR-W5JC](../decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md) item 3).

## Appendix A. Golden folders

Gate 2 makes these folders. Each is committed with its SHA-256 sums and the script that made it,
from synthetic frames and pinned tools. Each has the reader result of SFF-885, with records, as
a committed JSON file.

| # | Golden folder | Sections |
|---|---|---|
| G1 | A capture-only take: 2 cameras of about 90 frames at a small size, one with a gap, both with a fit; audio of 3 s, mono, with a click every 500 ms. Each camera shows a flash at the time of each click. The take holds the capture info JSON, which skellycam writes at the take start (SFF-801) | 4 to 11, 13 |
| G2 | G1 with stereo audio | 9, 10 |
| G3 | A processed take: G1 plus the processing info JSON, a calibration TOML, a Parquet with 2D and 3D, and the exports. The Parquet has a model with connection pairs and a model with no connection pair | 14 to 16, 18 |
| G4 | A rotated camera: `display_rotation` 0, 90, 180 and 270, with coloured corner markers and the expected upright corner colours | 6, 8 |
| G5 | A crashed take: unfinished camera files and sidecars (a clean cut, a torn row of 37 bytes, a row with a wrong CRC), an unfinished audio file (a clean kill and a torn fragment), a `.tmp` manifest and the old manifest | 12 |
| G6 | G5 after repair, and G5 with an interrupted repair | 12 |
| G7 | Two copies of G3: one with its manifest deleted, and one whose manifest has another `take_uuid` | 5, 20 |
| G8 | A renamed take folder: a copy of G3 in a folder with another name | 4, 16, 20 |
| G9 | Mismatch vectors: `take_uuid`, `camera_key`, a Parquet frame range, finished camera files with different numbers of rows, image dimensions, a rotation in `camera_configs`, an unresolved file name, a stale `parquet_sha256`, a calibration hash, a `calibration_uuid`, a Parquet with a wrong `recording_id` | 16, 20 |
| G10 | Version vectors: a higher `minor` with an unknown header key and an unknown column in a timing sidecar, and with an unknown member in a JSON file; an unknown `major` in a timing sidecar, and in a folder file; `format_prerelease` > 0 | 3 |
| G11 | Header and row error vectors: an integer with a leading zero; a `+` sign; a row integer of 2^53; a `nominal_rate` of 0/1 and of 2^20 + 1; a `display_rotation` of 45; a bad label; a missing header key | 2, 7, 8 |
| G12 | Fit vectors: two video segments; a source frame gap; a `period_ps` with a remainder; an audio fit with `period_fs`; a sidecar with no fit; two rows with equal fitted times; a row with the flag `encode_skip` | 8, 11 |
| G13 | A realtime take in the state after the fold and before the verified delete of the journal: a complete small take (2 camera files, their timing sidecars, a manifest and both info JSONs) that also holds a realtime journal (good records, a record with a wrong CRC, a 4 KiB zero hole, a torn tail) and the Parquet run of its fold | 5 to 8, 13, 14, 16, 17 |
| G14 | A calibration take and a motion-capture take that holds a copy of its TOML; a library TOML outside a take | 15 |
| G15 | Legacy folders: one v1 folder of each era signal; a v1 folder whose signals are in two chains; a v1 folder with no era signal; a v0.0.x folder; a v0.1.0 folder; a folder of MP4 files only (the family `unknown`) | 21 |
| G16 | Files with code: a pickle (`.pkl`) in the take folder; an NPY with an object array that the manifest lists | 22 |
| G17 | (provisional) A skellysync folder | 19 |

## Appendix B. Player guidance (informative)

This appendix is not normative. It gives the methods that the skellycam player harness used to keep
audio and video in sync to within 0.24 ms over a 60-minute take.

- Use the audio output timestamp (`AudioContext.getOutputTimestamp()`) as the clock. `currentTime`
  of an `AudioContext` or of an `<audio>` element runs 40 to 57 ms late.
- Decode the audio in windows of about 1 s with the WebCodecs `AudioDecoder`. Give the input
  timestamps on the timeline of the file, which includes the pre-skip, and place each output by its
  timestamp. Do not subtract the pre-skip a second time.
- After a seek, start decoding about 80 ms (4 packets) before the target, and discard that audio.
- Do not use `decodeAudioData` for long files.
- Find the fragments of the audio file by a walk of its `moof` boxes. Do not remux the file to plain
  MP4: a file with no `moof` cannot be indexed this way.
- VLC ignores the Opus pre-skip in MP4 and plays the audio about 6.5 ms late. This is accepted.
