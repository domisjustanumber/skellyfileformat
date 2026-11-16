# Interface notes: the folder tests (SFT-735 to SFT-770)

These notes belong to the test files `test_s13_15_info_calibration.py` to `test_s23_result.py` and
to `checks_folder.py`. They record what the tests had to choose, what they could not assert, and
what does not agree. `INTERFACE_NOTES_capture.md` holds the same for SFT-700 to SFT-734.
The status of each choice is: proposed. The user did not review this file.

## 1. Signatures and return shapes that the tests chose

| Function | Signature and shape | Test |
|---|---|---|
| `read_folder` | `read_folder(path, records=False, scope="full")`. `path` is a `pathlib.Path`. The tests pass `records` and `scope` as keywords. | All reader tests |
| `canonical_json` | `canonical_json(result) -> bytes`: the RFC 8785 bytes, with no line end. The tests compare it with the bytes of `<case>.<scope>.json`. | SFT-768, SFT-769 |
| `js_reader` (fixture) | `js_reader(folder, records=False) -> bytes`: the standard output of `node js/bin/read-folder.mjs <folder> [--records]`. | SFT-768, SFT-769 |
| `run_details` | `run_details(folder) -> list[dict]`: one item for each run of the Parquet of the take, in order of `run_id`. Each item has `run_id` (int), `geometry` and `rows`. `geometry` is `"stored"` when the reader uses `camera_geometry` of the run, `"calibration"` when it uses the TOML, and `None` when the run has no camera geometry. `rows` is a list with one tuple for each Parquet row, in file order: `(timestamp_s, sensor_group, frame_number, source, reference_frame, channel, name, component, value, units)`. `value` is the Python float of the column that the `dtype` of the channel names, or `None`. `frame_number` is a Python int for an int32 file and for an int64 file. Two results compare with `==`. | SFT-747, SFT-754 |
| `TakeWriter` | The test uses the interface of `INTERFACE_NOTES_capture.md`: `TakeWriter(folder, rec, cameras, audio, writer=..., trace=...)`, `take_start_host_ns`, `write_frame(index, jpeg, host_ns, source_frame_number=...)`, `close()`, and the trace events `("lock" or "unlock", ".processing.lock")` and `("replace", <file name>)`. SFT-735 needs: the capture info JSON exists and is complete directly after the constructor returns, and the trace shows two `replace` events for it, each between a `lock` and an `unlock`. | SFT-735 |
| The result for `camera_key` 0 | `camera_key` of the `files` item is the text `"0"`. | SFT-763 |
| The capture info key for `camera_key` 0 | The key of the camera config is `0:<camera_label>`, and the other files hold `camera_key` `"0"` (the manifest, the TOML, the Parquet descriptor). | SFT-763 |

The tests use no other detail function: `camera_details`, `frame_spans`, `read_frame`,
`position_at`, `audio_details` and `sample_time_ns` are only in the tests of the other file.

Test inputs that a test makes ("G3 with X"), and the choices in them:

- A changed JSON file is written with an indent of 2 spaces and one LF (the convention of the golden
  folders). A changed TOML is written by `checks_folder.toml_text`.
- When a test changes the Parquet, it also writes the new `parquet_sha256` in the processing info
  JSON. When it changes the TOML, it also writes the new `sha256` in the manifest. So only the
  vector of the test differs from G3.
- SFT-747 and SFT-770 write the changed Parquet with pyarrow as one row group for each write call
  of pyarrow, not one row group for each channel. This breaks only a writer rule (SFF-823).
- SFT-754: "moved 10 mm" adds 10 to `translation[0]` of the camera with `index` 0. The rigid change
  is a rotation by the Rodrigues vector (0.1, −0.2, 0.3) and a shift of (100, −50, 25) mm. The
  `calibration_uuid` does not change.
- SFT-757: the cut record is `SKRJ`, a `length` of 2^20, the type 2 and 10 zero bytes, put before
  the last good record. The torn tail is the last good record without its last 5 bytes. The test
  copies have no end record.
- SFT-761 and SFT-762: the extra sidecar is a copy of the sidecar of camera 1 with `camera_key`
  `abcdef0123456789`, `camera_label` `abcdef` and `group_position` 2. The other take has the
  `take_uuid` `0000000000004000800000000000ffff`. The clock vector writes `linux_monotonic`.
- SFT-765: the four folders are copies of the case `v1a` of G15 with the folder name `old_session`.
  Each TOML that the test adds holds only `[cam_0]` with a zero `rotation`.
