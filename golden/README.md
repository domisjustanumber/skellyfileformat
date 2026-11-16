# Golden folders

This folder holds the golden folders of [SPEC.md Appendix A](../spec/SPEC.md#appendix-a-golden-folders).
A tool makes each file from synthetic input. No file holds data of a person or of a real device.
The committed bytes are the reference
([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 10).
A change to a golden file needs a decision entry ([AGENTS.md section 4](../AGENTS.md#4-project-rules)).

Only G1 exists. It is the worked example for the other folders. The user reviewed it on 2026-11-16
and accepted its conventions for the other folders ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md), ADR-G21H item 5).

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
  (`cameras[].flash_positions`). SFT-723 and SFT-729 need these facts.
- `.gitattributes` stops line-end conversion in this folder.

## How to make and check the files

The reference platform is Windows x86-64 with Python 3.13.13 and the dependency group `golden` of
`pyproject.toml`: av 19.0.2 (FFmpeg 9.0.2, libopus 1.6.1) and pillow 13.0.0. On another platform,
the encoders can give other bytes.

| Task | Command |
|---|---|
| Check the committed files against a new run | `uv run --group golden python tools/make_golden.py --check` |
| Write one folder again | `uv run --group golden python tools/make_golden.py --only G01` |
| Test the committed files | `uv run --group golden pytest tools/tests` |

`uv run pytest` also tests the sums and the text files. It skips the tests that decode the media
files, because the default environment has no PyAV.

The scripts are `tools/make_golden.py` (the command), `tools/goldgen/common.py` (the shared code)
and `tools/goldgen/g01.py` (the input of G1).

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

## Provisional parts

- [G01_CHOICES.md](G01_CHOICES.md) lists each value of G1 that the spec does not give. The user
  accepted the list as the conventions of the golden folders ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 5). The other golden
  folders copy them.
- Items 13, 14, 15 and 24 of that list can be rules of the format. The user must decide
  ([open-work.md](../decisions/open-work.md)).
- `byte_offset` and `byte_size` (SFF-757), `port_path` and `os_device_id` (SFF-752) and
  `audio_latency_ns` (SFF-771) are provisional in the spec.
