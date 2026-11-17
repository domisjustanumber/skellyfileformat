# Interface notes: the capture tests (SFT-700 to SFT-734)

These notes belong to the test files `test_s02_03_conventions.py`, `test_s04_05_folder_manifest.py`,
`test_s06_camera.py`, `test_s07_10_sidecars_audio.py`, `test_s11_timing.py` and
`test_s12_crash_repair.py`, and to `checks_capture.py` and `conftest.py`. They record what the tests
assume of the future Python package and of the JavaScript reader. `INTERFACE_NOTES_folder.md` holds
the same for SFT-735 to SFT-770.
The status of each choice is: proposed. The user did not review this file.

[ADR-G21H](../../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) fixes only the
names and the main arguments of the public interface. The column "Fixed by G21H" shows which part of
each row it fixes. Each other part is "assumed by the tests, not decided".

## 1. Names that the tests call

The tests get the package from the fixtures `reader` and `writer` of `conftest.py`. Both fixtures give
the top-level module `skellyfileformat`. The child process of SFT-730 also imports that module, so
`TakeWriter` and `repair_take` must be attributes of it.

| Name | Signature and shape | Fixed by G21H | Test |
|---|---|---|---|
| `read_folder` | `read_folder(path, records=False, scope="full")`. `path` is a `pathlib.Path`. The tests pass `records` and `scope` as keywords. The tests never read the return value. They give it to `canonical_json`. | The name, `path`, `records` and the return value (the reader result of SPEC.md section 23). The `scope` argument is assumed by the tests, not decided. | SFT-701 to SFT-704, SFT-706, SFT-707, SFT-709, SFT-710, SFT-713, SFT-714, SFT-716 to SFT-719, SFT-725, SFT-727 to SFT-729, SFT-731 to SFT-734 |
| `canonical_json` | `canonical_json(result) -> bytes`: the RFC 8785 bytes, with no line end. The tests parse these bytes with `json.loads`. | The name and the argument. The return type `bytes` is assumed by the tests, not decided. | The same tests as `read_folder` |
| `js_reader` (fixture) | `js_reader(folder, records=False) -> bytes`: the standard output of `node js/bin/read-folder.mjs <folder> [--records]`. The test needs exit code 0. The output must be the `player` result. | The command and `<folder>`. The flag `--records`, and the rule that the command gives the scope `player`, are assumed by the tests, not decided. | SFT-702, SFT-703, SFT-727, SFT-729 |
| `TakeWriter` | `TakeWriter(folder, rec, cameras, audio, *, writer, trace=None, mode="capture")`. See section 2 for the arguments. The constructor returns after it writes the manifest (`state` `recording`) and the capture info JSON. | The name only. Each argument is assumed by the tests, not decided. | SFT-700, SFT-703, SFT-705, SFT-708, SFT-711, SFT-712, SFT-715, SFT-717, SFT-720, SFT-722, SFT-725, SFT-726, SFT-730 |
| `TakeWriter.take_start_host_ns` | An `int`: the take start on the host clock, in ns. The tests read it after the constructor returns. | Assumed by the tests, not decided | SFT-708, SFT-712, SFT-717, SFT-722 |
| `TakeWriter.write_frame` | `write_frame(index, data, host_ns, *, source_frame_number, sample_ns=None)`. `index` is the `group_position` of the camera. `data` is a `bytes` object: a JPEG, or a raw YUYV frame when the camera config has `capture_format` `YUYV`. `host_ns` is an absolute host time (the take start plus the row time). `sample_ns` is absolute too, or `None`. `source_frame_number` is an `int` or `None`. | The name only | SFT-700, SFT-708, SFT-711, SFT-712, SFT-717, SFT-722 |
| `TakeWriter.write_audio` | `write_audio(pcm, host_ns, *, adc_ns=None, dropped_before=0, overflow=False)`. `pcm` is interleaved 16-bit little-endian PCM at 48 kHz, with `min(device_channels, 2)` channels. `dropped_before` is the number of samples that the device dropped before this block. | The name only | SFT-700, SFT-708, SFT-720, SFT-722 |
| `TakeWriter.add_warning` | `add_warning(code, *, camera_key, detail)`. The manifest gets `{"code", "source": "skellycam", "camera_key", "detail"}`. | The name only | SFT-708 |
| `TakeWriter.close` | `close()`. It sets `state` `finished`, writes the summary and the `# end` lines, and adds the warning `camera_gap` for a camera with a gap. | The name only | All tests that record a take |
| `repair_take` | `repair_take(folder, *, writer, trace=None)`. `writer` is the writer string of the program that repairs. The tests do not read the return value. | The name only | SFT-730, SFT-733 |
| `release_check` | `release_check() -> dict`. The test reads the key `"opus_encoder"`. Its value must be `"libopus"`. | The name only | SFT-721 |
| `camera_details` | `camera_details(folder, name) -> dict`. `name` is the `name` of a `files` item. The keys that the tests read: `format_version` (text, for example `"2.0"`), `format_prerelease` (int), `writer` (text), `display_rotation` (int), `nominal_rate` (a pair of ints, `[num, den]`) and `strict_ns` (a list with one int for each usable frame: the strict player times of SFF-782). | The name only | SFT-703, SFT-709, SFT-713, SFT-718, SFT-728 |
| `frame_spans` | `frame_spans(folder, name, method=<default>) -> list` of `(offset, size)` pairs, one for each usable frame, in position order. The tests give `method` `"walk"` or `"csv"` in SFT-714 and no `method` in SFT-713. | The name only. `method` and its values are assumed by the tests, not decided. | SFT-713, SFT-714 |
| `read_frame` | `read_frame(folder, name, position) -> bytes`: the bytes of the block payload. The reader does not decode them. | The name only | SFT-713, SFT-714, SFT-718 |
| `position_at` | `position_at(folder, name, t_ns) -> int or None`: the position of the frame shown at the take time `t_ns` (SFF-783). `None` when `t_ns` is before the player time of position 0. | The name only | SFT-728 |
| `audio_details` | `audio_details(folder, name) -> dict`. The keys that the tests read: `format_version`, `format_prerelease`, `writer`, `pre_skip` (int), `fit_segments` (a list of dicts, each with `n0`, `t0_ns` and `period_fs`; an empty list when the reader computes no fit) and `usable_samples` (int, SFF-785). | The name only | SFT-703, SFT-723, SFT-729, SFT-732 |
| `sample_time_ns` | `sample_time_ns(folder, name, sample, microphone=False) -> int or None`: the take time of an audio sample. `None` when the reader has no fit, and when `sample` is at or after `usable_samples`. With `microphone=True`, the value is the fitted time minus `audio_latency_ns`. | The name only. `microphone` is assumed by the tests, not decided. | SFT-724, SFT-729 |