- SFT-767: the test adds its files to a copy of G16 with the role `export` and `sha256` null. It
  also adds `canary.pkl` and an NPZ member whose load creates a canary file, because the pickle of
  G16 is harmless (G16_CHOICES.md item 3). The test never loads them.
- SFT-768: the empty annotated video is `annotated_videos/<rec>.<label of camera 0>.annotated.mp4`,
  with the role `annotated_video`, the owner `freemocap` and the SHA-256 of zero bytes.
- SFT-770: the test changes the first model that has a joint. The copies are: `detector_type`
  deleted; `scale_reference_name` = 5; `skeleton.x_unknown` = 1; `child` of the first joint =
  `no_such_segment`; `handedness` of the first segment frame as `1.0` and the first `position`
  value of the first landmark as `0`.

Checks that are not in a Pass text but that the tests add, each on committed files and with no
implementation:

- `test_sft_768_committed_results` applies the form rules of SFT-768 to each committed
  `<case>.full.json` and `<case>.player.json`.
- `test_sft_769_committed_results` applies the `player` rules of SFT-769 to each committed pair.
- SFT-770 checks its own copies with the structure check of `checks_folder.py`, so that a copy has
  the fault that the test wants.

## 2. Pass sentences with no assertion, or with a weaker assertion

| Test | Sentence | Reason |
|---|---|---|
| SFT-736 | "each config is linked to the camera of its key" | The reader result holds no value of a camera config. The test asserts that the check `camera_key` is `ok` and that the result is the committed result of G3. |
| SFT-737 (golden part) | "after each write"; "The file is rewritten after the export" | G3 holds one state of the files and no export. The test checks the hash and the members of that state. |
| SFT-738 (golden part) | The triangulated point (X, Y, Z) → (−Y, X, Z) | It needs a triangulation of freemocap. The tolerance of "`world_orientation` is the transpose" is 1e-9 in each value: the test chose it. |
| SFT-739 (golden part) | The alignment; the kills | They need a run of freemocap. |
| SFT-740 | "The camera tables are linked by `camera_key`, in order of `index`" | The result does not show the order. The test puts the camera tables of G14 in the other order in the file and asserts that `camera_key` and `calibration` are `ok` and that the take has no `calibration_mismatch`. |
| SFT-740 | "ignores the second TOML" | The test asserts that `links` and `folder_files` are those of the committed result. It does not assert the place of the second TOML in the result (see section 3). |
| SFT-746 | "the codec is ZSTD at level 3" | A Parquet file does not hold the level. The test asserts the codec only. |
| SFT-746 | "the writer rules of each model and of its nested types" | The check does not have the rules of `SuperquadricContours` that need the compiled volume: "the x distance between the eyes fits in the volume", and the two rules of `nose`. The part does not give their formulas. |
| SFT-747 | "pyarrow reads every value bit-exactly" | pyarrow wrote the golden file, and the repository has no other reference of the values. The test asserts the pinned version and the number of rows, and uses the pyarrow values as the reference for the other readers. |
| SFT-749 | "G3 with a rotated camera (`display_rotation` 90)" | No camera of G3 has `display_rotation` 90 (section 3). The check runs on G3 as it is: each image reference has the size of the stored frames (PyAV), each 2D channel is in pixels, and `calibrated_world` has the Blender basis and mm. |
| SFT-751 (golden part) | The posthoc run, the repair, the manifest with `state` `recording` | They need a run of freemocap. |
| SFT-752 | "no counts" | The test asserts that the take has only the members of SFF-885 and that the result holds no text of the note. The comparison with the committed result is in SFT-768. |
| SFT-753 | "No other file holds them" | No rule tells how to find ChArUco corners in an unknown file. No assertion. |
| SFT-756 (golden part) | "Each result kind of SFF-842 that the session made is in the journal"; "Missing values are NaN"; `data_records` "the number of data records that the writer wrote" | A golden file does not show what a session made or what the writer wrote. The test asserts that no value is infinite, and that an end record, when G13 has one, has the two members. |
| SFT-757 | "the reader skips the record with a wrong CRC, finds the next record after the zero hole and stops at the torn tail" | The test asserts the three counts: they equal the committed result and the scan of SFF-843 in `checks_folder.scan_journal`. |
| SFT-757 | The state of the copy with the cut record and of the copy that ends with 2 bytes of `magic` | The Pass text gives only a count for these two copies. The test asserts the counts. |
| SFT-758 (golden part) | "The count and the digest of the check equal the values that the test computes from the G13 journal" | No committed file holds the two values. The test computes them from the journal and from the rows of the realtime run of the Parquet, and asserts that they are equal. |
| SFT-762 | "the values of `group_position` 0 are used" | The result holds no `clock`. The test asserts only `take_fact_mismatch`. |
| SFT-762 | "each take is reported" (G9) | The test asserts that `takes` has one item for each `take_uuid` of the timing sidecars of the case. |
| SFT-764 | The folder with no era signal and the folder with two chains: the exact range | The test compares `legacy` with the committed result and asserts `ambiguous` true. |
| SFT-766 | The privacy list of G7 and of "G1 with its camera pairs deleted" | The list is a writer rule. The test checks the manifest of G3. For the two other inputs it checks only the reader member. |
| SFT-768 | "The states follow the order of SFF-886" | One result cannot show an order of two states. The test asserts that each state and each code is in its list. The comparison with the committed results checks the order. |
| SFT-769 | "The checks `take_uuid`, `camera_key`, `rotation` and `files` have only the parts that need no TOML, Parquet or journal" | The result does not show the parts. The comparison with the committed `player` result checks them. The test leaves `links` out of the comparison of the two scopes. |
| SFT-741, SFT-742 | "A `<rec>.blend1` is not in the reader result"; "A `.partial.mp4` file is not in the reader result" | Each test is external as a whole and has no golden part, so no test of this repository runs these two reader sentences (SFF-849, SFF-852). |

