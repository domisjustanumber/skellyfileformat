# skellyspecs recording format specification

Status: **draft v2 (the whole take folder)**. Gate 1 closed on 2026-11-16. The user approved
gate 2 for stage 1 on 2026-11-17
([ADR-N1AM](decisions/entries/N1AM-gate-2-approval-of-stage-1.md),
[AGENTS.md section 3](AGENTS.md#3-project-rules)). This repository holds no implementation: each
program that uses the format implements it ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)). No format version is released yet. Draft v1
(the MCAP profile) was withdrawn before gate 1, because the freemocap Blender addon needs real video
files ([ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). Draft v0 (MKV
with binary sidecars) was withdrawn earlier. Their IDs stay in section 0, marked withdrawn. A
requirement marked `(provisional)` names the open item that it waits for
([open-work.md](decisions/open-work.md)).

This specification is normative, with its part [parts/parquet-descriptor.md](parts/parquet-descriptor.md).
The [legacy annex](legacy-annex.md) and Appendix B are informative. The license of the spec text is
Apache-2.0 ([LICENSE](../LICENSE)).

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

The spec defines each file in full. It does not leave a part of a file to the code of the program
that writes it ([ADR-2C9V](../decisions/entries/2C9V-whole-take-folder-scope-and-package.md) item 2).

An agent proposed the details that the decisions of the user do not fix (names, columns, keys and
values) in spec draft v2. The user accepted them at gate 1
([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md),
[ADR-3D33](decisions/entries/3D33-spec-draft-v2-details-folder-files.md);
[ADR-G9ER](decisions/entries/G9ER-consolidation-of-the-pushed-entries.md) supersedes both).

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
| repaired file | An unfinished file that a repair changed into a finished file (section 12), or a file that the program that recorded the take completed (SFF-894). |
| `missing` row | A row of a video sidecar with the flag `missing`: the camera gave no usable frame for it (SFF-756). |
| placeholder | The black JPEG in the block of a `missing` row (SFF-756). |
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
- **The draft form.** A requirement or a test that waits for gate 1 has the word "Draft" before its
  ID, for example `**Draft SFF-896**`. Its ID is reserved: no other requirement or test gets it. The
  tools of `tools/` do not read it as a requirement or a test. A draft test is not in the stage
  table of conformance.md, and it has no runnable test. A heading comes between the last test that
  is not a draft and the first draft test, so that the `Checks:` line of a draft test belongs to no
  other test. At gate 2, the word "Draft" goes, and the runnable tests and the stage rows come in
  the same commit ([ADR-91PB](decisions/entries/91PB-choices-for-the-v1-camera-file-rules.md)
  item 2).
- A provisional requirement has `(provisional)` after its ID and names the open item that it waits
  for. A provisional requirement must be closed before v2.0.0.
- `(writer)` or `(reader)` after an ID tells which program the requirement applies to.
- Each requirement has one or more tests in [conformance.md](conformance.md).
  `tools/check_spec_traceability.py` checks this.
- ⌊a / b⌋ is integer division rounded down, for a ≥ 0 and b > 0.
- A path in this spec is relative to the take folder and uses `/`.
- Note (informative): the principle of this spec is one fact, one home. The home of a fact is the
  file whose section states it. The other files hold `take_uuid` and `camera_key` as link keys. The
  manifest `summary` is the one informative copy (SFF-728). The home of the stored resolution, the
  actual frame rate and the frame counts (also the gaps and the fills) is the camera file and its
  timing sidecar ([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md) item 2,
  [ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) item 5). This note
  adds no requirement. When a requirement names a copy of a fact in another file, that requirement
  applies, for example the TOML `size` (SFF-808), the Parquet image reference (SFF-829),
  `coverage.frames_in_take` (SFF-834) and each copy of `camera_label`.

**SFF-700** (writer, reader) Each timing sidecar, JSON file and TOML file of this format, and each
JSON record of the journal, is UTF-8 with no byte order mark and with LF line ends. The exports of
section 18 have their own rules.

**SFF-701** (writer, reader) An integer in a CSV field or in a CSV header value is written in
decimal, with a `-` sign when it is negative, with no `+` sign, no leading zeros (except the value
`0`) and no spaces. A reader refuses a file with an integer in another form (reason `bad_metadata`).
In a data row, each integer that is not a time is from 0 to 2^53 − 1. A reader refuses a file with
another value (reason `bad_metadata`)
([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-702** (writer, reader) A JSON file is RFC 8259 JSON with one object at the top. In it, each
integer that can be outside the range −2^53 to 2^53 is a JSON string in the form of SFF-701. Other
integers are JSON numbers. In version 2.0, no member of a JSON file is an integer in a string,
because each time in a JSON file is relative to the take start. A writer writes the members in the
order that this spec lists them. A writer writes a JSON number with an integer value with no
fraction and no exponent (`30`). It writes each other number in the shortest decimal form that reads
back as the same float64, as RFC 8785 gives it (`29.97`)
([ADR-PVG8](decisions/entries/PVG8-spec-v2-details-part-10.md) item 24a,
[ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 38d). A reader accepts each
white space that RFC 8259 allows
([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 5).

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

The rules of the README section [Versioning](README.md#versioning-normative) apply
([ADR-9DV4](decisions/entries/9DV4-format-version-from-freemocap.md)). The format version is the
`major.minor` of the freemocap release that last changed any file of the folder.

**SFF-707** (writer) These files record the format version as `format_version` (the text
`major.minor`, for example `2.0`) and `format_prerelease` (an integer): the manifest, each timing
sidecar, the capture info JSON, the processing info JSON, the calibration TOML, the descriptor of the
Parquet, the header record of the journal, the export inventory and the BVH metadata JSON
(section 18). No other file of section 18 records the format version or a writer string
([ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)). `major`, `minor` and
`format_prerelease` are integers from 0 to 65,535. The section of
each file gives the place of these fields. A media file is a standard file with no added field: a
writer writes no version field and no writer string of this format into a camera file or an audio
file. The timing sidecar of a device pair holds the format version and the writer string for its
media file ([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).

**SFF-708** (reader) A reader MUST refuse a file with a `major` that it does not know (state
`unsupported_version`). It does not report the file as legacy.

**SFF-709** (reader) A reader MUST read a file with a higher `minor` of a `major` that it
knows. It ignores the header keys, columns, JSON members, TOML keys, flag bits and record types that
it does not know. In a camera file and an audio file, a reader ignores each Matroska element and
each MP4 box that this spec does not name ([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md)
item 3).

**SFF-710** (writer) A writer writes only the latest format version. Before v2.0.0 is
released, a writer writes `2.0` and the `format_prerelease` of the current draft. This requirement
is the only place that gives the value. The value is 1 until the draft goes to external review. An
internal draft change does not change it. From that review on, each revised draft that goes to the
reviewers adds 1 to the value. The value of this draft is 1. A released writer of 2.0 writes
`format_prerelease` = 0. A reader treats each value above 0 in the same way (SFF-891)
([ADR-0JVZ](decisions/entries/0JVZ-spec-v2-details-part-9.md) item 20, [ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 8).

**SFF-711** (reader) A reader MAY refuse a file with `format_prerelease` > 0.

**SFF-712** (writer, reader) Each file that SFF-707 names holds a writer string `writer`, for
example `skellycam 2.1.3`. A media file holds none: the `writer` of its timing sidecar is the writer
string of the device pair. A reader MUST NOT change its behaviour because of a writer string.
skellysync writes the format version that this spec gives.

**SFF-713** (reader) The version of a container (the Matroska `DocTypeVersion`, the MP4
brands, the Parquet format version) is not the format version. A reader does not use it as the
format version.

**SFF-714** (reader) A reader uses a field or a rule only when the `minor` of the file is equal
to or higher than the minor version that added it. In version 2.0, every field and rule of this spec
has minor 0.

## 4. The take folder: layout and names

A take folder has this layout ([ADR-5XNA](decisions/entries/5XNA-folder-layout-names-and-manifest.md)).
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
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)).

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
subfolders for files of this format. The only exceptions are the legacy recognition of section 21
(SFF-875, [ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 5)
and the reads of the camera files and the time files of a v1 folder (SFF-896 to SFF-903,
[ADR-91PB](decisions/entries/91PB-choices-for-the-v1-camera-file-rules.md) item 12).

**SFF-722** (writer) A writer of this format does not write `synchronized_videos_README.md`.

## 5. The recording manifest

The manifest `recording_manifest.json` links the files of the take
([ADR-5XNA](decisions/entries/5XNA-folder-layout-names-and-manifest.md)). It is a JSON file
(SFF-702) with these members, in this order:

| Member | Value |
|---|---|
| `skellyspecs` | `"recording_manifest"` |
| `format_version`, `format_prerelease` | The format version (section 3) |
| `writer` | The writer string of the program that wrote this version of the file |
| `take_uuid` | The ID of the take (SFF-703) |
| `recording_name` | `<rec>` |
| `purpose` | `"motion_capture"` or `"calibration"` |
| `state` | `"recording"` while the capture writer records, `"finished"` after it ends the take or after a repair (SFF-793). It has no other value. |
| `cameras` | An array, in order of `group_position`. Each item: `camera_key`, `camera_label`, `group_position`, `video` (path of the camera file), `timing` (path of its CSV), `calibration_camera` (the name of its camera table in the calibration TOML, or null) |
| `audio` | null, or an object with `audio` (path of the audio file) and `timing` (path of its CSV) |
| `calibration` | null, or an object with `calibration_uuid`, `file` (`<rec>_camera_calibration.toml`) and `sha256` (64 lowercase hexadecimal characters of the SHA-256 of the file) |
| `files` | An array of the other files of the take, in order of `path`. Each item: `path`, `role`, `owner` (`skellycam`, `freemocap` or `blender_addon`), `sha256` (a SHA-256 or null, SFF-723) |
| `warnings` | An array of warning objects (SFF-727) |
| `privacy` | The privacy list (section 22) |
| `summary` | The informative overview (SFF-728) |

The roles of `files` are `capture_info`, `processing_info`, `tracking`, `realtime_journal`, `blend`,
`blender_output`, `annotated_video`, `export` and `log`. The reader result also has the role
`calibration`, for the file that `calibration.file` names (SFF-885). It is not a role of `files`
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 3).

**SFF-723** (writer) The manifest has each member of the table, in the order of the table. Each
path is relative to the take folder, with `/`. `sha256` of a `files` item is the SHA-256 of the file
(64 lowercase hexadecimal characters) for the roles `capture_info`, `processing_info`, `blend`,
`blender_output` and `annotated_video`. It is null for the role `tracking` (the home of that hash is
`parquet_sha256`, section 14), for the role `export` (the home is the export inventory) and for the
roles `realtime_journal` and `log`
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-724** (writer) The capture writer writes the manifest before it writes the first frame or
sample of the take, with `state` = `"recording"`. It lists each camera and the audio file that it
starts. It writes the manifest again after it closes the last media file, with `state` =
`"finished"` and the warnings of SFF-727. For each write, it reads the manifest (when the file
exists), changes it and writes it while it holds `.processing.lock` (SFF-789). It keeps each member
and each item that freemocap owns
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-725** (writer) freemocap updates the manifest when it adds, replaces or deletes a file of
the take. It reads the manifest, changes it and writes it while it holds `.processing.lock`
(SFF-789). It keeps each member and each item that skellycam owns, and each member that it does not
change. It sets `writer` to its own writer string.

**SFF-726** (writer) Each write of the manifest replaces the whole file (SFF-786).

**SFF-727** (writer) Each item of `warnings` has `code`, `source` (`skellycam` or `freemocap`),
`camera_key` (or null) and `detail` (a text for people, or null). skellycam writes
`camera_gap` (a camera has one or more gaps), `control_mismatch` (a control reads back a value that
differs from the value that it set) and `awb_not_settled` (auto white balance did not settle before
the take). A repair adds `camera_gap`, with the `source` of the program that did the repair
(SFF-793). A program adds its warnings. It does not remove the warnings of another program.
skellycam also writes `camera_dead` (a camera stopped during the take; its sidecar holds `missing`
rows to the end of the take), `camera_file_short` (the camera file ends early, SFF-754) and
`take_error` (an error ended the take). The `detail` of `camera_dead` is
`last_frame=<p> reason=<text>`, where p is the position of the last row that is not `missing`, or
`none`. The `detail` of `camera_file_short` is `blocks=<b> rows=<r>`: the number of blocks of the
camera file and the number of rows of its sidecar. The `detail` of `take_error` is the error text,
and its `camera_key` is the camera of the error, or null. A write error gives `camera_file_short`
and `take_error`, and no `camera_dead`. A reader parses the two `detail` forms as SFF-895 gives
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 5).

**SFF-728** (writer) The `summary` member is an informative overview for people. It holds:
`take_start_utc` (ISO 8601 UTC text); `duration_s`; `cameras` (each with `camera_label`, `user_name`,
`model`, `stored_px` (`"<width>x<height>"`), `display_rotation`, `nominal_fps`, `gaps`, `filled`,
`missing` and `exposure_us`, a number or null); `audio` (null, or `{file, sample_rate, channels, duration_s}`);
`calibration` (the `calibration_uuid` and the source take); `processing_runs` (each item is
`{run_id, origin, recorded_at}`, with the latest `recorded_at` of the stage provenances of the run);
and `warnings` (the codes of the manifest `warnings`, each one time, sorted). The writer of the
manifest computes the summary from the files
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)). The values are
([ADR-PVG8](decisions/entries/PVG8-spec-v2-details-part-10.md) item 24):

- `nominal_fps` and each `duration_s` are JSON numbers (SFF-702): an integer number of thousandths,
  divided by 1000. So each has at most 3 decimal places.
- `nominal_fps` is ⌊(2000 × `num` + `den`) / (2 × `den`)⌋ thousandths, where `num/den` is the
  nominal rate (rounded half up).
- `take_start_utc` is `take_start_utc_ns` as `YYYY-MM-DDTHH:MM:SSZ`, rounded down to the second.
- `duration_s` of the take: ns is the largest `arrival_ns` of the last row that holds an
  `arrival_ns` of each video sidecar
  ([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).
  The value is ⌊(ns + 500,000) / 10^6⌋ thousandths. A take with no camera uses the audio value. A
  take in which no video sidecar holds an `arrival_ns` also uses the audio value, or null when it
  has no audio ([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 5).
- `duration_s` of `audio` is `samples` of the `# end` line divided by `sample_rate` of the header,
  rounded half up to thousandths. After a repair, `samples` of the `# end` line counts only the
  samples of the kept rows (SFF-769, SFF-795).
- `cameras` is in order of `group_position`. `user_name` and `model` are `user_name` and
  `device.model` of the camera config (section 13), so the text rule of `user_name` also applies
  here. `exposure_us` is `controls.exposure_us.value`
  of that config, or null. `stored_px` is the size of the first stored JPEG that is not a
  placeholder, or the mode size of SFF-756 when there is none ([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 5; "that is
  not a placeholder", [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 12). `gaps`,
  `filled` and `missing` are the counts of the `# end` line (`missing`:
  [ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).
- `audio.file` is the path of the audio file.
- `calibration` is null, or `{calibration_uuid, source_take_uuid}` from the TOML.
  `source_take_uuid` is null when the TOML has none.
- `processing_runs` is in order of `run_id`. `origin` is `realtime` when a stage provenance of the
  run has that origin, else `posthoc`. `recorded_at` is the unchanged text of the latest stage
  provenance.
- In a manifest with `state` `recording`, each `duration_s`, `stored_px`, `gaps`, `filled` and
  `missing` is null.

**SFF-729** (reader) A reader MUST NOT use a value of `summary` for processing. When
`summary` does not agree with the home of a value, the home wins, and a reader gives the take
warning `summary_stale`. A reader gives this warning when `camera_label`, `display_rotation` or
`nominal_fps` of a summary camera differs from the timing sidecar of the camera, or when `gaps`,
`filled` or `missing` differs from the `# end` line of a finished or repaired sidecar (`missing`:
only when both hold it, [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 11;
[ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1). For `nominal_fps`, the
reader compares the thousandths of SFF-728. A sidecar that the reader refuses (state `invalid`) is
not in this comparison (SFF-871).

**SFF-730** (reader) A reader uses the manifest to find the files of the take. It checks
each link against the files (section 20). It does not check `sha256` of a `files` item.

**SFF-731** (reader) When `recording_manifest.json` is missing, is not valid JSON, is not a
manifest of this format, or holds another `take_uuid` than the take (SFF-867), a reader rebuilds
the links of the take by a scan. It finds the device pairs in the media
folder by their content (section 20). It takes `<rec>` from the timing sidecars (SFF-868). Then it
tests these exact names in the root: `<rec>_info.json`, `<rec>_recording_info.json`,
`<rec>_camera_calibration.toml`, `<rec>_data.parquet`, `<rec>_realtime_journal.bin` and
`<rec>.blend`. It does not match a suffix
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)). The `role` of each file that it
finds comes from its fixed name: `capture_info`, `processing_info`, `calibration`, `tracking`,
`realtime_journal` and `blend`, in the order of the names above
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 5,
[ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 4). The scan does not
find the files of the other subfolders (SFF-721). Each rebuild gives the take
warning `manifest_missing`, also when the take member `manifest` is `invalid` (SFF-867). The
reader does not write a manifest. A program can offer to write a new manifest
([ADR-5XNA](decisions/entries/5XNA-folder-layout-names-and-manifest.md) item 8).

## 6. Camera files

A camera file is a Matroska file ([RFC 9559](https://www.rfc-editor.org/rfc/rfc9559)) with DocType
`matroska` ([ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). It
holds no version field and no writer string of this format: its timing sidecar holds them (SFF-707).

**SFF-732** (writer) A camera file has exactly one track: a video track with CodecID `V_MJPEG`
and a track number below 128. It has no other track.

**SFF-733** (writer) Each block holds one JPEG image (a frame or a placeholder) in one
`SimpleBlock` with the keyframe flag. No block is laced. The blocks are in position order
([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 11).

**SFF-734** (writer) A capture writer stores the JPEG bytes that an MJPEG camera sent,
unchanged. For a camera that sends raw frames, it encodes each frame to JPEG
([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md)). It does not capture H.264. It
refuses a request for H.264 capture. There are two exceptions to "unchanged": (1) the block of a
`missing` row is the placeholder of SFF-756; (2) when the camera sent a JPEG with no DHT segment
before its first SOS, the capture writer inserts the standard tables of ITU-T T.81 Annex K.3 as one
DHT segment immediately before the first SOS, and stores those bytes. It changes no other byte
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 3).
The order of the four tables in that segment is the choice of the writer
([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 6).

**SFF-735** (writer) A writer stores each frame in the orientation of the sensor. It does not
rotate the pixels. It writes no rotation element (for example `Projection` or `ProjectionPoseRoll`)
and no EXIF orientation tag ([ADR-DE9S](decisions/entries/DE9S-rotation-in-the-video-csv-header.md)).

**SFF-736** (writer) The TimestampScale is 1,000,000 (1 ms). The container timestamp of the
frame at position k is ⌊(2 × k × `den` × 1000 + `num`) / (2 × `num`)⌋ ms, where `num/den` is the
nominal rate (k / nominal rate, rounded half up). The track `DefaultDuration` is
⌊10^9 × `den` / `num`⌋ ns: the nominal frame period in nanoseconds, rounded down, as the pinned
FFmpeg writes it ([ADR-94YQ](decisions/entries/94YQ-golden-g1-review-decisions.md) item 2). For
30000/1001, it is 33,366,666. A writer MUST NOT store measured times in the container. A
writer refuses a nominal rate above 1000 frames per second.

**SFF-737** (writer) A writer stores no timing data, no overlay and no burned-in text in a
frame, for example in an APPn segment of the JPEG. A take folder holds no overlay file
([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md)).

**SFF-738** (reader) A reader MUST NOT require a JFIF or APP0 segment, a DHT segment or a
fixed marker order in a JPEG. It MUST accept bytes after the entropy-coded data. A frame is the bytes
of its block payload. A reader ignores an EXIF orientation tag.

**SFF-739** (reader) A reader finds a block payload by parsing the block header: the track
number as an EBML variable-size integer, then 2 bytes of timestamp, then 1 byte of flags. It MUST NOT
assume a fixed header length.

**SFF-740** (reader) An unfinished camera file can have no Cues and elements of unknown size. A
reader of an unfinished camera file finds its frames from the byte positions of its CSV rows, or by a
walk of the elements from the start of the Segment data. The j-th row with byte fields
(`byte_offset` and `byte_size`) belongs to the j-th complete block of the camera file, in file
order. When each row has byte fields, row k belongs to block k. A `missing` row with empty byte
fields has no block (SFF-754). It is usable when it is complete and its CRC is correct
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 2).
A frame is usable when its row is usable (SFF-746) and, for a row with byte fields, its block is
complete. A reader uses no row after the first row with byte fields whose block is not complete,
and no block after the last usable row (the mapping by the rows with byte fields and the first row
whose block is not complete, [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 1; [ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)). `rows` of the
reader result still counts each usable row, also a row after the last complete block (SFF-746,
SFF-885). The multi-camera frames use only the usable frames (SFF-754)
([ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 2).

## 7. CSV timing sidecars: common rules

Each media file has one timing sidecar, a CSV file with the same name stem and the suffix `.csv`
([ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md)). A timing sidecar
has, in this order: header lines, one column line, data rows, and footer lines.

```
# skellyspecs=video_timing
# format_version=2.0
# format_prerelease=1
# writer=skellycam 2.0.0
# take_uuid=6f1c2c1e1d7e4c479a3e2f2b3c4d5e6f
...
frame,source_frame_number,arrival_ns,sample_ns,flags,byte_offset,byte_size,crc32
0,1000,1203311,1180002,0,4127,61234,5b1e0c2a
...
# fit_segment pos_first=0 pos_last=18341 t0_ns=1190001 period_ps=33366700000
# end rows=18342 gaps=2 filled=0 missing=0 encode_skips=0
```

**SFF-741** (writer) A timing sidecar is a text file (SFF-700). Fields are separated by
`,`. A field holds no `,`, no quote, no space and no line end. No field is quoted.

**SFF-742** (writer) A header line has the form `# <key>=<value>`, with one key on each line.
A key holds only `a`–`z`, `0`–`9` and `_`. A value holds no line end. The first header line is
`# skellyspecs=video_timing` or `# skellyspecs=audio_timing`. The header holds each key that
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
counts of section 8 or 10 ([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-746** (reader) A reader reads a timing sidecar strictly. It uses a data row only when
the row ends with LF, has the right number of fields and its CRC is correct. A last line with no LF is
torn: it ends the read, and its bytes count in `torn_bytes`. A complete row with a wrong CRC makes the
file `damaged` (reason `crc_mismatch`), and the read stops at that row. A reader reads no data row
after the first footer line. A complete footer line counts in no member of the reader result. A
torn footer line counts in `torn_bytes`
([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 28b).

**SFF-747** (reader) A timing sidecar whose last line is not an `# end` line is unfinished, also
when it has fit lines and a `# repair` line (SFF-795). A reader uses its complete rows. It does not
use its fit lines: a reader uses the fit lines only of a finished or repaired sidecar
([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 28c).

**SFF-748** (reader) A reader refuses a timing sidecar (state `invalid`) whose header lacks a
key that its kind requires (reason `missing_metadata`), or has a value in a wrong form (reason
`bad_metadata`). The range of `group_position` (0 to `group_size` − 1 in the header table of
section 8) is not a form check: a reader reads a sidecar with a `group_position` at or above
`group_size` normally, and the count of SFF-869 reports the extra file (`extra_files`)
([ADR-QDF0](decisions/entries/QDF0-label-form-and-group-position-range.md)).

## 8. Video timing sidecar

The header of a video timing sidecar holds these keys, in this order:

| Key | Value |
|---|---|
| `skellyspecs` | `video_timing` |
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
| `arrival_ns` | The arrival time (relative), or empty in a `missing` row (SFF-756) |
| `sample_ns` | The sample time (relative), or empty |
| `flags` | The flags of the frame (SFF-756) |
| `byte_offset` | The offset of the JPEG payload of the block of the row (the frame or the placeholder) from the start of the camera file, or empty in a `missing` row with no block (SFF-754) |
| `byte_size` | The number of bytes of the JPEG payload of the block of the row, or empty in a `missing` row with no block |
| `crc32` | The row CRC (SFF-744) |

The footer of a finished file has zero or more `# fit` and `# fit_segment` lines (section 11), then
`# end rows=<R> gaps=<G> filled=<F> missing=<M> encode_skips=<E>`
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) items 1 and 2).

The sidecar has no legacy column, for example `recording_frame_number` or
`timestamp.from_recording_start.sec` ([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md)
item 5).

**SFF-749** (writer) The take keys (`take_uuid` to `audio_count`) have the same values in each
timing sidecar of a take.

**SFF-750** (writer, reader) In `nominal_rate`, `num` and `den` are integers from 1 to 2^20. A
reader refuses another value (reason `bad_rate`).

**SFF-751** (writer, reader) `display_rotation` is the clockwise rotation in degrees that a reader
applies to the stored frame to show it upright. A reader refuses another value (reason
`bad_rotation`).

**SFF-752** (writer) `camera_key` is the first 8 bytes of the SHA-256 of the identity string of the
camera, as 16 lowercase hexadecimal characters. The hash input is the UTF-8 bytes of the identity
string. The identity string is the first of these forms that applies
([ADR-70VP](decisions/entries/70VP-camera-identity-forms-and-remembered-keys.md), which changes
[ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md) item 16a):

1. `<vendor_id>:<product_id>:serial:<serial>`, when the USB serial number is usable. A serial is
   usable when it is not empty, it is not a known placeholder (for example `0001`), and no other
   connected camera with the same vendor ID and product ID has the same serial.
2. `<vendor_id>:<product_id>:port:<port_path>`, when the camera has a port path. The capture writer
   reads the port path from the operating system, never from the capture library.
3. `<vendor_id>:<product_id>:device:<os_device_id>`, for a camera that is not a USB device and has
   a persistent identifier of the operating system (for example a built-in laptop camera).
4. `<vendor_id>:<product_id>:assigned:<uuid>`. `<uuid>` is 32 lowercase hexadecimal characters of a
   random UUID. The capture program makes it one time for the camera and remembers it. The user
   attaches it to the camera again in a later session.

`<vendor_id>`, `<product_id>`, `<serial>`, `<port_path>` and `<os_device_id>` are the texts of
`device` in the capture info JSON (section 13), with `0000` for a vendor ID or a product ID that is
null. No file holds `<uuid>`.

A capture writer MUST write a `camera_key` that is not 0. It MUST NOT refuse a camera because of
its identity. A conversion writer MAY write `0`.

A capture writer MAY write the remembered `camera_key` of a camera in place of the computed one,
when the user confirmed that the device is that camera. `key_origin` of the camera config
(section 13) tells which key the file holds.

A capture writer that cannot read the values of the identity string MAY write a provisional key, with
`key_origin` `provisional`: 16 lowercase hexadecimal characters, not 0, that the writer made from its
own camera identifier. The key is not stable across computers or sessions. A program does not
remember it
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 6). A writer that writes a provisional key for a camera does not make an assigned key
(form 4) for that camera (the words "cannot read the values" and "not 0", and this sentence,
[ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 5).

A capture writer MUST NOT give two different cameras the same `camera_key`. The capture program
finds a remembered camera by its remembered location (the serial, the port path or the OS device
identifier), not by a new computation of the hash. When the computed key of a camera is equal to
the key of a remembered camera that has another location, the capture program MUST NOT use that key
before it asks the user. When the user says that the camera is not that remembered camera, the
capture program gives the camera an assigned key (form 4), with `key_origin` `assigned`
([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 10).

The capture program asks the user in this case: a connected camera matches no remembered camera,
and a remembered camera that is not connected is a candidate. A remembered camera is a candidate
when its `vendor_id` and its `product_id` are equal to those of the connected camera and are not
null. When one of these values is null, in either camera, a remembered camera is a candidate when
its `model` is equal to that of the connected camera. The capture program never compares `os_name`
([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 1,
[ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 1). It
asks if the device is that camera. The prompt shows the live preview of the connected camera, and
`user_name`, `camera_label` and `model` of each candidate
([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 2). When the user agrees, the camera keeps
the remembered `camera_key`. When two or more candidates fit, the user selects one of them, or says
that it is a new camera.
When freemocap runs and a calibration applies, freemocap first checks from the calibration where
the cameras are. Then it asks, with the most likely cameras first. skellycam alone does not make
this check: it asks with no suggestion
([ADR-94YQ](decisions/entries/94YQ-golden-g1-review-decisions.md) item 6).

The list of remembered cameras is local state of the capture program. It is not in the take folder,
and this spec defines no file for it. A capture program can make it from the capture info JSON of
any take.

A serial is also not usable when
it has a character outside 0x21 to 0x7F, when it has a `,`, or when it is one repeated character.
The known placeholders, compared in lower case, are `0`, `00`, `000`, `0000`, `00000000`,
`000000000000`, `0000000000000000`, `1`, `01`, `0001`, `0123456789`, `123456789`, `1234567890`,
`12345678`, `123456`, `0123456789abcdef`, `sn0001`, `sn12345678`, `none`, `null`, `default`,
`serial`, `unknown`, `n/a`, `na`, `123` and `200901010001`. This list does not change in major
version 2 ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 9).
When `device.serial` is not null and the writer does not use it for the key, the file records no
reason ([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 4).

(provisional: the identifier tests on Windows, Linux and macOS) The source of `port_path` is:
on Windows, `DEVPKEY_Device_LocationPaths[0]`; on Linux, the PCI address of the controller, the USB
revision and the port chain, from sysfs; on macOS, the `locationID`. The source of `os_device_id`
is the `AVCaptureDevice.uniqueID` on macOS, or the device instance ID on Windows. The exact text
form of the two values is not decided.

**SFF-753** (reader) A reader refuses a sidecar whose `camera_label` does not have the form
of SFF-720 (reason `bad_label`). The form is the pattern only, 6 to 8 lowercase hexadecimal
characters or `cam<N>`, so a reader does not refuse a label that is not the start of the
`camera_key` of its own camera ([ADR-QDF0](decisions/entries/QDF0-label-form-and-group-position-range.md)).

**SFF-754** (writer) There is one row for each position, in position order.
`frame` is 0 in the first row and increases by 1 in each row. Row k of each video sidecar of a take
is multi-camera frame k. The finished camera files of one take have the same number of rows
([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md)). A camera file has at most 2^31
frames. A camera file has one block for each row, with two exceptions: when the process that writes
the camera file is killed or hangs, and when a write to the camera file fails, the file ends early.
Each row after its last block has the flag `missing` and empty `byte_offset` and `byte_size`. Such a
row has no block. A camera file can hold no block: it then holds no Cluster, only the elements before
the first Cluster ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 9)
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 2).
When the camera files that a reader reads have different numbers of usable frames
(SFF-740), the multi-camera frames are the frames from 0 to the smallest number of usable frames
minus 1. For a finished or a repaired camera file, the number of usable frames is `rows` (SFF-885):
each row of a repaired camera file is a usable frame
([ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 3).
For an unfinished camera file, it counts only the usable frames of SFF-740: the usable rows that have
a complete block, and the usable `missing` rows with no block ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 3)
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 32,
[ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 2).

**SFF-755** (writer) `arrival_ns` is the host-clock time at which the writer received the frame,
minus the take start. `sample_ns` is the time that the capture driver gives for the frame, on the host
clock, minus the take start. It is empty when the driver gives none. A conversion writer writes an old
per-frame time as `arrival_ns`. In a `missing` row, `arrival_ns` and `sample_ns` follow SFF-756.

**SFF-756** (writer) `flags` is a decimal integer of bits. Bit 0 (1): `gap`, the source frame
number is not the source frame number of the row before plus 1, and it is not equal to the source
frame number of the row before. `gap` is 0 in the first row, and when the row or the row before has
an empty `source_frame_number`. Bit 1 (2): `filled` (provisional: the slot assembly of the skellycam
plan, row 2.2, and desk tests DT4 and DT7), the writer copied the JPEG of the row before, because
the camera gave no new frame for this multi-camera frame
([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md)). A writer of version 2.0 writes 0
to bit 1, because it copies no frame. Bit 2 (4): `encode_skip`, the writer did not store one or more
frames before this frame because the JPEG encoder failed. Bit 3 (8): `repeat`, the source frame
number is equal to the source frame number of the row before. Bit 4 (16): `missing`, the camera gave
no usable frame for this row. A writer writes 0 to the other bits
([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md),
[ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

A capture writer writes `missing` for a frame with a capture error, and for each multi-camera frame
after the last frame of a camera that stopped during the take. The block of a `missing` row is a
placeholder: a baseline JPEG of one colour, black, with the width, the height, the number of
components and the H/V sampling factors of each component of the camera's frames. When the writer
knows no frame of the camera, it uses the mode size (the width and the height of the capture mode
that the writer opened; [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 10) and the factors 2x1, 1x1, 1x1. Its Huffman and
quantisation tables are the writer's choice. The writer compares layouts by the size, the number of
components and the H/V factors only. In a `missing` row, `source_frame_number`, `arrival_ns` and
`sample_ns` hold the values of the frame that had the error, or are empty when the camera gave no
frame. The `missing` rows after the last block of a short file have no block (SFF-754)
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).

Guidance for programs: in skellycam, the flag `encode_skip` replaces the log message of an encoder
skip ([ADR-Z641](decisions/entries/Z641-program-guidance-gate-2-scope-and-no-push.md) item 1).

**SFF-757** (writer) (provisional: live byte offsets, desk test DT5) `byte_offset` and
`byte_size` give the JPEG payload of the block of the row (the frame or the placeholder) in the
camera file. They are correct while the file is live, and they do not change when the file is
closed. A row with no block has both fields empty (SFF-754; [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 4).

**SFF-758** (writer) In the `# end` line, `rows` is the number of data rows, `gaps` the number of
rows with the `gap` flag, `filled` the number with the `filled` flag, `missing` the number with the
`missing` flag, and `encode_skips` the number of rows with the `encode_skip` flag. A repair computes
each count from the rows
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md), `missing`:
[ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).

**SFF-759** (reader) The number of rows with byte fields (SFF-740) of a finished or a repaired
video sidecar is the number of blocks of its camera file
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 2).
On a mismatch, a reader refuses the pair (state `invalid`, reason
`bad_metadata`). A repair makes the two numbers equal (SFF-795,
[ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 1,
[ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 10).
A player MAY show the frames of a finished or repaired camera file before it has counted its
blocks. It then checks, for each frame that it reads, that the block of the frame is the next block
after the block of the previous row with byte fields (SFF-739), and, at the open, that no block
follows the last block that a row points at. When a check fails, the player stops showing images of
that camera file and reports the file as `invalid` with `bad_metadata`. The reader result of SFF-885
does not use this order
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 9).
A reader also refuses the pair (state `invalid`, reason `bad_metadata`) when a row has one empty
byte field and one that is not empty, when a row has empty byte fields and no flag `missing`, or when
a row with byte fields follows a row with empty byte fields ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 10).

## 9. Audio file

The audio file is Opus ([RFC 6716](https://www.rfc-editor.org/rfc/rfc6716)) in a fragmented ISO BMFF
file (ISO/IEC 14496-12), with the Opus mapping of the "Encapsulation of Opus in ISO Base Media File
Format" specification ([ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md)). It
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

**SFF-766** (reader) Sample 0 of the audio is the first decoded sample after the pre-skip samples of
`dOps`. A program that decodes the audio drops the pre-skip samples and applies no output gain. Through
its test adapter, a reader does not decode: the detail function `audio_details` gives the pre-skip
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 36, [ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).

## 10. Audio timing sidecar

The header of the audio timing sidecar holds, in this order: `skellyspecs` (`audio_timing`),
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
does not mix the two in one file. A row with no `arrival_ns` has no player time, also when the file
has a fit ("also when the file has a fit", [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 11). In the strict
player time of SFF-782, the reader skips it
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).

**SFF-782** (writer, reader) The player time never decreases from one position to the next in one
file. A position with no player time (SFF-781) is not in this rule. The times that a reader gives to
freemocap for a camera strictly increase. With the player times p, in position order and with only
the positions that have a player time, the strict player time is s(0) = p(0), and s(k) is the
larger of p(k) and s(k − 1) + 1 ns (only the positions with a player time,
[ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 2).
A reader gives s to freemocap, and SFF-828 uses s. The `records` of the reader result hold p
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-783** (reader) A player shows, at take time t, the last frame of each camera whose player
time is at or before t. When two or more positions have the same player time, the player shows the
highest of them at that time
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 8). It MUST NOT compute a frame from its index and the frame rate. A player shows
no frame of a camera before its first player time ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 11).

At a take time in a `missing` row, a player shows the last frame before it that is not `missing`,
with a mark "no frame". It never shows the placeholder as a picture. A program that ignores the flag
shows the placeholder (black)
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 10).
A take time t is in a `missing` row when that row is the last row whose player time is at or before
t. It is also in a `missing` row with no player time when the player shows the multi-camera frame of
that row at t. How a player selects that multi-camera frame is its choice. When no frame before the
`missing` row is not `missing`, the player shows no frame of the camera, with the mark "no frame"
([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) items 1 and
2).

**SFF-784** (reader) A reader maps an audio sample to take time only with the fit of the audio
sidecar (SFF-779). It MUST NOT use the take start and the nominal sample rate. It adds
`file_sample_offset` to a decoded sample index before it uses the fit. When the sidecar has no fit
that the reader uses (SFF-747), for example after a crash, the reader gives the warning
`missing_fit` and computes one fit segment
from the rows that it uses (SFF-746), with this method ([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).
For an unfinished audio file, the fit uses each row that SFF-746 lets the reader use. It also uses a
row whose block is not in `records` (SFF-792,
[ADR-64ER](decisions/entries/64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) item 2).

- The time of a row is its `adc_ns` when that field is not empty, else its `host_ns`.
- A row with the flag `silence` is a usable row for the fit
  ([ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)).
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

The rules of [ADR-G1YG](decisions/entries/G1YG-writing-crash-reading-and-repair.md) apply.

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
files. skellycam holds the lock for each whole-file write that it makes: the manifest and the
capture info JSON (SFF-801)
([ADR-JB3A](decisions/entries/JB3A-repair-state-question-and-skellycam-lock.md)). A writer does
not write one of these files when another program holds the lock. An append to
the journal needs no lock: the journal is a live append-only file (SFF-787), like a camera file. A
reader ignores the lock file
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).
On Windows, the lock is an exclusive lock of byte 0 for 1 byte (`LockFileEx` with
`LOCKFILE_EXCLUSIVE_LOCK`, or `LockFile`, which takes the same lock; Python `msvcrt.locking` calls
`LockFile`). On Linux and macOS, it is `flock` with `LOCK_EX` on the whole file. Each program uses
this form, because a `flock` lock and an `fcntl` record lock do not see each other on Linux
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 7).

**SFF-790** (reader) A reader ignores a file whose name ends in `.tmp`. It gives the folder warning
`stray_tmp` when it finds one or more
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-791** (reader) A reader reads an unfinished file in place. It reads each complete record
in file order and reports the file as `unfinished`. A record that is not complete ends the read, and
its bytes count in `torn_bytes`. `torn_bytes` of a device pair is the sum of two numbers. The first
is the number of bytes of the last line of the sidecar when that line has no LF, else 0. The second
is the number of bytes of the media file after its last complete block or fragment when the last
line of the sidecar is not an `# end` line, else 0. So `torn_bytes` is 0 for a finished and for a
repaired pair. For a `damaged` sidecar, it does not count the row with the wrong CRC or the rows
after it: they are complete lines
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md),
[ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 28a). A reader checks that the read
reached the end of the file or a torn record, because a streaming reader can stop at a torn tail
with no error.

**SFF-792** (reader) In an unfinished audio file, a reader ignores a fragment whose `moof` or
`mdat` goes past the end of the file, and a `trun` entry whose bytes go past the end of the file.
`rows` of the reader result counts each row that SFF-746 lets the reader use. `records` holds only
the blocks whose every sample, from `first_sample` to `first_sample` + `n_samples` − 1, is in a
complete fragment. A block can be in two fragments. This is the rule of an unfinished camera file
(SFF-740). A block that is only partly in the complete fragments is
not usable. Sample n of the sidecar is decoded sample n − `file_sample_offset`, and decoded sample
0 is the first sample after the pre-skip (SFF-766). So each sample of a block is in a complete
fragment when
`first_sample` + `n_samples` − `file_sample_offset` is not more than the samples that the file holds
(SFF-785)
([ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 4,
[ADR-783H](decisions/entries/783H-text-corrections-of-the-second-golden-review.md) item 9).

**SFF-793** (writer) When a program (skellycam or freemocap) finds an unfinished file of a take,
or a manifest of a take whose `state` is `recording`, it asks the user: "An
incomplete recording was found. Would you like to repair it?" skellycam asks about a take that it
recorded on its own. When freemocap runs, freemocap asks one time for the whole take: for the media
files and the journal together. So the user gets one question for one take. This rule also applies
at start-up. No
program repairs a file, folds a journal or changes a file of the take before the user agrees. The
only exception is the completion of SFF-894 by the program that records the take
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 4). When
the user agrees, the program repairs the files, and freemocap folds a left-over journal as part of
that repair (SFF-845). The repair sets `state` of the manifest to `finished`. The manifest `state`
has no third value: each repaired file still reports the state `repaired`, from its `# repair` line
(SFF-795). When the user does not agree, the program changes nothing, and a reader still
reads the files in place (SFF-791). freemocap also asks this question before it folds a journal that
is left over in a take whose manifest already has `state` `finished`. It folds that journal only
when the user agrees
([ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md),
[ADR-JB3A](decisions/entries/JB3A-repair-state-question-and-skellycam-lock.md)).
A repair does each step for the whole take before the next step: (1) it cuts each media file;
(2) it cuts each sidecar; (3) it appends the footer lines of SFF-795: first the fit lines to each
sidecar, then the `# repair` line to each sidecar, then the `# end` line to each sidecar; (4) it
writes the manifest. In the tail repair of SFF-795, step 1 appends the placeholder blocks and step
2 appends the cut rows again ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 6)
([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 3,
[ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 3). An
interrupted repair leaves the manifest in the state `recording`. A repair that stops in step 3 can
leave some sidecars `repaired` and the others `unfinished`. The program asks the question again,
and a new repair finishes the rest (SFF-798,
[ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 12). The case
`interrupted_repair` of G6 stopped in the `# repair` pass of step 3: each of its sidecars is
`unfinished`. After
the manifest, freemocap folds a left-over journal (SFF-844). So the fold uses the fit of the
repaired sidecars. In step 4, the program that did the repair writes the manifest while it
holds `.processing.lock` (SFF-789). It sets `state` to `finished` and `writer` to its writer
string. It computes the summary again (SFF-728). It adds the warning `camera_gap` for a repaired
video sidecar with `gaps` more than 0. The `source` of that warning is the program that did the
repair: `skellycam` or `freemocap` ([ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 5). It changes no other member. When the take has no manifest that a reader uses (SFF-867), the
repair writes no manifest
([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 26a).

**SFF-794** (writer, reader) A repair never changes a byte before its cut. It cuts each file of a
device pair after the last record that it keeps (SFF-795 to SFF-797). Then it appends the footer
lines of SFF-795 to the sidecar, and, in the tail repair of SFF-795, the cut rows again before
them. It appends nothing to the media file, except the placeholder blocks of the tail repair
([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 4; the appended rows, [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 6). A repaired camera file has no
normal end: the repair writes no Cues and does not write the SeekHead again. A repaired audio file
has no `mfra` box. These writes would change bytes before the cut. A reader accepts a repaired
camera file with no normal end, and reads it as SFF-740 gives for an unfinished camera file: with no index and no normal end
([ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 1). A
reader accepts a repaired audio file with no `mfra` box ([ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 3).

**SFF-795** (writer) The repair of a timing sidecar cuts the sidecar at its first bad row: a row
that is not complete or that has a wrong CRC. It keeps no row after a bad row. The repair makes a
camera pair equal: it keeps only the frames that have a kept row and a complete block (SFF-740). So
it keeps the first n rows with byte fields of a video sidecar and the first n blocks of its camera
file (SFF-797). n is the smaller of two numbers: the number of rows with byte fields before the
first bad row (each row with byte fields, when no row is bad), and the number of complete blocks. When n is the
number of rows with byte fields before the first bad row, the repair also keeps the `missing` rows
with empty byte fields that follow them, up to the first bad row. These rows do not count as blocks
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 2; the wording, [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 7). A later repair MAY replace the tail of a
short file with placeholders (SFF-756) ([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 2).
Such a repair cuts the sidecar before its first row with empty byte fields. It appends a placeholder
block to the camera file for each cut row, and it appends each cut row again with the byte fields
of its placeholder ([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 4). A program runs it only after the question of SFF-793 and the
agreement of the user. Its `# repair` line has the bytes that it cut from the sidecar in
`cut_bytes`, and `media_cut_bytes` 0 ([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 6).
A repaired video sidecar has as many rows with byte fields as its camera file has blocks (SFF-759)
([ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) items 1 and 4,
[ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 2). The repair
of an audio pair keeps the first n rows of the audio sidecar. n is the smaller of two numbers: the
number of rows before the first bad row, and the number of first rows whose block has each sample in
a complete fragment (SFF-792) of the audio file that the repair keeps (SFF-796). So the `# end` line
and the manifest `duration_s` of the audio count only the samples of the kept rows (SFF-728,
SFF-769)
([ADR-7JJJ](decisions/entries/7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md)
item 2). The repair computes the fit from the kept rows and appends the fit lines, the line
`# repair cut_bytes=<n> media_cut_bytes=<m> repair_writer=<writer string>`, and the `# end` line.
`cut_bytes` is for the sidecar, and `media_cut_bytes` is for the media file. `repair_writer` is the
last key of the line (SFF-745). A reader reports a sidecar as `repaired` only when it has a
`# repair` line and its last line is an `# end` line. With another last line, the sidecar is
`unfinished` (SFF-747)
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md),
[ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 28c).

**SFF-796** (writer) The repair of an audio file cuts the file after the last fragment whose
`moof` and `mdat` are complete. It removes a zero-filled tail only when the box walk finds an
incomplete box. It does not remux the file, and it appends no `mfra` box (SFF-794). This is step 1
of SFF-793. In step 2, the repair cuts the audio sidecar to its first n rows. n is the smaller of
two numbers: the number of rows before the first bad row, and the number of first rows whose block
has each sample in a complete fragment of the cut file. In step 3, it appends the fit lines, the
repair line and the `# end` line to the audio sidecar (SFF-795).

**SFF-797** (writer) (provisional: the repair of a camera file, desk test DT-R1) The repair of a
camera file keeps its first n blocks (SFF-795). Each of them is a complete block. It cuts the file
after block n − 1, changes no byte before its cut and appends nothing, except the placeholders of
the tail repair of SFF-795 (the exception, [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 6; SFF-794,
[ADR-B6WH](decisions/entries/B6WH-repair-equal-pair-cut-and-no-normal-end.md) item 1).

**SFF-798** (writer) A repair that stops before its end leaves the manifest in the state
`recording`, and it can leave unfinished files. When it stops in step 3 of SFF-793, some sidecars can be
`repaired` and the others `unfinished`
([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 12). A new
repair starts again from the same cut, finishes the rest and gives the same result, except for
`cut_bytes` and `media_cut_bytes`. A reader reports a sidecar of an interrupted repair as `unfinished`, with `fit`
false and the warning `missing_fit`, also when the sidecar has fit lines (SFF-747).

**SFF-799** (reader) A reader never creates, moves, renames or changes a file of the take
folder.

## 13. Capture info JSON

skellycam writes `<rec>_info.json` with the capture facts of the take, and no other facts
([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md)). It is a JSON file
(SFF-702) with these members, in this order:

| Member | Value |
|---|---|
| `skellyspecs` | `"capture_info"` |
| `format_version`, `format_prerelease` | Section 3 |
| `writer` | The writer string |
| `take_uuid` | The ID of the take |
| `camera_configs` | An object. Each key is a `camera_key` (16 hexadecimal characters, or `0` with the label after it, as `0:<camera_label>`). Each value is a camera config (below). A writer MUST write the keys in order of `group_position` ([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 4). |
| `audio` | null, or an object with `device_name`, `host_api` and `device_channels` |

A camera config has these members:

| Member | Value |
|---|---|
| `camera_label` | The label (a link for people; `camera_key` is the link key) |
| `user_name` | The name that the user gave the camera: null, or a text of 1 to 128 bytes of UTF-8 with no control character |
| `key_origin` | The origin of `camera_key` (SFF-752): `"computed"` (the key is the hash of form 1, 2 or 3, built from the `device` values of this file), `"confirmed_by_user"` (a remembered key that the camera has because the user confirmed the camera, in this session or an earlier one), `"assigned"` (form 4, made in this session, confirmed by nobody) or `"provisional"` (a capture writer that cannot read the identity of SFF-752 made the key from its own camera identifier; the key is not stable across computers or sessions, and a program does not remember it, [ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 6). null when `camera_key` is 0. |
| `device` | `model` (the product text that the camera reports about itself: the USB product string), `os_name` (the name that the capture API lists for the camera) ([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 2), `vendor_id` and `product_id` (4 lowercase hexadecimal characters, or null), `serial` (or null), `port_path` (or null), `os_device_id` (a text, or null: the persistent identifier of the OS, SFF-752), `backend` (for example `media_foundation`, `v4l2`, `avfoundation`) and `os_index` (the OS index at capture, or null) |
| `requested` | `width`, `height` and `framerate` (a number, or `"camera_default"`), `capture_format` (`MJPG` or `YUYV`) and `exposure_mode` (`auto`, `manual` or `recommend`) |
| `controls` | An object of the control values that the writer read back at the take start. Each key is a control name with its unit (SFF-802). Each value is `{"value": <number or null>, "auto": <true, false or null>}`. A writer MUST write the keys in the order of the list of SFF-802 ([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 4). |
| `exposure_step` | The result of the exposure step, or null: `selected_exposure_us`, `method` and `samples` (an array of `{exposure_us, mean_luma}`) |

**SFF-800** (writer) The capture info JSON has each member of the tables, in their order. It
has no other member. In particular, it has no `videos`, `camera_timing` or `multiframe_timing` map,
no `recording_name`, `recording_directory`, `recording_uuid`, `mic_device_index` or full timestamp
object, and, in a camera config, no `rotation`, `camera_index`, `use_this_camera`, `resolution`,
`color_channels`, `pixel_format` or `writer_fourcc`. A reader reports a `rotation` member with the
link check `rotation` (SFF-872). `user_name` is metadata only: no writer puts
it in a file name, in `camera_label` or in the identity string (SFF-752). A writer SHOULD NOT give
two cameras of one take the same `user_name` that is not null. A reader has no rule for `user_name`
([ADR-70VP](decisions/entries/70VP-camera-identity-forms-and-remembered-keys.md)).

**SFF-801** (writer) skellycam writes the capture info JSON when the take starts and again when
it ends, each time whole (SFF-786), while it holds `.processing.lock` (SFF-789,
[ADR-JB3A](decisions/entries/JB3A-repair-state-question-and-skellycam-lock.md)). It is the only
writer of this file.

**SFF-802** (writer) The control names are `exposure_us`, `gain`, `white_balance_k`, `focus`,
`zoom`, `pan_deg`, `tilt_deg`, `power_line_hz`, `auto_exposure_priority`, `brightness`, `contrast`,
`saturation`, `sharpness`, `gamma` and `backlight_compensation`. A writer writes each control that the
device has. It writes null for a value that it could not read.

**SFF-803** (reader) A reader links a camera config to its camera only by its key (`camera_key`).
A reader checks only that `key_origin` is one of its four values, or null when `camera_key` is 0.
Another value makes the capture info JSON `invalid`, with the reason `bad_schema`
([ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 7; the fourth
value: [ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 6). A reader never
computes a key again from the `device` values ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 9).

## 14. Processing info JSON

freemocap writes `<rec>_recording_info.json` with the summary of its processing, and no capture facts
([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md)). It is a JSON file (SFF-702)
with these members, in this order:

| Member | Value |
|---|---|
| `skellyspecs` | `"processing_info"` |
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
  ([ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)).
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
([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md)). The camera model is the
OpenCV pinhole model, P = K [R | t], where R and t map the world to the camera. The distortion model is
Brown–Conrady with k1, k2, p1 and p2.

One calibration serves each take of one camera setup. A user makes a new calibration when the setup
changes: a camera moved, or a lens or the focus changed. A change of the geometry also gives a new
`calibration_uuid` (SFF-810, [ADR-3D33](decisions/entries/3D33-spec-draft-v2-details-folder-files.md)
item 4). A calibration always comes from a take. The user can delete that take,
but it is strongly advised to keep it
([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md) item 3).

The file has one table `[metadata]` and one table for each camera:

```toml
[metadata]
format_version = "2.0"
format_prerelease = 1
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
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-810** (writer) A new calibration gets a new `calibration_uuid`. A writer that changes the
geometry of a calibration (an alignment or a transform) writes a new `calibration_uuid` and adds the
change to `transformation_history` ([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md),
[ADR-3D33](decisions/entries/3D33-spec-draft-v2-details-folder-files.md) item 4).
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
`<rec>_camera_calibration.toml` ([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)
item 6b).

**SFF-815** (reader) A reader links a camera table to its camera by `camera_key`. It reads the
camera tables in the order of `index`, not of their keys.

## 16. Tracking Parquet

`<rec>_data.parquet` holds the 2D and 3D tracking data of the take, the ChArUco observations and the
diagnostics ([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md)). It is an Apache Parquet file
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
such a file (reason `bad_schema`). Note: fastparquet 2026.9.0 cannot read these files
([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md) item 7).

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
([ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-825** (writer) The descriptor holds `take_uuid`, `format_version`, `format_prerelease` and
`writer`.

**SFF-826** (writer) Each camera source is `camera:<camera_label>`, with the definition of
parts/parquet-descriptor.md: `camera_key`, `camera_label`, `video_filename`, `timing_filename`,
`timing_method` and `inferred_offset_s`. The definition holds no nominal frame rate: the timing sidecar is its home.
`video_filename` and `timing_filename` are file names with no folder. The files are in the media
folder ([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 38g).

**SFF-827** (writer) `frame_number` of a camera row is the position of the frame in its camera
file. All cameras of a sensor group use the same `frame_number` for one multi-camera frame
(SFF-754).

**SFF-828** (writer) `timestamp_s` of a capture `TIMESTAMPS` row, and of the `OVERLAY_2D` and
`BOXES_2D` rows of a camera, is the strict player time of the frame (SFF-782) divided by 10^9. The
camera's `timing_method` is `recorded`. The group `TIMESTAMPS` (`synchronized`) of frame f is the mean
of the strict player times of the cameras at frame f, divided by 10^9, with the method
`mean_camera_times`. The 3D, reconstruction and diagnostic rows use the group times. The exact
values are these. s is the strict player time of a frame, in nanoseconds. A camera `timestamp_s` is
the float64 nearest to s / 10^9. S is the sum of s over the n cameras of the sensor group at one
frame. The group time is m = ⌊(2 × S + n) / (2 × n)⌋ ns: the mean, rounded half up. Here, ⌊⌋
rounds down also for a negative value. The group `timestamp_s` is the float64 nearest to m / 10^9
([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 38b). (provisional: rows with
no player time, [open-work.md](decisions/open-work.md)) A frame with no strict player time
(SFF-781) has no camera `timestamp_s`, and S and n count only the cameras that have one
([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 8).

**SFF-829** (writer) 2D values are pixels of the stored JPEG, in sensor orientation, before
`display_rotation`. The `width` and `height` of each camera image reference are the width and height
of the stored JPEG frames. freemocap rotates the 2D values by `display_rotation` (SFF-751) to show
them ([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md) item 4).

**SFF-830** (writer) 3D points of a take with two or more cameras are in millimetres in the
reference frame `calibrated_world`, with the basis `blender_x_right_y_forward_z_up` (+X right, +Y
forward, +Z up, right-handed). A take with one camera uses `camera_plane`, in pixels.

**SFF-831** (writer) The confidence of a 2D point is the component `visibility` of `OVERLAY_2D`,
from 0 to 1. A point that the tracker did not detect on a frame has `x` and `y` null and
`visibility` 0.

**SFF-832** (writer) Each recorded model of the descriptor has `tracker_keypoint_names`,
`tracker_connections` (pairs of tracker keypoint names, to draw the skeleton) and
`segment_topology`: an array of segments, each with `name`, `parent` (a segment name or null),
`proximal` and `distal` (landmark names). `segment_topology` has one item for each item of
`skeleton.segments` of the model, in that order. `name` is the segment name. `parent` is
`rest_pose.parents[name]`. `proximal` is `frame.origin` of the segment, and `distal` is
`frame.primary_point`. So the two are landmark names, as in `LANDMARKS_3D`
([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 38a). Each name of
`tracker_connections` is in
`tracker_keypoint_names`. A writer omits `tracker_connections` when it has no pair
([ADR-W5JC](decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md)). A take folder
has no `tracker_schema.json`.

**SFF-833** (writer) The file holds each retained run. `selected_run_id` of the processing info
JSON (section 14) names the run to show. The descriptor does not hold it, so a change of the selected
run does not rewrite the Parquet. A new posthoc run gets a new `run_id`. A writer never replaces or
changes a run whose `origin` is `realtime`, with one exception. After a repair, freemocap rewrites
the times of a realtime run: `timestamp_s` of its rows and the values of its `TIMESTAMPS` rows. It
does this when it next opens the take and finds that a timing sidecar has a `# repair` line and a
fit that the run did not use. It changes nothing else of a realtime run
([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md),
[ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)). So `latency_ms` of each
`coverage` keeps the value of the fold (SFF-834)
([ADR-1P4N](decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)
item 7). Within these rules, what posthoc processing does with a realtime run is the choice of
freemocap ([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md) item 8).

**SFF-834** (writer) A run from the realtime journal (section 17) has, in the stage provenance
of each sensor group, `origin` = `realtime` and a `coverage` object: `frames_in_take`,
`frames_processed`, `skips` (an object of counts by reason), `journal_crc_rejects`, `clean_close`,
`latency_ms` (`p50`, `p99`) and `events`. `origin` = `realtime` means that the run was folded from
the journal. Each stage of such a run has `origin` = `realtime`, also the stage `timing`, whose rows
the fold takes from the timing sidecars (SFF-844)
([ADR-1P4N](decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)
items 1 and 6). The latency of a result is `processed_ns` of its journal
record minus the group time of the frame (SFF-828). `p50` and `p99` are nearest-rank percentiles.
`events` is an array of the event objects of the journal that name this stage, in journal order
([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md)). So `events` of the stage
`timing` holds the events that name `timing`
([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 9). A posthoc run has `origin` =
`posthoc` and `coverage` null. A skipped frame of a realtime run has `x`, `y` and `visibility` all
null. A realtime run has no checkpoints, so posthoc processing never continues from realtime data
([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md) item 8). The values of `coverage`, for one sensor group and stage,
are these ([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 38c,
[ADR-N6KY](decisions/entries/N6KY-spec-v2-details-part-14.md) item 42; for the stage `timing`,
[ADR-1P4N](decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)):

- `frames_in_take` is `sample_count` of the sensor group.
- `frames_processed` is the number of frames with one or more good data records (SFF-843) of a
  channel of the group and stage
  ([ADR-783H](decisions/entries/783H-text-corrections-of-the-second-golden-review.md) item 2).
- For the stage `timing`, `frames_processed` is the number of frames with one or more good data
  records (SFF-843) of any channel of the group: the frames that the realtime pipeline handled. A
  channel of the group is a channel that the journal header declares with that `sensor_group`. A
  rejected record and a cut record are not good
  ([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 7). Each
  frame has a time. This count is about the realtime pipeline, not about the `TIMESTAMPS` rows.
- `skips` is `{"no_record": frames_in_take − frames_processed}`: the journal holds no reason.
- `journal_crc_rejects` is `rejected_records` of the journal at the time of the fold (SFF-843). It
  also counts a record with a wrong `length`.
- `clean_close` is true when the journal has a good end record.
- The latency of a data record that counts in SFF-845 is `processed_ns` − m, where m is the group
  time of SFF-828 in nanoseconds, from the times of the frames at the time of the fold (SFF-844).
  For the stage `timing`, there is one latency for each frame of `frames_processed`: the lowest
  latency of the records of that frame, of all channels of the group, that count in SFF-845: for
  one channel and frame, only the last record in file order
  ([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 8). For k
  latencies in increasing order, `p50` is latency ⌈0.5 × k⌉
  and `p99` is latency ⌈0.99 × k⌉, counted from 1, each as the float64 nearest to ns / 10^6. Each
  is null when k is 0. A later rewrite of the times (SFF-833) does not change `latency_ms`
  ([ADR-1P4N](decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)
  item 7).
- An event has `time_ns` (an integer JSON number: the host-clock time of the change, relative to
  the take start), `stage` (a processing stage), `parameter` (a text) and `value` (a JSON value).
  The `stage` of an event is `timing` or the `stage` of a channel that the journal header declares.
  The fold fails on each other event (SFF-844).

**SFF-835** (reader) A reader gives the take warning `realtime_run` one time when a run has a stage
provenance with `origin` = `realtime`. The reader result holds only the code. The text "Realtime
run: N/M frames processed, causal filters, may contain dropped and extrapolated frames" is guidance
for the program that shows the take: that program shows it for each camera sensor group, where N is
`frames_processed` and M is `frames_in_take` of the `coverage` of the stage `observations`, and it
shows a badge for the realtime run
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md); the badge: [ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md) item 8).

**SFF-836** (writer) The ChArUco observations of a calibration take are rows of the Parquet,
with the channel kinds of parts/parquet-descriptor.md. They are not in a separate file. The source
is `charuco_detector:<squares_x>x<squares_y>` of the board, for example `charuco_detector:5x3`. The
board has no name member. Each name is `corner_<id>`, where `<id>` is the OpenCV corner ID, in
decimal ([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 37).

**SFF-837** (reader) When the camera geometry stored in a run (`camera_geometry`) does not agree
with the calibration TOML of the take, a reader uses the stored geometry for that run and gives the
take warning `calibration_mismatch`. The two agree when each of these is true for each camera,
linked by `camera_key`: the image size is equal; `fx`, `fy`, `cx`, `cy`, `k1`, `k2`, `p1` and `p2`
each differ by 1e-6 or less; and the pose relative to the camera with `index` 0 differs by 1e-6 or
less in each value of the rotation matrix and in each value of the translation in millimetres. A
rigid change of the world does not change a relative pose. So an alignment by `person` or `charuco`
gives no `calibration_mismatch`
([ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-838** (writer) freemocap writes the Parquet whole (SFF-786), while it holds
`.processing.lock`, then writes the processing info JSON (section 14), then updates the manifest.

## 17. Realtime journal

freemocap writes the realtime tracking results of a take to `<rec>_realtime_journal.bin` while the
take runs, and folds it into a Parquet run at the end
([ADR-Q9X2](decisions/entries/Q9X2-realtime-tracking-journal.md)). The journal is a binary file of
framed records. Each multi-byte integer and float in it is little-endian.

Guidance for programs: the journal writer is a node of its own in the freemocap realtime pipeline:
a subscriber with its own queue, so that the aggregator and the cameras never wait for the disk. The
journal is the binary file of freemocap. The rule that skellycam writes only standard media and
human-readable sidecars does not apply to it
([ADR-Z641](decisions/entries/Z641-program-guidance-gate-2-scope-and-no-push.md) item 1).

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
| 1 | header | UTF-8 JSON (SFF-702): `skellyspecs` (`"realtime_journal"`), `format_version`, `format_prerelease`, `writer`, `take_uuid`, `origin` (`"realtime"`) and `channels`: an array of channel declarations, each with `channel_index` and the members of a Parquet channel (section 16) |
| 2 | data | `channel_index` (`u16`), `frame_number` (`i32`, the Parquet `frame_number` of SFF-827), `processed_ns` (`i64`, the host-clock time at which the pipeline finished the result, relative to the take start), `n` (`u32`, the number of names), `k` (`u32`, the number of components), then n × k `f32` values in name order, then component order |
| 3 | event | UTF-8 JSON: a parameter change, with `time_ns`, `stage`, `parameter` and `value` (SFF-834). `stage` is `timing` or the `stage` of a channel of the header (SFF-844) |
| 4 | end | UTF-8 JSON: `data_records` (the number of data records that the writer wrote) and `clean_close` (`true`) |

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
outside the take ([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md)).

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
not a rejected record. The scan is this
([ADR-N6KY](decisions/entries/N6KY-spec-v2-details-part-14.md) item 43):

- The scan starts at offset 0. At each step, it finds the first `magic` at or after its position.
  o is the offset of that `magic`.
- The record is **cut** when the file ends before o + 8, or when `length` is from 1 to 2^26 and
  the file ends before o + 12 + `length`.
- A record that is not cut is **rejected** when `length` is not from 1 to 2^26, or when `crc32` is
  wrong. Else it is **good**.
- After a good record, the scan goes on at o + 12 + `length`. After each other `magic`, it goes on
  at o + 4. The scan ends when it finds no `magic`.
- `records` is the number of good records, of each type.
- The first cut record after the last good record is the torn tail. `torn_bytes` is the number of
  bytes from its o to the end of the file. A cut record with a good record after it is a rejected
  record (a wrong `length`). A rejected record after the start of the torn tail does not count.
- With no torn tail, `torn_bytes` is the number of bytes (1 to 3) of a start of `magic` at the end
  of the file, else 0. Bytes that hold no `magic` count in no member.
- The journal has an end record when a good record of the type 4 exists.

A journal with one or more rejected records is `damaged` (reason
`crc_mismatch`, also when the cause is a wrong `length`). A
journal with a torn tail, or with no end record, is `unfinished` (SFF-791). When both apply, the
journal is `damaged` (SFF-886). A reader refuses a journal whose header declares a channel with a
`dtype` that is not `float32`, or a channel of the kind `TIMESTAMPS` (state `invalid`, reason
`bad_schema`) ([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md),
[ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-844** (writer) At the end of the take, freemocap folds the journal into a new Parquet run
with `origin` = `realtime` and its coverage block (section 16). freemocap starts the fold only after
`state` of the manifest is `finished` (SFF-724). The one exception is the fold of a left-over
journal as part of a repair that the user agreed to (SFF-793,
[ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).
The fold writes each event record into
`coverage.events` of the stage that the event names, for each sensor group that has a stage
provenance of that stage (SFF-834). The fold fails when an event names a stage that is not `timing`
and not the `stage` of a channel of the header. A failed fold writes no run
([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 9). Then
freemocap keeps the journal (SFF-845)
([ADR-1P4N](decisions/entries/1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md)
item 5). The fold takes
`timestamp_s` of each
row and the value of each `TIMESTAMPS` row from the timing sidecars of the take (SFF-828), not from
the journal. The fold uses the player times that the sidecars give at the time of the fold. For a
sidecar with no fit, for example after a crash, that time is the arrival time (SFF-781). The
latency of `coverage` also uses these times (SFF-834). A later
repair adds a fit to the sidecar, and freemocap then rewrites the times of the run (SFF-833).

**SFF-845** (writer) freemocap deletes the journal only after it has read the new Parquet run
back and compared the count and the digest of the folded values with the journal. The digest is the
SHA-256 of these bytes: for each channel in order of `channel_index`, for each `frame_number` in
increasing order, the n × k values in record order, each as a little-endian float32. When two
records have the same channel and frame, only the last in file order counts. A missing value (NaN in
the journal, null in the Parquet) is the bytes `00 00 C0 7F`. The count is the number of these
values. A null row of a frame with no record is not in the count or the digest
([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md)).
When the fold or the check fails, freemocap keeps the journal. No program folds a journal
automatically at start-up. freemocap folds a left-over journal of an unfinished take only as part of
a repair that the user agreed to (SFF-793). When the user does not agree, freemocap keeps the journal
and changes no file
([ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)). freemocap
folds a journal that is left over in a take whose manifest already has `state` `finished` only
after it asks the question of SFF-793 and the user agrees
([ADR-JB3A](decisions/entries/JB3A-repair-state-question-and-skellycam-lock.md)).

**SFF-846** (provisional: the journal load test and the kill test DT11) Before freemocap writes
the journal in a release, a load test runs a full realtime session with the journal writer on and
off and compares the aggregator latency and the dropped frames, and a kill test with real data
passes.

## 18. Blender outputs, annotated videos, exports and logs

These files are in formats of other projects. For each, this section gives the name, the container
and codec, and the content mapping ([ADR-QS7B](decisions/entries/QS7B-blender-outputs-and-exports.md)).

A name with no run number is always a name of run 0. Each file of a run N other than 0 has `run-<N>`
in its name. Each subsection gives the place of `run-<N>` for its files. A writer does not rename or
replace a file of this section when the selected run changes. `selected_run_id` of the processing info JSON
(section 14) names the selected run ([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).
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

(provisional: exports are not in gate 2) This section waits for the port of the freemocap
exporter. G3 holds no export, and SFT-743 has no golden part until then ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 12).

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
inventory last ([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md)).

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
info JSON, Parquet or calibration ([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md)).

**SFF-862** (writer) (provisional: the skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO)
skellysync writes one camera file and its sidecar for each camera, and,
when its input has audio, one audio file and its sidecar, with the rules of sections 6 to 10. Its
`clock` is `synthetic`. Its `camera_key` can be 0.

**SFF-863** (reader) (provisional: the skellysync decisions D-Q, D-FPS, D-HDR, D-DRIFT and D-AUDIO)
A reader does not give the warning `missing_fit` for a file whose `clock`
is `synthetic`.

## 20. Opening a folder

**SFF-864** (reader) A device pair is a file in the media folder whose name ends in `.csv` and
whose first line is `# skellyspecs=video_timing` or `# skellyspecs=audio_timing`, with the
media file of the same stem and the suffix `.mkv` (video) or `.m4a` (audio). A camera file starts with
the EBML magic `1A 45 DF A3`. An audio file has `ftyp` as its first box.

**SFF-865** (reader) A media file of the media folder with no timing sidecar of this format, and a
timing sidecar with no media file, are not in a device pair. A media file alone has no mark of this
format. A reader lists it in `other_files` with the state `not_in_format`. A timing sidecar alone,
with a `take_uuid` that the reader can read, is in the `files` of its take when that take exists
(SFF-866). Its `name` is the path of the missing media file. Its state is `invalid`, with the reason
`missing_media`. It does not count as a camera file or an audio file in SFF-869. When no such take
exists, the item is in `other_files`, with the same state and reason. In `other_files`, its `name`
is the path of the sidecar: `other_files` lists files that exist
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 33). A timing sidecar
alone whose `take_uuid` the reader cannot read is in `other_files`, with the state `invalid` and
the reason of SFF-748: `missing_metadata` when the header has no `take_uuid`, else `bad_metadata`
([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 5,
[ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 4). For
each of these files, the reader gives the folder warning `orphan_file`
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md)).

**SFF-866** (reader) A reader groups the device pairs by `take_uuid`. A take exists for each
`take_uuid` that one or more device pairs hold. When the folder holds more
than one `take_uuid`, it reports each take and gives the folder warning `multiple_takes`.

**SFF-867** (reader) A manifest belongs to the take whose `take_uuid` it holds. A reader uses the
manifest only for that take. The take member `manifest` (SFF-885) is `missing` only when
`recording_manifest.json` does not exist. It is `invalid` when the file exists and the reader does
not use it for the take: the file is not valid JSON, is not a manifest of this format, or holds
another `take_uuid`. The reader then rebuilds the links (SFF-731). The manifest is never an item of
`folder_files`. A manifest that no take of the folder uses is in `other_files`, with the state
`invalid`. Its reason is `take_fact_mismatch`, with the folder warning `orphan_file`, when it holds
a `take_uuid` (SFF-889). Else its reason is `bad_schema`, with no `orphan_file`
([ADR-PVG8](decisions/entries/PVG8-spec-v2-details-part-10.md) item 25).

**SFF-868** (reader) A reader takes `<rec>` from the manifest. When it rebuilds the links, it
takes `<rec>` from the name of a timing sidecar file. For a camera sidecar, `<rec>` is the name
without the suffix `.<camera_label>.csv`. For an audio sidecar, `<rec>` is the name without the
suffix `.audio.csv`. A take with only an audio sidecar uses the audio sidecar name. When the
sidecars give two or more values, it gives the take warning `take_fact_mismatch`. It then uses the
value of the video sidecar with the lowest `group_position`, as SFF-871 does for a take key. A take
with no video sidecar uses the audio sidecar
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 34).

**SFF-869** (reader) When a take has fewer camera files than `group_size`, or fewer audio files
than `audio_count`, the reader reports the take as `incomplete`, with the warning `incomplete_take`,
and it opens the other files. When it has more, it gives the warning `extra_files`. A camera pair
or an audio pair that is `invalid` or `unsupported_version` (a refused pair) counts as a present
file of the take wherever the reader counts the files of the take: for the take state, so the take
stays `complete`, and also for `extra_files`. The state of that file is the report
([ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 1,
[ADR-783H](decisions/entries/783H-text-corrections-of-the-second-golden-review.md) item 7).
This rule is about the counts only. A refused pair stays out of the take-level checks (SFF-871,
[ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 2,
[ADR-64ER](decisions/entries/64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) item 3).

**SFF-870** (reader) When two camera files of one take have the same `camera_label`, the reader
gives the warning `duplicate_label` and keeps both files.

**SFF-871** (reader) When the timing sidecars of one take disagree on a take key
(SFF-749), the reader gives the warning `take_fact_mismatch` and uses the values of the
camera with the lowest `group_position`. A timing sidecar that the reader refuses (state
`invalid`) is not in the take-level checks: it causes no `take_fact_mismatch` (this requirement and
SFF-868) and no `summary_stale` (SFF-729). Its own state `invalid` is the report
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 2).

**SFF-872** (reader) A reader checks the links of the take and reports each check (section 23):

| Check | Rule |
|---|---|
| `take_uuid` | The manifest, each timing sidecar, both info JSONs, the Parquet descriptor and the journal header hold the take's `take_uuid` |
| `camera_key` | The `camera_key` of each manifest camera is in exactly one video sidecar, in `camera_configs` of the capture info JSON, in one camera table of the calibration TOML (when the take has one) and in one camera source of the Parquet (when it has one) |
| `frames` | Each Parquet `frame_number` of a camera is from 0 to the number of rows of its video sidecar minus 1. The finished camera files of the take have the same number of rows |
| `dimensions` | `width` and `height` of each image reference frame `camera:<camera_label>:image` of the Parquet (SFF-829) are the width and height of the stored JPEG frames of that camera file. The check compares nothing else ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 6) |
| `rotation` | The capture info JSON holds no rotation. The `display_rotation` of the summary agrees with the sidecar |
| `files` | Each path of the manifest, and each file name of the Parquet camera sources, names a file that exists. For a file name `<name>` of a Parquet camera source, the check tests `synchronized_videos/<name>` (SFF-826) |
| `hashes` | The `sha256` of the manifest calibration is the SHA-256 of the TOML. `parquet_sha256` of the processing info JSON is the SHA-256 of the Parquet |
| `calibration` | The `calibration_uuid` of the manifest is the `calibration_uuid` of the TOML |

`frames` is also `mismatch` when the finished camera files of a take have different numbers of rows
(SFF-754). The row-count part of `frames` compares the camera files with the state `finished`. A
reader evaluates it when the take has two or more of them. A camera file that is `repaired`,
`unfinished` or `damaged` is not in the comparison: a crash and a repair cut each camera pair at
its own place (SFF-795). When the take has no Parquet, the row-count part alone decides `frames`:
for the scope `full`, the check is `ok` when the reader evaluates the part and the row counts are
equal; for the scope `player`, it is `not_checked` (SFF-892)
([ADR-94YQ](decisions/entries/94YQ-golden-g1-review-decisions.md) item 4). SFF-754 gives the multi-camera frames when the values of `rows` differ
([ADR-W6HV](decisions/entries/W6HV-spec-v2-details-part-3.md),
[ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 32).

A check has one part for each file, or pair of files, that its rule tests. The parts are
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 31):

- `take_uuid`: one part for each of the manifest, each timing sidecar, each info JSON, the Parquet
  and the journal;
- `camera_key`: the manifest with the video sidecars; with the capture info JSON; with the TOML;
  with the Parquet;
- `frames`: the Parquet with each video sidecar; the row counts of the camera files;
- `dimensions`: the Parquet with each camera file;
- `rotation`: the capture info JSON alone; the manifest summary with each video sidecar;
- `files`: the paths of the manifest; the file names of the Parquet;
- `hashes`: the manifest with the TOML; the processing info JSON with the Parquet;
- `calibration`: the manifest with the TOML.

A reader does not evaluate a
part when a file that the part needs is absent, is `invalid` or `unsupported_version`
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 7), or is a file that the scope of the
result does not read (SFF-892). The state of a check is `mismatch` when an evaluated part fails,
`ok` when one or more parts
are evaluated and none fails, and `not_checked` when no part is evaluated. So, with no manifest,
`calibration` and `camera_key` are `not_checked`, `hashes` has only its Parquet part, `files` has
only its Parquet part and `rotation` has only its capture info part
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)). A capture info JSON of version
2.0 that holds the member `rotation`, which SFF-800 forbids, stays `present`: its part of `rotation`
fails, and the check is `mismatch`
([ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 2).

**SFF-873** (reader) When a camera has `camera_key` 0, a reader links it by `camera_label` and
gives the warning `camera_key_zero`.

**SFF-874** (reader) A `hashes` mismatch of `parquet_sha256` gives the warning
`stale_processing_info`. It does not make the take or the Parquet invalid. (freemocap replaces the
Parquet and the processing info JSON one after the other, and a crash between the two leaves a stale
hash.)

## 21. Legacy folders

The rules of [ADR-CZQ9](decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md)
apply. This section tells how a reader recognises a legacy folder and what it reports. The code that
reads the old files is in skellycam and freemocap. The informative
[legacy annex](legacy-annex.md) describes the files of each layout.

This section also gives the rules to read the camera files and the time files of a FreeMoCap v1
folder: SFF-896 to SFF-903, in
[Section 21, continued](#section-21-continued-the-camera-files-of-a-v1-folder) at the end of
section 23. They are there because each new ID comes after the last ID of the file (section 2)
([ADR-91PB](decisions/entries/91PB-choices-for-the-v1-camera-file-rules.md) item 1).

**SFF-875** (reader) A file of this format is one of these: a timing sidecar with the first line of
SFF-864; a JSON file whose `skellyspecs` member has a value of this spec; a TOML file with
`[metadata].calibration_uuid`; a Parquet file with a `freemocap.recording` descriptor of
`schema_version` 2; a journal with a header record; and a media file in a device pair. A media file
alone has no mark of this format (SFF-865)
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md)). A folder is legacy when it has no
file of this format, and it has one or more
regular files. A reader then reports the folder state `legacy` and does not change the folder. A
folder with a file of this format and no take is `unreadable` (SFF-888), not legacy. Examples are a
folder with only a timing sidecar of this format, and a folder with only `<rec>_data.parquet` of this
format. Only for the legacy recognition, a reader MAY read the subfolders that the signals of
SFF-876 to SFF-878 name: `SyncedVideos/`, `RawVideos/`, `synchronized_videos/timestamps/`,
`output_data/` and `output_data/raw_data/`. It reads no other subfolder (SFF-721,
[ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 5,
[ADR-783H](decisions/entries/783H-text-corrections-of-the-second-golden-review.md) item 10).

**SFF-876** (reader) A reader reports the family `pre_v1` for a folder with one of these: a
`SyncedVideos/` or `RawVideos/` subfolder and a
`<name>_config.yaml` or `sessionSettings.txt` file (v0.0.x); or a `synchronized_videos/Camera_NNN.mp4`
file with no `_synchronized` suffix, with `synchronized_videos/timestamps/Camera_NNN_binary.npy`
(v0.1.0). A folder that also has a signal of SFF-877 is `v1`. For `pre_v1`, `release_range` is null, `ambiguous` is false, and `eras` and `warnings`
are `[]`, as for `unknown` (SFF-877). The note "freemocap pre-v1 layout, unsupported" is guidance
for the program that shows the folder. It is not in the reader result
([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 29,
[ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 30c).

**SFF-877** (reader) A reader reports the family `v1` for a folder with
`synchronized_videos/*_synchronized.mp4` or `synchronized_videos/timestamps/*_synchronized_binary.npy`.
When a folder has a signal of `pre_v1` (SFF-876) and a signal of `v1`, `v1` wins
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 1). A legacy folder that is not `v1` and not `pre_v1` has the family `unknown`, with `release_range`
null, `ambiguous` false, and empty `eras` and `warnings`. Version 2.0 does not recognise the layout
of the freemocap development code
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md)).

**SFF-878** (reader) For a `v1` folder, a reader reports the narrowest release range that the
content proves, from this table. A row matches when each signal of the row is present. A key that
a signal names in `recording_parameters.json` counts at any depth of the JSON: as a member of the
top object or of a nested object ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 1). "as X" adds
the signals of row X. The rows that say "as" make a chain with the rows that they name: the rows
V1b–V1d and V1b–V1c are one chain, and the rows from V1e–V1h' to V1h' are one chain. Each other row
is a chain of one row. When the matched rows are in one chain, the reader reports the range of the
last matched row, and `ambiguous` is false. When they are in two or more chains, or no row matches,
the reader reports the range from the lowest first release to the highest last release of the
matched rows (v1.0.25 to v1.8.2 when no row matches), and `ambiguous` is true. It does not guess
([ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md)).

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

A V1i folder does not match the row V1e–V1h': v1.8.0 removed `run_reprojection_error_filtering`.
So only the row V1i matches, and `ambiguous` is false. "A TOML whose `cam_0` rotation is 0" means:
each of the 3 values of `cam_0.rotation` has a magnitude of 1e-6 or less. The TOML of a signal is
the one that SFF-880 gives with the state `present`. With another state, each TOML signal is absent
([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 30).

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
the state `present`, `missing` or `ambiguous`. `path` is null when the state is not `present`. The
lookup is only for `v1`: the member `calibration` is null for `pre_v1` and for `unknown`
([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 29).

## 22. Privacy and safety

The rules of [ADR-T8PK](decisions/entries/T8PK-privacy-notice-and-no-code-in-files.md) apply.
Private data is allowed in any field. This version gives no option to remove private data from the
files. Guidance for programs: freemocap shows a privacy notice when the user exports or shares a
take ([ADR-T8PK](decisions/entries/T8PK-privacy-notice-and-no-code-in-files.md) items 3 and 4).

**SFF-881** (writer) The manifest member `privacy` is an object with `fields` and
`media_shows_people`. `fields` is an array, sorted by `file` and then by `field`, each in the order of its UTF-8 bytes
([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 1). Each item has
`file` (a path), `field` (a JSON pointer, a TOML key path or a CSV header key) and `kind`:
`device_name`, `serial_number`, `device_path`, `user_entered_name`, `absolute_path`, `time_zone` or
`other`. `fields` holds exactly the fields of this table, when the file exists and the value is not
null. `<key>` is a key of `camera_configs`, and `<i>` is an index of the summary `cameras`.
`media_shows_people` is `true` when the take has a camera file, an audio file or a Parquet
([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md); the kinds of the manifest fields:
[ADR-1HH0](decisions/entries/1HH0-lock-startup-repair-and-reader-model-check.md); `os_device_id`:
[ADR-70VP](decisions/entries/70VP-camera-identity-forms-and-remembered-keys.md)).

| File | Field | Kind |
|---|---|---|
| The capture info JSON | `/camera_configs/<key>/user_name` | `user_entered_name` |
| | `/camera_configs/<key>/device/model` and `/camera_configs/<key>/device/os_name` | `device_name` |
| | `/camera_configs/<key>/device/serial` | `serial_number` |
| | `/camera_configs/<key>/device/port_path` | `device_path` |
| | `/camera_configs/<key>/device/os_device_id` | `device_path` |
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
([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md)). For an NPZ file that the
manifest lists, the reader reads the ZIP directory and, for each member whose name ends in `.npy`,
only the NPY header. It inflates only the bytes of the header when the member is compressed. It
reads no other member. A `descr` of an object type in one member makes the `folder_files` item
`invalid`, with the reason `code_in_file`. A file that is not a ZIP file, or a member with no NPY
header, makes the item `invalid`, with the reason `bad_schema`. The same reason applies to an NPY
file with no NPY header
([ADR-N6KY](decisions/entries/N6KY-spec-v2-details-part-14.md) item 45).

## 23. The reader result

A reader can give the result of opening a folder as JSON. The conformance tests and the golden files
use this result to compare readers
([ADR-KW3G](decisions/entries/KW3G-reader-result-for-the-folder.md)).

**SFF-885** (reader) The reader result is a JSON object with these members, serialised with the
JSON Canonicalization Scheme (RFC 8785). A result has no byte after the canonical JSON: it has no
line end ([ADR-W389](decisions/entries/W389-format-rules-from-the-golden-conventions.md) item 2):

- `result_version`: 2;
- `folder_state`: `ok`, `unreadable`, `legacy` or `empty` (SFF-888);
- `folder_warnings`: an array of warning codes;
- `takes`: an array, in order of `take_uuid`. Each take has `take_uuid`, `recording_name`, `state`
  (`complete` or `incomplete`), `manifest` (`present`, `missing` or `invalid`, SFF-867), `warnings`,
  `may_contain_private_data`, `files`, `folder_files` and `links`. In a `legacy` folder, `takes` is
  `[]`;
- each item of `files` (a media file and its sidecar, or a timing sidecar alone, SFF-865): `name`
  (the path of the media file, relative to the take folder, with `/`), `kind` (`camera` or `audio`),
  `state`, `reason`, `camera_key`, `camera_label`, `rows` (the number of data rows that SFF-746 lets
  the reader use), `torn_bytes` (SFF-791), `fit` (true only when the sidecar is finished or
  repaired, holds fit lines and the reader
  uses them, SFF-747; false when the reader computes a fit, SFF-784), `warnings` and, when the test asks for
  them, `records`. An audio item has `camera_key` and `camera_label` null. An item with the state
  `invalid` or `unsupported_version` has `rows`, `torn_bytes` and `fit` null. It also has `records`
  null, not `[]`, also when the test asks for `records`. For each other state,
  `torn_bytes` is an integer. For each state, also `invalid` and `unsupported_version`, the
  `camera_key` and `camera_label` of a camera item are the header values only when the reader can
  read their header lines and the value has the correct form (section 8). A value of the wrong form
  is null. A reader of an unknown `major` checks the form of version 2.0
  ([ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) items 1 and 3,
  [ADR-783H](decisions/entries/783H-text-corrections-of-the-second-golden-review.md) item 8,
  [ADR-7JJJ](decisions/entries/7JJJ-audio-repair-refused-header-values-and-the-rules-of-w5ak.md) item 11;
  the form of an unknown `major`:
  [ADR-64ER](decisions/entries/64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md) item 1);
- each item of `records`: `[position, source_frame_number, arrival_ns, sample_ns, player_ns]` for a
  camera, and `[block, first_sample, n_samples, host_ns, fitted_ns]` for audio. An absent value is
  null. `rows` counts the `missing` rows. A `records` item of a row with no time has `arrival_ns`,
  `sample_ns` and `player_ns` null
  ([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 1).
  For an unfinished camera file, `records` holds only the usable frames (SFF-740). For an
  unfinished audio file, `records` holds only the blocks whose every sample is in a complete
  fragment (SFF-792).
  `fitted_ns` is the fitted time of the `first_sample` of the block (SFF-779), with the fit that
  the reader uses: the fit lines of a finished or repaired sidecar, else the fit that the reader
  computes (SFF-784). It is null when the reader has no fit
  ([ADR-0WTH](decisions/entries/0WTH-spec-v2-details-part-12.md) item 35);
- each item of `folder_files`: `path`, `role`, `state` (`present`, `missing`, `invalid`,
  `not_checked`, `unsupported_version`, `unfinished` or `damaged`), `reason` and `warnings`.
  `folder_files` has one item for each `files` item of the manifest, one for `calibration.file`, and
  one for each root file with a fixed name of SFF-731 that exists. `role` is the role of the
  manifest item. The item of `calibration.file` has the role `calibration`
  ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 3). In a rebuild, `role` comes from the fixed name (SFF-731). An item is `missing` only when
  the manifest names a path that does not exist. In a rebuild, the list holds only the files that
  the reader finds. The item of the journal also has three integer members: `records` (the number of
  good records), `rejected_records` and `torn_bytes` (SFF-843). Each of the three is null when the
  journal is `not_checked` (SFF-892);
- each item of `links`: `check` (a name of SFF-872), `state` (`ok`, `mismatch` or `not_checked`)
  and `detail`. `detail` is null in the canonical result. A reader can give a text outside the
  result. `links` holds each check of SFF-872 one time, in the order of that table;
- `other_files`: an array of the files of the root and the media folder that are in no take, each
  with `name` (a path relative to the take folder, with `/`), `state` and `reason`. `name` is the
  path of a file that exists (SFF-865). A file whose
  name ends in `.tmp` or starts with `.`, and `<rec>.blend1`, is in no list of the result. In a
  `legacy` folder, `other_files` follows the same rule: it lists each file of the root and of
  `synchronized_videos/`, not of their subfolders, as `not_in_format`, or as `invalid` with
  `code_in_file` for a pickle (SFF-884)
  ([ADR-YYE3](decisions/entries/YYE3-spec-v2-details-part-11.md) item 29);
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
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md),
[ADR-0XX2](decisions/entries/0XX2-spec-v2-details-part-5.md),
[ADR-72QQ](decisions/entries/72QQ-spec-v2-details-part-8.md)).

**SFF-886** (reader) The file states are `unsupported_version`, `invalid`, `damaged`,
`unfinished`, `repaired`, `finished` and `not_in_format`. When two apply, the reader reports the first
in this order: `unsupported_version`, `invalid`, `damaged`, `unfinished`, `repaired`, `finished`. A
file that this spec makes a reader refuse is `invalid`, with one reason code. These are the states of
the items of `files` and `other_files`. A folder file has the states of SFF-885. When two of
`unsupported_version`, `invalid`, `damaged` and `unfinished` apply to a folder file, the reader
reports the first in the same order. A folder file with a `major` that the reader does not know is
`unsupported_version` (SFF-708). The `reason` of an item with the state `unsupported_version` is
null ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 7). Of the folder files, only the journal is a live file (SFF-787):
`unfinished` and `damaged` are states of the journal (SFF-843).

**SFF-887** (reader) The reason codes are `bad_metadata`, `missing_metadata`, `bad_rate`,
`bad_rotation`, `bad_label`, `bad_time`, `crc_mismatch`, `take_fact_mismatch`, `missing_media` (a
timing sidecar with no media file, SFF-865), `bad_schema` (a JSON, TOML or Parquet file, or a journal
header, without the members or the columns of its section, or a journal header with a channel that
SFF-843 refuses; a manifest that no take uses and that holds no `take_uuid`, SFF-867; an NPY file
with no NPY header, an NPZ file that is not a ZIP file, or an NPZ member with no NPY header,
SFF-884; int64 in the Parquet columns `frame_number` and `run_id` is
not a cause, SFF-819; the member `rotation` in the capture info JSON is not a cause, SFF-872) and
`code_in_file`. Each reader makes a file `invalid` with `bad_time` when a
row time or a fitted time has a magnitude of 2^53 ns or more. The take warnings are
`incomplete_take`, `duplicate_label`, `take_fact_mismatch`, `extra_files`, `manifest_missing`,
`camera_key_zero`, `stale_processing_info`, `summary_stale`, `calibration_mismatch`
and `realtime_run`. The file warnings are `missing_fit`, `encode_skip`, `gap` and `prerelease`. A
reader gives the file warning `encode_skip` when one or more usable rows have that flag. In the
same way, it gives a camera file the file warning `gap` when one or more usable rows have the flag
`gap` (SFF-756) ([ADR-94YQ](decisions/entries/94YQ-golden-g1-review-decisions.md) item 1). The
folder
warnings are `multiple_takes`, `stray_tmp` and `orphan_file`. The legacy warnings are those of
SFF-879. A reader reports each
code that this spec names, and no other
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md),
[ADR-ATW0](decisions/entries/ATW0-spec-v2-details-part-6.md)).

**SFF-888** (reader) `folder_state` is `ok` when the folder has one or more takes,
`unreadable` when it has no take but one or more files of this format, `legacy` by SFF-875, and
`empty` when it has no regular file. A folder that holds only a TOML, a Parquet or a journal of
this format is `unreadable` in the two scopes (SFF-892, [ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 10).

**SFF-889** (reader) A file of this format (SFF-875) whose `take_uuid` a reader can read is in
the `files` of its take, also when it is `invalid`. A folder file is in the `folder_files` of its
take: the take whose manifest lists it, or the take whose `<rec>` its fixed name has. A folder file
that holds another `take_uuid` than its take stays in the `folder_files` of its take, with the state
`present`. The link check `take_uuid` is then `mismatch` (SFF-872)
([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 4,
[ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 5). Other files are in `other_files`. A folder file of this format that has no take is in
`other_files` with the state `invalid` and the reason `take_fact_mismatch`: in a folder with no
take, and in a folder with a take when no manifest lists the file and its name has the `<rec>`
of no take
([ADR-158N](decisions/entries/158N-details-for-the-decisions-of-round-3.md) item 13). Each file of this format
that is alone gives the folder warning `orphan_file` (SFF-865)
([ADR-Q4BK](decisions/entries/Q4BK-spec-v2-details-part-4.md)). The manifest is never in
`folder_files`: SFF-867 gives its place.

**SFF-890** (reader) Takes are in order of `take_uuid`. The camera files are in order of
`group_position`, then by the bytes of the file name, and the audio file is last. `folder_files` and
`other_files` are in order of the bytes of the path. `links` is in the order of the table of
SFF-872. Each `warnings` array is sorted by code point.

**SFF-891** (reader) The readers of skellycam, skellysync, freemocap and the Blender addon, in
Python and in JavaScript ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)), read a file with
`format_prerelease` > 0 and give it the warning `prerelease`. They treat each value above 0 in the
same way. Another reader MAY refuse it as
`unsupported_version`
([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 8). A file with
the state `invalid` or `unsupported_version` also gets the warning `prerelease` when the reader can
read its `format_prerelease` and the value is above 0 ([ADR-XR63](decisions/entries/XR63-reader-rules-of-the-golden-review.md) item 7,
[ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 6,
[ADR-FB8P](decisions/entries/FB8P-refused-pairs-rotation-member-invalid-files-audio-records-legacy-subfolders.md) item 3). The manifest is not an item of the result (SFF-889), so its
`format_prerelease` gives no warning: each other file of the take has the warning
([ADR-94YQ](decisions/entries/94YQ-golden-g1-review-decisions.md) item 3).

**SFF-892** (reader) A reader gives its result for a scope: `full` or `player`. The scope is an
input of the read. It is not a member of the result. The scope `full` is the whole result of
SFF-885. The scope `player` is the result for the files that a player needs: the media files, the
timing sidecars and the JSON files. A reader that is asked for a scope gives exactly the result of
that scope, whichever reader it is. For the scope `player`, a reader reads no TOML file, no
Parquet file, no journal, no NPY file and no NPZ file. It reads no NPY header. The `player` result
of a folder is the `full` result of that folder with only these changes:

- `folder_files`: an item of a TOML, a Parquet, a journal, an NPY file or an NPZ file that exists
  has the state `not_checked`, `reason` null and `warnings` `[]`. The three integers of the journal
  item are null. A `missing` item stays `missing`.
- `links`: `frames`, `dimensions`, `hashes` and `calibration` are `not_checked`, also the row-count
  part of `frames`. Each other check has only the parts of SFF-872 that need no TOML, Parquet or
  journal.
- Take warnings: the result has no `stale_processing_info`, `calibration_mismatch` or
  `realtime_run`.
- The reader finds the mark of SFF-875 only in a timing sidecar, a JSON file and a media file of a
  device pair. A TOML, a Parquet or a journal that is in no `folder_files` list is `not_in_format`
  in `other_files`, with no `orphan_file`. The only exception is `folder_state`: when the folder
  has no take, the reader also looks for the mark of SFF-875 in each TOML, Parquet and journal of
  the root. It reads only the part of the file that holds the mark: the `[metadata]` table of a
  TOML, the key-value metadata of a Parquet footer and the header of a journal
  ([ADR-W5AK](decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 8). So a
  folder that holds only one of these files of this format is `unreadable`, as for the scope
  `full` (SFF-888).
- `legacy`: `family` and `calibration` do not change. For `v1`, the reader reads no era signal. It
  reports as when no row matches (SFF-878): `release_range` `["v1.0.25","v1.8.2"]`, `ambiguous`
  true, `eras` `[]` and the four warnings of SFF-879.

A Python reader supports the two scopes. A JavaScript reader supports only the scope `player`.
Through its test adapter ([conformance.md, "The test adapter"](conformance.md#the-test-adapter)), a
Python reader is `read_folder(path, records=False, scope="full")`, and a JavaScript reader is a
command that writes the canonical JSON to standard output, and no other byte. So a Python reader
with the scope `player` and a JavaScript reader give the same bytes for the same folder
([ADR-DM9S](decisions/entries/DM9S-spec-v2-details-part-7.md),
[ADR-0JVZ](decisions/entries/0JVZ-spec-v2-details-part-9.md) item 21, [ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).

**SFF-893** (reader) This requirement belongs to section 16. A reader ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)) checks the
structure of each `RecordedModel` of the descriptor and of its nested types, as
parts/parquet-descriptor.md section "Structure rules and writer rules" gives it: each member is
present, except a member that its row lets the writer omit and a member whose row gives a default;
a member that its row lets the writer omit when null can also be null
([ADR-H2HQ](decisions/entries/H2HQ-descriptor-members-deferred-points-and-old-audio.md) item 2);
each member has its JSON type; and a closed type has no other member. For this check, an "integer" is a JSON number with no fraction in
its value (`1` and `1.0` pass), a "float" is each JSON number, and a text is a JSON string
([ADR-6VRQ](decisions/entries/6VRQ-spec-v2-details-part-13.md) item 39). A structure fault makes the `folder_files` item of the Parquet
`invalid`, with the reason `bad_schema`. In version 2.0, the reader does not check a writer rule of
the part: it does not refuse a model that breaks only a writer rule
([ADR-W5JC](decisions/entries/W5JC-nested-model-types-in-the-descriptor-part.md) item 3).

**SFF-894** (writer) This requirement belongs to section 12. When the process that writes a camera
pair ends during a take with no normal end of its files (a hang, a kill), the program that records
the take completes that pair at the end of the same take, in the same run, after that process has
ended. It cuts the camera file and the sidecar as SFF-795 gives, appends no byte to the camera file,
and appends a `missing` row with empty byte fields (SFF-754) for each multi-camera frame up to the
number of rows of the take. That number is the number of multi-camera frames that the program
counted, or, when it counted none, the largest number of rows of the other sidecars of the take
([ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 10). Then it appends the `# repair` line and the `# end` line. It writes the
fit lines of SFF-795 only when it has a fitter. This is not the repair of SFF-793: the program does
not ask the user. A reader reports the pair as `repaired` (SFF-795)
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 4).
The program completes a camera pair after a write to its camera file failed (SFF-754) in the same way
([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 3).

**SFF-895** (reader) This requirement belongs to section 5. A reader parses the `detail` of
`camera_dead` and of `camera_file_short` (SFF-727) as keys and values: each key is followed by `=`,
the keys are separated by one space, the values of p, b and r are integers in the form of SFF-701
(or `none` for p), and the value of `reason` is the rest of the text. A player shows "camera lost at
frame N" with N = p + 1, and N = 0 for `none`
([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md) item 5).
When a `detail` does not parse, the player shows the warning of the code with no frame number. The
codes of SFF-727 are not warnings of the reader result: SFF-887 does not change
([ADR-5B03](decisions/entries/5B03-choices-for-the-format-changes-f1-to-f10.md) item 7).

### Section 21, continued: the camera files of a v1 folder

Status: **draft, for review at gate 1.** SFF-896 to SFF-903 belong to section 21. Each one has the
draft form of section 2: the word "Draft" before its ID. They tell how a program reads the camera
files and the time files of a FreeMoCap v1 folder: which folders it reads, the time file, the frame
table of a camera file, the multi-camera frames and the time map
([ADR-3XYN](decisions/entries/3XYN-v1-camera-file-rules-move-to-recording-files.md),
[ADR-91PB](decisions/entries/91PB-choices-for-the-v1-camera-file-rules.md)). Each program that
plays, processes or converts a v1 folder follows them. In these requirements, "a reader" is such a
program. They add no member to the reader result (section 23), and they do not change SFF-875 to
SFF-880. The codes in these requirements (`time_file_unusable`, `no_index`, `index_damaged`,
`no_video_track`, `extra_tracks`, `edit_list_not_supported`, `index_mismatch`,
`frame_count_differs` and `no_frames`) are for the report of the program. They are not warnings of
the reader result. Where the spec of a program states the same rule as these requirements, these
requirements win ([ADR-91PB](decisions/entries/91PB-choices-for-the-v1-camera-file-rules.md)
item 11). The [legacy annex, section 9](legacy-annex.md#9-the-camera-files-and-the-time-files-of-v1)
gives the background.

**Draft SFF-896** (reader) This requirement belongs to section 21. The camera files of a legacy folder
(SFF-875) are the files of `synchronized_videos/` whose name ends in `.mp4`, in any case. A reader
applies these rules in this order:

1. A folder whose `synchronized_videos/` holds a file whose name ends in `.id-<n>.idx-<n>.mp4`, with
   `<n>` one or more decimal digits and `.mp4` in any case, is a v2 alpha folder. Its family is the
   family that SFF-876 and SFF-877 give. A reader does not read its camera files. It refuses the
   folder with a message that says that FreeMoCap v2 alpha recordings are not supported, for example
   "FreeMoCap v2 alpha recordings are not supported".
2. A folder of the family `pre_v1` (SFF-876) with one or more camera files is a v0.1.0 folder. A
   reader does not refuse it. It reads its camera files as in rule 3. This spec has no test for such
   a folder and gives no promise for it.
3. A reader reads the camera files of each other legacy folder with one or more camera files by
   SFF-897 to SFF-903. This includes a folder of the family `unknown` whose camera file names do not
   end in `_synchronized.mp4`, for example the official FreeMoCap sample data and a folder of the v1
   "import videos" wizard.
4. A legacy folder with no camera file has no camera file to read. A reader that was asked to play
   or process it reports that the folder has no camera file, for example "no camera files: no
   synchronized_videos/*.mp4". For a folder that is not of the family `v1`, it MAY say that the
   folder is not a FreeMoCap v1 recording.

For these rules, a reader reads only the camera files and their time files. It does not read the
`_timestamps_human_readable.csv` files, the PNG files of `synchronized_videos/`, `annotated_videos/`,
`output_data/` or the other results of the processing.

**Draft SFF-897** (reader) This requirement belongs to section 21. The time file of the camera file
`synchronized_videos/<stem>.mp4` (in any case of `.mp4`) is
`synchronized_videos/timestamps/<stem>_binary.npy`. A reader uses no other name rule. It parses the
NPY format itself:

- The file starts with the magic `\x93NUMPY`, then the version: the bytes `1 0`, `2 0` or `3 0`.
  Then comes the length of the header as a little-endian unsigned integer: 2 bytes for version 1.0,
  4 bytes for the versions 2.0 and 3.0. The header follows. The values start after the header.
- The header is ASCII text. It is one Python dictionary literal, then zero or more spaces, then one
  `\n`. The dictionary holds exactly the keys `descr`, `fortran_order` and `shape`, each one time,
  in any order. Each key is in single or double quotes. The value of `descr` is a string in single
  or double quotes. The value of `fortran_order` is `False` or `True`. The value of `shape` is a
  tuple of decimal integers in Python form, for example `(6,)` or `(6, 1)`. A tuple of one item
  has its `,`. Spaces can come before and after
  each `:`, each `,` and each bracket. A `,` can come after the last item of the dictionary and of
  the tuple. A header in any other form is a `bad_header`.
- It accepts only `descr` `'<f8'`, `fortran_order` `False` and a shape `(n,)`.

The time file is usable when the parse passes, the file holds exactly n values of 8 bytes after the
header and no other byte, and n is the frame count of its camera file (SFF-898). Each other time
file is not usable. For a camera with a time file that is not usable, the reader reports
`time_file_unusable` with one reason:

| Reason | Cause |
|---|---|
| `missing` | No file has the name of the time file |
| `bad_header` | The magic, the version, the header length or the header does not parse |
| `dtype` | `descr` is not `'<f8'` |
| `shape` | `fortran_order` is not `False`, or the shape is not `(n,)` |
| `length` | The file does not hold exactly n values after the header, or n is not the frame count |

Value k of a usable time file is the time of frame k of the camera, in nanoseconds of
`time.perf_counter_ns()` on the recording machine. The reader rounds each finite value to the
nearest integer, and a half rounds up. A value that is not finite (NaN or an infinity), a value
below 0 and a value of 2^63 or more are frames with no time. A repeated value is a duplicated frame.
The reader keeps it as a frame.

**Draft SFF-898** (reader) This requirement belongs to section 21. A reader makes the frame table of each
camera file from the MP4 index of the file (`moov`). It reads 64-bit box sizes. It uses the first
track whose `hdlr` handler type is `vide`. When the file has two or more video tracks, it reports
`extra_tracks`. Then:

- **A file that the reader cannot index.** The reader does not read the camera file, and it reports
  one code:
  - `no_index`: the file has no `moov` box. A v1 file that was cut before its end has no `moov`,
    because the v1 writer writes `moov` last.
  - `index_damaged`: a box size goes past the end of its parent box or of the file; a box of the
    index is shorter than its entries need; `stts`, `stsz` and `stsc` with `stco` or `co64` do not
    give the same number of samples; or the `mdhd` or `mvhd` time scale is 0.
  - `no_video_track`: the file has no track whose `hdlr` handler type is `vide`.
- **Samples.** For each sample of the track, the DTS comes from `stts`, and the CTS is the DTS plus
  the composition offset of `ctts` (0 when the file has no `ctts`). The key flag comes from `stss`.
  Each sample is a key sample when the track has no `stss`. The byte offset comes from `stsc` with
  `stco` or `co64`, and the size from `stsz`.
- **The edit list.** The reader accepts a track with no `elst`, and a track whose `elst` holds zero
  or more empty edits (media time −1) and then one edit with a media time of 0 or more, a media rate
  of 1 and a segment duration above 0. It does not read a camera file with each other edit list, and
  it reports `edit_list_not_supported`. M is the media time of the non-empty edit, in track units.
  t_m is the `mdhd` time scale, and t_v the `mvhd` time scale. d is the segment duration of the
  non-empty edit, in movie units, and D = d × t_m / t_v is that duration in track units, as a
  rational number. The edit keeps each sample with M ≤ CTS < M + D. A reader compares exactly, for
  example as CTS × t_v < M × t_v + d × t_m. S is the sum of the segment durations of the empty
  edits, in movie units, and E = ⌊(S × t_m + ⌊t_v / 2⌋) / t_v⌋ is that sum in track units. With no
  `elst`, M = 0, E = 0, and the edit keeps each sample.
- **The sample list** holds each sample of the track, in decode order, with its DTS, its CTS, its
  key flag, its byte offset and its size. A sample that the edit does not keep stays in the sample
  list, because a kept frame can need it as a reference.
- **The frame table** holds each sample that the edit keeps, in the order of the CTS. Samples with
  an equal CTS are in decode order. Frame k is entry k of the frame table, from 0. Each entry holds
  the frame time stamp CTS − M + E (in track units), the position of the sample in the sample list,
  its key flag, its byte offset and its size.
- **The frame count** n_c of camera c is the number of entries, from frame 0, before the first entry
  whose bytes are not all inside the file. It is not the duration multiplied by the frame rate. It
  can be 0.

**Draft SFF-899** (reader) This requirement belongs to section 21. The frame table is the index of the
camera file. When a reader decodes a camera file through a demuxer that keeps its own index of the
file (for example the MP4 demuxer of FFmpeg), it compares that index with the frame table when it
opens the file. It uses the entries of the index for the video track, not the packets that the
demuxer reads. It leaves out each entry that the demuxer marks to discard (in FFmpeg, the flag
`AVINDEX_DISCARD_FRAME` of the index entry, which becomes `AV_PKT_FLAG_DISCARD` on the packet). e(k)
is the entry with the byte offset of frame k. For each frame k from 0 to n_c − 1:

- e(k) exists, it is not left out, and it has the size of frame k;
- the time stamp of e(k) minus the time stamp of e(0) equals the DTS of frame k minus the DTS of
  frame 0 (FFmpeg gives the DTS as the time stamp of a MP4 index entry, in track units).

The reader compares no entry for a frame from n_c on: a file cut short keeps its full index. When a
check fails, the reader does not read the camera file, and it reports `index_mismatch`.

**Draft SFF-900** (reader) This requirement belongs to section 21. The frame index is the truth.
Multi-camera frame k is frame k of each camera file that the reader reads. A reader never chooses
the frame of a camera by its time. K is the smallest frame count n_c of these camera files. A camera
file that the reader does not read (SFF-898, SFF-899) does not count for K. When the reader reads no
camera file, K = 0. The frames from K on are not multi-camera frames. When the frame counts differ,
the reader reports `frame_count_differs`, with the frame count of each camera. When K = 0, the
folder has no multi-camera frame and no time map, and the reader reports `no_frames`.

**Draft SFF-901** (reader) This requirement belongs to section 21. C is the set of the cameras that the
reader reads and that have a usable time file (SFF-897). v_c(k) is value k of the time file of
camera c, as an integer. When one or more values v_c(k) are finite, for a camera c of C and a k
below K, the times are:

- j is the first k with one or more finite v_c(k) in C. The base B is the smallest finite v_c(j) of
  C.
- U_k is the mean of the finite v_c(k) of C: with s their sum and m their number,
  U_k = ⌊(2 × s + m) / (2 × m)⌋ (the nearest integer; a half rounds up). A reader computes s with
  exact integers: a sum of values near 10^18 goes past a signed 64-bit integer. A JavaScript reader
  uses `BigInt` (SFF-706).
- T_k is the time of multi-camera frame k, in nanoseconds. T_k = 0 for k < j. T_j = U_j − B. For
  k > j, T_k = max(T_(k−1), U_k − B), and T_k = T_(k−1) when no v_c(k) of C is finite. Thus T_k never
  decreases.
- The camera time of camera c at frame k is v_c(k) − B for a camera of C with a finite v_c(k). It is
  absent for a camera of C with a v_c(k) that is not finite. It is T_k for a camera that is not in
  C, and the reader shows it as an estimate.

When no camera of C has a finite value below K, SFF-902 gives the times.

**Draft SFF-902** (reader) This requirement belongs to section 21. The header rate r_c of camera c is
(n_c − 1) × t_m / (p_last − p_first), as a rational number. p_first and p_last are the frame time
stamps of frame 0 and of frame n_c − 1 (SFF-898). This rule applies also when `stts` has two or more
entries. A camera with n_c < 2, or with p_last = p_first, has no header rate. r is the median of the
header rates of the cameras that the reader reads and that have a header rate. For an even number of
rates, r is the mean of the two middle rates. r is the recorded frame rate of the folder, also when
the folder has time files. When no camera of C (SFF-901) has a finite value below K:

- T_k is k × 10^9 / r, rounded to the nearest integer nanosecond, and a half rounds up.
- The camera time of each camera at frame k is T_k.
- The reader shows each such time as an estimate. (The skellycam player puts a `~` in front of
  it.)
- When no camera has a header rate, T_0 = 0, and T_k is not defined for k > 0. The reader then moves
  only frame by frame, and the folder has no recorded frame rate.

**Draft SFF-903** (reader) This requirement belongs to section 21. A reader that plays a v1 folder at the
recorded pace shows, at the play time t, the multi-camera frame k with the largest T_k ≤ t. A gap in
T_k (a stalled capture) plays as a gap of the same length: the reader shows the frame before the gap
until t reaches the next T_k. The reader does not close or shorten the gap.

## Appendix A. Golden folders

Gate 2 makes these folders. Each is committed with its SHA-256 sums and the script that made it,
from synthetic frames and pinned tools. Each case of a folder has two committed reader results of
SFF-885, with records: one for each scope of SFF-892. The section "Layout and cases" gives the
files. Each file of each case that holds `format_prerelease` has the value 1 (SFF-710), and so the
warning `prerelease` (SFF-891). The only exception is the case `prerelease_0` of G10. A file that
does not hold `format_prerelease` does not have the warning ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 2). Each capture info JSON of a golden
folder has `key_origin` and `device.os_device_id` (section 13). `key_origin` is `computed`, except
in the case `confirmed_key` of G1
([ADR-70VP](decisions/entries/70VP-camera-identity-forms-and-remembered-keys.md)).

| # | Golden folder | Sections |
|---|---|---|
| G1 | A capture-only take: 2 cameras of about 90 frames at a small size, one with a gap, both with a fit; audio of 3 s, mono, with a click every 500 ms. Each camera shows a flash at the time of each click. The take holds the capture info JSON, which skellycam writes at the take start (SFF-801) | 4 to 11, 13 |
| G2 | G1 with stereo audio | 9, 10 |
| G3 | A processed take: G1 plus the processing info JSON, a calibration TOML and a Parquet with 2D and 3D. Camera 1 has `display_rotation` 90, the input of SFT-749 ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 3). It holds no export: no file in `exports/` and no manifest item with the role `export`. The Parquet has a model with connection pairs and a model with no connection pair | 14 to 16 |
| G4 | A rotated camera: `display_rotation` 0, 90, 180 and 270, with coloured corner markers and the expected upright corner colours | 6, 8 |
| G5 | A crashed take: unfinished camera files and sidecars (a clean cut, a torn row of 37 bytes, a row with a wrong CRC), an unfinished audio file (a clean kill and a torn fragment), a `.tmp` manifest and the old manifest. Besides the device pairs, each case holds the manifest and the capture info JSON, and no Parquet and no TOML ([ADR-E68K](decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 6) | 12 |
| G6 | G5 after repair, and G5 with an interrupted repair. Besides the device pairs, each case holds the manifest and the capture info JSON, and no Parquet and no TOML | 12 |
| G7 | Two copies of G3: one with its manifest deleted, and one whose manifest has another `take_uuid` | 5, 20 |
| G8 | A renamed take folder: a copy of G3 in a folder with another name | 4, 16, 20 |
| G9 | Mismatch vectors: `take_uuid`, `camera_key`, a Parquet frame range, finished camera files with different numbers of rows, image dimensions, a rotation in `camera_configs`, an unresolved file name, a stale `parquet_sha256`, a calibration hash, a `calibration_uuid`, a Parquet with a wrong `recording_id` | 16, 20 |
| G10 | Version vectors: a higher `minor` with an unknown header key and an unknown column in a timing sidecar, and with an unknown member in a JSON file; an unknown `major` in a timing sidecar, and in a folder file; a journal with a higher `minor` and a record of an unknown type; `format_prerelease` 0 | 3 |
| G11 | Header and row error vectors: an integer with a leading zero; a `+` sign; a row integer of 2^53; a `nominal_rate` of 0/1 and of 2^20 + 1; a `display_rotation` of 45; a bad label; a missing header key; an unknown `clock` | 2, 7, 8, 11 |
| G12 | Fit vectors: two video segments; a source frame gap; a `period_ps` with a remainder; an audio fit with `period_fs`; a sidecar with no fit; two rows with equal fitted times; a row with the flag `encode_skip` | 8, 11 |
| G13 | A realtime take in the state after the fold and before the verified delete of the journal: a complete small take (2 camera files, their timing sidecars, a manifest and both info JSONs) that also holds a realtime journal (good records, a record with a wrong CRC, a 4 KiB zero hole, a torn tail) and the Parquet run of its fold | 5 to 8, 13, 14, 16, 17 |
| G14 | A calibration take and a motion-capture take that holds a copy of its TOML; a library TOML outside a take. The calibration take holds the processing info JSON and a Parquet with one run: the `TIMESTAMPS` rows and the ChArUco `OVERLAY_2D` rows (SFF-836) | 14 to 16 |
| G15 | Legacy folders: one v1 folder of each era signal; a v1 folder whose signals are in two chains; a v1 folder with no era signal; a v0.0.x folder; a v0.1.0 folder; a folder of MP4 files only (the family `unknown`) | 21 |
| G16 | Files with code: a pickle (`.pkl`) in the take folder; an NPY with an object array that the manifest lists | 22 |
| G17 | (provisional) A skellysync folder | 19 |
| G18 | Missing frames: a finished take of 3 cameras with no audio. Camera 0 has a frame with a capture error: a `missing` row with its times and a placeholder. Camera 1 stops during the take: `missing` rows with no times and placeholders, and the warning `camera_dead`. The process of camera 2 hangs in the write of block 8 and ends: a short file that the program completed (SFF-894), with `missing` rows with no block, a `# repair` line, no fit line, and the warnings `camera_dead` and `camera_file_short`. The case `no_block` has 2 cameras: row 0 of camera 0 is a `missing` row with its times, and the process of camera 1 ends before its first block, so its camera file holds no Cluster ([ADR-6AT7](decisions/entries/6AT7-format-changes-f1-to-f10-missing-frames-and-short-files.md); the case `no_block`: [ADR-76NN](decisions/entries/76NN-details-for-the-format-changes-f1-to-f10.md) item 13) | 5, 6, 8, 11, 12 |

### Layout and cases

The layout is from [ADR-0JVZ](decisions/entries/0JVZ-spec-v2-details-part-9.md) item 22. A case
is one folder `recording-files/golden/G<NN>/<case>/`, with two digits in `<NN>`: a take folder or a legacy folder.
A case name has only `a` to `z`, `0` to `9` and `_`. It is not the `<rec>` of the take. The two
results are beside the case folder: `<case>.full.json` (the scope `full`) and `<case>.player.json`
(the scope `player`). `recording-files/golden/G<NN>/SHA256SUMS` lists each file. The cases are:

- G1 to G4, G12, G13 and G16: `take`. G4 has four cameras. G12 has four cameras and audio with a
  fit: camera 0 has two segments and a source frame gap, camera 1 a `period_ps` with a remainder,
  camera 2 no fit, and camera 3 two equal fitted times and an `encode_skip` row. G12 also holds the
  Parquet of the vector of SFT-748 (the two rows with equal fitted times) as committed bytes
  ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 5).
- G1 also has `confirmed_key`: a copy of `take` in which camera 1 has `key_origin`
  `confirmed_by_user` and a `camera_key` that is not the hash of the port form of its
  `device.port_path` (SFF-752). Its `camera_label` and its file names come from that key. A test
  that names G1 with no case uses `take`.
- G5: `audio_clean_kill` and `audio_torn_fragment`. Each has three cameras (0: a clean cut; 1: a
  torn row of 37 bytes; 2: a row with a wrong CRC), the `.tmp` manifest and the old manifest.
- G6: `repaired` and `interrupted_repair`, from `audio_torn_fragment`. Each sidecar of
  `interrupted_repair` is `unfinished`, with `fit` false and `missing_fit` (SFF-798).
- G18: `take` and `no_block`.
- G7: `no_manifest` and `other_take_manifest`. `other_take_manifest` has `manifest` `invalid`, the
  warning `manifest_missing`, the manifest in `other_files` and `orphan_file` (SFF-867).
- G8: `renamed`.
- G9: `take_uuid`, `camera_key`, `frame_range`, `row_counts`, `dimensions`, `rotation_in_configs`,
  `unresolved_file`, `stale_parquet_sha256`, `calibration_hash`, `calibration_uuid` and
  `recording_id`.
- G10: `higher_minor`, `unknown_major_sidecar`, `unknown_major_folder_file`,
  `higher_minor_journal` and `prerelease_0`. `higher_minor` is G3 with `2.1` in each version field.
  It has `x_future` as the last header key and as a column before `crc32` in each sidecar, and as a
  member of the manifest and of the info JSONs. It also has an unknown key in `[metadata]` and in
  one camera table of the TOML, and the flag bit 7 (128) in one row of one video sidecar.
  `unknown_major_sidecar` is G1 with `3.0` in one video sidecar. `unknown_major_folder_file` is G1
  with `3.0` in the capture info JSON. `higher_minor_journal` is a copy of G13 whose journal header
  has `2.1` and whose journal has one good record of the unknown type 200. That record counts in
  `records`. `prerelease_0` is a copy of G1 in which each file has `format_prerelease` 0. It has no
  warning `prerelease`.
- G11, each a copy of G1 with one changed video sidecar: `leading_zero`, `plus_sign`,
  `row_integer_2_53`, `rate_0_1`, `rate_2_20_plus_1`, `rotation_45`, `bad_label`, `missing_key` and
  `unknown_clock`.
- G14: `calibration_take` and `mocap_take`, and the folder `library/`, which is not a case.
- G15: `v1a`, `v1b_v1d`, `v1b_v1c`, `v1e_v1h`, `v1f_v1h`, `v1g_v1h`, `v1h`, `v1h_prime`, `v1i`,
  `two_chains`, `no_signal`, `v0_0_x`, `v0_1_0` and `mp4_only`. The case `v1i` has
  `tracking_parameters_model` and no `run_reprojection_error_filtering` (SFF-878).

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
- The audio file plays in standard players. Exact sync is judged in the skellycam player
  ([ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md) item 1).
- VLC ignores the Opus pre-skip in MP4 and plays the audio about 6.5 ms late. This is accepted.
- The player draws the frame label from the fields of the frame. The take holds no overlay, and
  `.skov` is not part of the format (SFF-737, [ADR-2C9V](../decisions/entries/2C9V-whole-take-folder-scope-and-package.md) item 7).
- Lichtblick is not a viewer of this format
  ([ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md) item 12).
