# Golden folders

This folder holds the golden folders of [SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders).
A tool makes each file from synthetic input. No file holds data of a person or of a real device.
The committed bytes are the reference
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 10).
A change to a golden file needs a decision entry ([AGENTS.md section 4](../AGENTS.md#4-project-rules)).

G1 to G16 exist. G17 does not exist: it waits for the skellysync decisions. G1 is the worked
example for the other folders. The user reviewed G1 on 2026-11-16 and accepted its conventions for
the other folders ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md), ADR-G21H item 5).
Each file `G<NN>…_CHOICES.md` and `CAPTURE_VECTORS_CHOICES.md` lists the choices of its folders
that the spec does not give. On 2026-11-16, the user also accepted the items of the other lists as
conventions of the golden folders. They are not rules of the format
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 7). A decision of
the same day replaced some items: each list gives the decided rule for them. Each list marks the
items that are still open. No reader exists, so each expected result comes from the spec text only.

[ADR-W389](../decisions/entries/W389-format-rules-from-the-golden-conventions.md) decided items 13
(JSON white space and escapes), 14, 15 and 24 of [G01_CHOICES.md](G01_CHOICES.md). Items 14, 15 and
24 are rules of the format (section 13, SFF-881, SFF-885). The white space of item 13 (the indent of
2 spaces and the one LF at the end of a JSON file) is a convention of the golden folders only: a
reader accepts each JSON white space (SFF-702, W389 item 5). The rest of item 13 is a convention of
the golden folders, as each other item.

## Layout

```
golden/
  G01_CHOICES.md               the choices of G1 that the spec does not give, accepted as conventions
  G01/
    SHA256SUMS                 the SHA-256 sum of each other file below G01/
    take/                      a case: one take folder
    take.full.json             the expected reader result of the case, scope `full`, with `records`
    take.player.json           the expected reader result of the case, scope `player`, with `records`
    take.truth.json            facts of the generator that the reader result does not hold
    confirmed_key/             a second case, with the same three files beside it
```

- A case folder is the input of a reader. The files beside it are not part of the take.
- `SHA256SUMS` has one line for each file: the sum, two spaces and the path relative to `G<NN>/`.
  The lines are in order of the bytes of the path. The file does not list itself.
- Each result file is the canonical JSON of SFF-885 (RFC 8785): one line, with no line end after it.
- `<case>.truth.json` is canonical JSON. For G1 it holds the first sample of each click
  (`audio.click_samples`) and the position of each flash frame of each camera
  (`cameras[].flash_positions`). SFT-723 and SFT-729 need these facts. The truth file of G3 (and
  its copy in G8) also has the member `parquet`: `name` (the file name of the Parquet), `rows` (the
  number of rows) and `values_sha256` (the digest of the next section). SFT-747 needs it.
- `golden/G12/equal_fitted_times.parquet` is beside the case `take` of G12, so it is not a file of
  the take. It holds 12 rows: the `TIMESTAMPS` channel `capture` of camera 3, whose rows 6 and 7
  have equal fitted times. Its descriptor holds only `runs.0.sensor_groups`. It is not a full
  descriptor. SFT-748 reads the file
  ([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 5).
- `.gitattributes` stops line-end conversion in this folder.

## The digest of the Parquet values

`values_sha256` is the SHA-256 of a byte string, as 64 lowercase hexadecimal characters. The
generator computes it from the values that it gives to the Parquet writer, not from the file. A
reader computes it from the values that it reads. The byte string has, for each row of the file in
file order (the row groups in order, then the rows in order), for each of the 12 columns in the
order of the table of SPEC.md section 16, these bytes:

- a null: the byte `00`;
- another value: the byte `01`, then the value:
  - `timestamp_s` and `value_f64`: the 8 bytes of the IEEE 754 binary64 value, little-endian;
  - `value`: the 4 bytes of the IEEE 754 binary32 value, little-endian;
  - `frame_number` and `run_id`: the integer as 8 bytes, two's complement, little-endian (so a
    copy with int64 columns has the same digest);
  - each text column: the number of bytes of the UTF-8 text as 4 bytes, unsigned, little-endian,
    then the UTF-8 bytes.

The bytes of a float are the bytes of the value as the file stores it, so `-0.0` and `0.0` differ.
`tools/tests/test_g03.py` checks the digest with bytes that it writes by hand.

## How to make and check the files

The reference platform is Windows x86-64 with Python 3.13.13 and the dependency group `golden` of
`pyproject.toml`: av 19.0.2 (FFmpeg 9.0.2, libopus 1.6.1), pillow 13.0.0, numpy 2.4.6 and pyarrow 26.0.0. On another platform,
the encoders can give other bytes.

| Task | Command |
|---|---|
| Check the committed files against a new run | `uv run --group golden python tools/make_golden.py --check` |
| Write one folder again | `uv run --group golden python tools/make_golden.py --only G01` |
| Test the committed files | `uv run --group golden pytest tools/tests` |

`uv run pytest` also tests the sums and the text files. It skips the tests that decode the media
files, because the default environment has no PyAV.

The scripts are `tools/make_golden.py` (the command), `tools/goldgen/common.py`,
`folder_common.py` and `capture_cases.py` (the shared code) and one module `tools/goldgen/g<NN>.py`
for each folder.

## G1: what the take holds

- Two cameras with 90 frames each of 64 × 48 pixels, at the nominal rate 30/1. Camera 0 has a
  serial number, a user name and a driver time in each row. Camera 1 has no serial number, no user
  name and no driver time. Camera 1 lost one source frame before position 40, so that row has the
  flag `gap`, and the camera file has the file warning `gap`.