The tests use no `run_details`. The tests of the other file use it.

### Members of the reader result that the tests read

The members are those of SFF-885. The tests read them from the parsed canonical JSON.

- Result: `takes`, `folder_state`, `folder_warnings`, `other_files` (`name`, `state`, `reason`) and
  `legacy`.
- Take: `take_uuid`, `recording_name`, `state`, `manifest`, `warnings`, `files`, `folder_files` and `links`.
- Item of `files`: `name`, `kind`, `state`, `reason`, `camera_key`, `camera_label`, `rows`,
  `torn_bytes`, `fit`, `warnings` and `records`.
- Item of `records`: the tests read index 0 (the position), 2 (`arrival_ns`) and 4 (`player_ns`) for a
  camera. They read index 0, 1 and 4 (`block`, `first_sample` and `fitted_ns`) for audio.

## 2. Arguments of `TakeWriter`

| Argument | Shape that the tests give | Fixed by G21H |
|---|---|---|
| `folder` | A `pathlib.Path` that does not exist yet, or that holds one earlier take (SFT-705). | Assumed by the tests, not decided |
| `rec` | The text `"synthetic_take"`, or `"take_a"` and `"take_b"`. | Assumed by the tests, not decided |
| `cameras` | A list of dicts. A dict has `camera_key` (a text or `None`), `key_origin` (`"computed"`, `"confirmed_by_user"`, `"assigned"` or `None`), `user_name`, `device` (`model`, `os_name`, `vendor_id`, `product_id`, `serial`, `port_path`, `os_device_id`, `backend`, `os_index`), `requested` (`width`, `height`, `framerate`, `capture_format`, `exposure_mode`), `controls` (a dict of `{name: {"value", "auto"}}`), `exposure_step`, `nominal_rate` (text such as `"30/1"`) and `display_rotation` (int). The position of a dict in the list is its `group_position`. When `camera_key` is `None`, the writer computes the key from `device` (SFF-752). | Assumed by the tests, not decided |
| `audio` | `None`, or a dict with `device_name`, `host_api` and `device_channels`. | Assumed by the tests, not decided |
| `writer` | A keyword. The writer string, for example `"skellycam 2.0.0"`. | Assumed by the tests, not decided |
| `trace` | A keyword. A callable `trace(event, path)`. See section 3. | Assumed by the tests, not decided |
| `mode` | A keyword. `"conversion"` makes a converter run (SFT-705, SFT-717). The default is a capture. | Assumed by the tests, not decided |

The writer refuses with a `ValueError`. The constructor raises it for a nominal rate of `1001/1`
(SFT-711), for `capture_format` `H264` (SFT-712) and for a folder that holds a file of another take
(SFT-705). In the last case the test also asserts that no file changes, so the refusal comes before
the first write. The exception class is assumed by the tests, not decided.

The camera in SFT-717 (`encoder_failure`) sends a raw `YUYV` frame. An empty `bytes` object at one
position makes the JPEG encoder fail. The writer stores no frame for it. The next stored row has the
flag `encode_skip`. This way to force a failure is assumed by the tests, not decided.

