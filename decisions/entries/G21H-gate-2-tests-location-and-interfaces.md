# G21H — Gate 2: where the runnable tests live and what they call

**Status:** superseded by [YBT1](YBT1-spec-only-test-adapter-and-labels.md), 2026-11-17 (commit to main; was absorbed, 2026-11-17 (commit to main; was accepted, 2026-11-16 (user; review of the spec after gate 1))).

## Decision

1. **Place.** The runnable conformance tests are in `tests/conformance/`, outside the default pytest
   run. `uv run pytest` stays green. The failing run is
   `uv run --group conformance pytest tests/conformance`.
2. **Interfaces.** The tests call:
   - the Python reader: `read_folder(path, records=False, scope="full")`, which returns the reader result of
     SPEC.md section 23, and `canonical_json(result)`;
   - the JavaScript reader: the command `node js/bin/read-folder.mjs <folder> [--records]` (the
     `scope` argument and the switch: [ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) item 21, corrected on 2026-11-17);
   - the Python writer: `TakeWriter` (with `write_frame`, `write_audio`, `add_warning` and `close`),
     `repair_take` and `release_check`.
3. **Detail functions.** A fact that a test needs and that the reader result does not hold comes
   from a detail function of the Python reader: `camera_details`, `frame_spans`, `read_frame`,
   `position_at`, `audio_details`, `sample_time_ns` or `run_details`. The result gets no member for
   it. The journal counts are the exception
   ([ADR-E45D](E45D-spec-draft-v2-corrections-after-review.md) item 1).
4. **Writer scope.** The package writer writes only what a capture or a conversion needs: the camera
   files, the audio file, the timing sidecars, the manifest, the capture info JSON and a repair.
   freemocap writes the Parquet, the TOML, the journal, the exports and the processing info JSON.
   This repository tests those files by checks on golden folders.
5. **G1 first.** The expected reader result of G1 is written first, as a worked example. The user
   approves it. The other golden results then use its conventions.
6. **G5 and G6.** They are built now, with a stand-in for the killed camera file: a copy taken
   before the muxer closes. They are provisional until the desk tests DT-R1 and DT5. A later change
   of a golden file needs a decision entry.
7. **SFT-713.** The test builds its unusual camera file at run time. Appendix A does not change.
8. **No decoding.** The Python reader does not decode pixels or audio samples. It returns the
   stored bytes and the timing. The tests decode with PyAV.
9. **Repository files.** `.gitattributes` stops line-end conversion in `golden/`. The golden
   generator is a tool in `tools/`, with tests. `AGENTS.md` gains the `golden/` and `tests/` rows
   and the command of the failing run.
10. **Byte identity.** A re-run gives byte-identical golden files only on the reference platform:
    Windows x86-64 with the pinned tools. The committed bytes are the reference.

## Reason

- Items 1 and 9: AGENTS.md section 3 says that `uv run pytest` must pass. The gate 2 tests fail
  until the implementation exists.
- Items 2 and 3: fixed names let the tests exist before the code. A small result keeps the Python
  and JavaScript results comparable.
- Item 4: freemocap owns its files ([ADR-2C9V](2C9V-whole-take-folder-scope-and-package.md)).
- Item 5: one approved example fixes the conventions before 15 more results use them.
- Item 6: the real bytes of a killed MKV wait for the desk tests.
- Item 7: a file that no golden folder needs stays out of `golden/`.
- Item 8: decoders differ in the pixel values and the sample values that they give.
- Item 10: the encoders do not promise the same bytes on each platform.

## Evidence

For item 10, measured on 2026-11-16 on Windows x86-64 with Python 3.13.13: av 19.0.2 (FFmpeg 9.0.2,
libopus 1.6.1), pillow 13.0.0, numpy 2.4.6 and pyarrow 26.0.0.

- Three runs each gave identical bytes for JPEG, for Opus in fragmented MP4, for Parquet and for a
  stored NPZ with fixed ZIP dates and `create_system` 0.
- The MKV was identical only with the muxer option `fflags=+bitexact`. Without it, `SegmentUID` and
  `TrackUID` are random.

No script is tracked for this measurement.

## Open work

[open-work.md](../open-work.md)