Parts that were not run at gate 2:

- The Node script of hyparquet in `checks_folder.HYPARQUET`: the packages are not installed. The
  test looks for them in `js/node_modules`.
- The parts with polars and DuckDB: the packages are not in a dependency group.
- Each check on G07, G09, G13, G14 and G17, when the folder was not built: `fold_faults`,
  `journal_faults`, `journal_digest`, `parquet_digest`, `charuco_faults`, the journal copies of
  SFT-757 and the TOML checks. The scan of SFF-843 and the journal copies were run on a small
  journal that a scratch script made.

## 3. Contradictions and gaps

1. **SFT-749 and Appendix A.** SFT-749 names "G3 with a rotated camera (`display_rotation` 90)".
   Appendix A and G3 give no camera of G3 a rotation. Only G4 has rotated cameras, and G4 has no
   Parquet.
2. **`records` of a refused file.** SFF-885 says that an `invalid` item has `rows`, `torn_bytes`
   and `fit` null. It does not give `records`. The committed results of G11 have `records` null.
   `result_faults` accepts null and an array.
3. **SFT-740, the second TOML.** A TOML with `[metadata].calibration_uuid` is a file of this format
   (SFF-875), and it holds no `take_uuid`. No rule gives its place in the result when a take
   exists and the manifest does not name it: `other_files` as `not_in_format`, or as `invalid`
   with `take_fact_mismatch` and `orphan_file` (SFF-889).
4. **SFT-767 and G16.** The Pass text says "a canary file is not created". The pickle of G16 runs
   no code (G16_CHOICES.md item 3), so G16 alone cannot show it. The test adds its own files.
5. **SFT-751, the stages of a realtime run.** SFF-834 gives `coverage` "for one sensor group and
   stage". It does not say which stages of a realtime run have a stage provenance. `fold_faults`
   checks each stage that the run has, also a stage with no journal channel (for example `timing`),
   for which the rule gives `frames_processed` 0.
6. **SFT-761, the sidecar "of the take with no media file".** The text does not say if the sidecar
   is a third sidecar or the sidecar of a deleted camera file. The test adds a third sidecar,
   because the Pass text says "It gives no `extra_files`".
7. **SFT-763, "G3 with one `camera_key` 0".** No golden case has this vector. The test changes six
   files of a copy of G3 (section 1). The form of key 0 in the manifest, the TOML and the
   descriptor is a choice: the spec gives it only for the sidecar (`0`) and the capture info JSON
   (`0:<camera_label>`).
8. **SFT-757, `torn_bytes` with no torn tail.** By SFF-843, a file whose last good record ends by
   chance with the byte `S` has `torn_bytes` 1. `scan_journal` follows the text.
9. **SFT-744, SFT-752 and the other tests with no "Python and JS".** These tests run only the
   Python reader with the scope `full`, as "How to read a test" says. A rule such as SFF-860 also
   applies to the scope `player`, but only SFT-768 and SFT-769 run that scope.