## 3. The trace

`trace(event, path)` is called for the file system actions that the tests check. `event` and `path`
are text. `path` is relative to the take folder, with `/`. The tests use these events.

| Event | Path | Meaning | Test |
|---|---|---|---|
| `lock` and `unlock` | `.processing.lock` | The writer takes and releases the lock. The events come in pairs. | SFT-708, SFT-730, SFT-733 |
| `read` | `recording_manifest.json` or `<rec>_info.json` | The writer reads a whole file to change it. It must call this event after `lock` and before `unlock`. A writer that never reads a whole file calls no `read`. Assumed by the tests, not decided. | SFT-708, SFT-730, SFT-733 |
| `replace` | `recording_manifest.json` or `<rec>_info.json` | A whole file is replaced in one rename. A writer calls it for each whole-file write. A `replace` of a path that is not in the list of the test fails the test. | SFT-708, SFT-730, SFT-733 |
| `write` and `flush` | `synchronized_videos/<rec>.audio.m4a` | A write to the audio file, and the flush after it. Each `write` must have a `flush` as the next audio event. | SFT-720 |
| `fsync` | a live file | The writer forces a live file to disk. At least one such event must exist. | SFT-730 (provisional) |
| any event | `synchronized_videos/...` | `repair_take` calls the trace for its writes to media files and sidecars. At least one such event must exist for a media file and for a sidecar. All of them come before the `replace` of the manifest. Each event of a media file, other than `read` and `fsync`, comes before each such event of a sidecar: the repair cuts every media file before it changes a sidecar ([ADR-E68K](../../decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 3). A `replace` of a media path or a sidecar is allowed, and the lock check ignores it. | SFT-733 |

A write of a whole file with any other event (for example `write` of the manifest path) fails
`check_whole_writes_hold_lock`. The event names are assumed by the tests, not decided.

## 4. Other assumptions of the tests

- The names in `files` items are paths of the media file, for example `synchronized_videos/<name>.mkv`.
  The detail functions take the same text as `name`.
- The row of an audio sidecar is one row for each call of `write_audio` (SFT-722 reads the row index of
  the block with the overflow). The writer does not merge or split the blocks.
- The sidecar `sample_ns` of a frame is `sample_ns - take_start_host_ns`. An absent `sample_ns` gives an
  empty field.
- `record_take` of `checks_capture.py` is the writer run that most tests use. It writes 12 frames for
  each camera, with one lost source frame in camera 1 before position 5, and 25 audio blocks of 4,800
  samples. It calls an `after` function after each call (SFT-730).
- SFT-730 starts a child process with the interpreter of the test. The child imports `skellyfileformat`
  and `checks_capture` and prints one line after the take starts and after each write call. Then it blocks
  on one byte of standard input. The test sends one byte for each step before its kill point, and then
  kills the child, so each of the 50 kill points is exact. After each kill, the test calls `repair_take`
  on the killed folder (the next writer). A repair of a take with no frame must work. Assumed by the
  tests, not decided.
- SFT-717 accepts a `computed` key that is the hash of any of the forms 1, 2 and 3 of SFF-752 that
  the `device` values of the capture info JSON can build. The file records no reason when a writer
  does not use a serial
  ([ADR-E68K](../../decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 4).
- SFT-719 makes two inputs at test time: a copy of G1 (a finished pair) and a copy of G6 `repaired`
  (a repaired pair). In each, the sidecar of camera 0 gets one row more than its camera file has
  blocks. Each pair is `invalid` with `bad_metadata`
  ([ADR-W5AK](../../decisions/entries/W5AK-details-for-the-decisions-q83-to-q111.md) item 10).
- SFT-733 checks on G6 `interrupted_repair` that each media file has the bytes of G6 `repaired` and
  that each sidecar has the rows of G6 `repaired`: the repair stopped after the cuts
  ([ADR-E68K](../../decisions/entries/E68K-camera-match-repair-order-and-g5-g6-files.md) item 3).
- The Opus encoder, PyAV and Pillow come from the `conformance` dependency group. A test that needs
  PyAV or Pillow is skipped when it is missing.

## 5. Parts that the tests do not run

- A test with the mark `external` is skipped here: SFT-705 (the freemocap part), SFT-703 (the export
  inventory and the BVH metadata), SFT-708 (freemocap and the detection of two warnings), SFT-711
  (Blender), SFT-712 (capture hardware), SFT-730 (a kill of freemocap) and SFT-733 (the user question).
- A test with the mark `provisional` is skipped: SFT-714 (CSV offsets, DT5), SFT-717 (the bit `filled`),
  SFT-724 (audio latency), SFT-725 (Linux and macOS), SFT-730 (fsync) and SFT-733 (the repaired camera
  file, DT-R1).
- The tests of SFT-703 on G10, of SFT-706 on G08 and of SFT-710 on G07 need golden folders that are not
  built yet. Each such test is skipped until the folder exists.