- Audio of 3 s (144,000 samples, mono) in 30 blocks of 4,800 samples.
- Six events, at 100 ms after the take start and then each 500 ms. At each event, the audio has a
  click of 1 ms, and the frame of each camera that is nearest to the event is white. The fitted
  time of each flash frame is less than 1 ms from the fitted time of the click.
- The fit of each sidecar is the exact line that made the rows. The arrival times have a
  synthetic delay.
- The case `confirmed_key` is a copy of `take`. Camera 1 has `key_origin` `confirmed_by_user` and
  the key of another port.

## G1: the expected reader result

The generator does not read the files to make the result, because no reader exists. It writes the
result from its input and from the rules of SPEC.md section 23. Each member has its requirement:

| Member | Value in G1 | Requirement |
|---|---|---|
| `result_version` | 2 | SFF-885 |
| `folder_state` | `ok`: the folder has one take | SFF-888 |
| `folder_warnings` | `[]`: one take, no `.tmp` file, no file alone | SFF-866, SFF-790, SFF-865 |
| `takes` | one item | SFF-866, SFF-890 |
| `takes[].take_uuid`, `recording_name` | the values of the manifest | SFF-866, SFF-868 |
| `takes[].state` | `complete`: 2 camera files for `group_size` 2, 1 audio file for `audio_count` 1 | SFF-869 |
| `takes[].manifest` | `present` | SFF-867 |
| `takes[].warnings` | `[]`. The manifest warning `camera_gap` is not a warning of the reader. The file warning `gap` shows the gap | SFF-887 |
| `takes[].may_contain_private_data` | true: the `privacy` list has items | SFF-883 |
| `files` (the order) | camera 0, camera 1, audio | SFF-890 |
| `files[].name`, `kind` | the path of the media file; `camera` or `audio` | SFF-885 |
| `files[].state`, `reason` | `finished`, null: the last line of each sidecar is `# end` | SFF-886, SFF-747 |
| `files[].camera_key`, `camera_label` | the header values; null for audio | SFF-885 |
| `files[].rows` | 90, 90 and 30 | SFF-885, SFF-746 |
| `files[].torn_bytes` | 0 | SFF-791 |
| `files[].fit` | true: the sidecar is finished and has fit lines | SFF-885, SFF-747 |
| `files[].warnings` | `["prerelease"]` for camera 0 and for audio. `["gap","prerelease"]` for camera 1: a row has the flag `gap` ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 1) | SFF-887, SFF-890, SFF-891, SFF-710 |
| `files[].records` (camera) | `[position, source_frame_number, arrival_ns, sample_ns, player_ns]`. `sample_ns` is null for camera 1 | SFF-885 |
| `player_ns` | the fitted time, with d from the source frame numbers. It is not the strict time | SFF-777, SFF-781, SFF-782 |
| `files[].records` (audio) | `[block, first_sample, n_samples, host_ns, fitted_ns]` | SFF-885 |
| `fitted_ns` | the fitted time of `first_sample`, from the fit lines | SFF-779, SFF-784 |
| `folder_files` | one item: the capture info JSON, with the `role` of the manifest, `present`, `reason` null | SFF-885, SFF-889 |
| `folder_files[].warnings` | `["prerelease"]`: the capture info JSON has `format_prerelease` 1. The manifest is not an item, so the result shows nothing for it | SFF-891 |
| `links` (the order, `detail` null) | the eight checks | SFF-885, SFF-890, SFF-872 |
| `links`: `take_uuid` | `ok`: the manifest, 3 sidecars and the capture info JSON | SFF-872 |
| `links`: `camera_key` | `ok`: the manifest with the video sidecars and with the capture info JSON | SFF-872 |
| `links`: `frames` | `full`: `ok`, from the row counts of the 2 finished camera files. `player`: `not_checked` | SFF-872, SFF-892 |
| `links`: `dimensions`, `hashes`, `calibration` | `not_checked`: the take has no Parquet and no TOML | SFF-872 |
| `links`: `rotation` | `ok`: the capture info JSON has no rotation, and the summary agrees with the sidecars | SFF-872 |
| `links`: `files` | `ok`: each path of the manifest exists | SFF-872 |
| `other_files` | `[]` | SFF-885, SFF-889 |
| `legacy` | null | SFF-885 |

The `player` result of each case of G1 differs from the `full` result only in the check `frames`
(SFF-892). The result of `confirmed_key` differs from the result of `take` only in `camera_key`,
`camera_label` and `name` of camera 1.

## G3 and its copies

G3 is the take of G1 with a calibration TOML, a tracking Parquet and the processing info JSON
([G03_CHOICES.md](G03_CHOICES.md)). Camera 1 of G3 has `display_rotation` 90: the input of SFT-749
([ADR-2MQE](../decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 3). So the
sidecar of camera 1 and the manifest summary differ from G1. The stored frames, the TOML `size`,
the image reference of the Parquet and the 2D values stay in stored-JPEG pixels (SFF-829). G7, G8,
G9 and the case `higher_minor` of G10 are copies of G3, so they also have the rotated camera.

## Provisional parts

- [G01_CHOICES.md](G01_CHOICES.md) lists each value of G1 that the spec does not give. The user
  accepted the list as the conventions of the golden folders ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 5). The other golden
  folders copy them.
- G5 and G6 hold a stand-in for a killed camera file: a copy of the muxer output before `close()`
  ([CAPTURE_VECTORS_CHOICES.md](CAPTURE_VECTORS_CHOICES.md) item 23). They are provisional until
  desk tests DT-R1 and DT5
  ([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 6).
- `byte_offset` and `byte_size` (SFF-757), `port_path` and `os_device_id` (SFF-752) and
  `audio_latency_ns` (SFF-771) are provisional in the spec.
