# Choices made for G1 that the spec does not give

**Accepted by the user on 2026-11-16** ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 5).
The later golden folders copy these choices as conventions of the golden folders. An item is a rule
of the format only where the spec states it.

The golden generator (`tools/goldgen/`) needed each of these values to write G1
([README.md](README.md)). The spec does not give them. Each item gives the gap, the choice and the
alternative ([ADR-G21H](../decisions/entries/G21H-gate-2-tests-location-and-interfaces.md) item 5).
Items 30 to 34 are points where the spec and the pinned tools, or two texts, did not agree. The same
entry decided items 20, 22, 23 and 30: each of them gives its decision. Items 13, 14, 15 and 24 can
be rules of the format: the user must decide ([open-work.md](../decisions/open-work.md)).

1. Appendix A gives no `<rec>` for a golden take. Choice: `g01_synthetic_take`, the same in the
   two cases. Alternative: the case name.
2. SFF-703 says that `take_uuid` is a random UUID version 4. A golden value must be synthetic.
   Choice: `00000000000040008000000000000001`, which has the version and variant bits of a
   version 4 UUID and is not random. Alternative: a random value, fixed in the script.
3. SFF-712 gives only an example of a writer string. Choice: `skellyfileformat-goldgen 1.0.0`,
   because the generator wrote the files. Alternative: `skellycam 2.0.0`, as Appendix A says
   that skellycam writes the take. `owner` and `source` in the manifest are `skellycam`, because
   the spec allows no other value for a capture.
4. Sections 8 and 11 do not give the take keys of a golden take. Choice: `clock` `windows_qpc`,
   `clock_hz` 10000000, `take_start_host_ns` 1000000000000, `take_start_utc_ns` of
   2000-01-01T00:00:00Z and `utc_offset_min` 0. Alternative: `clock` `synthetic` and an empty
   `clock_hz`.
5. Appendix A says "about 90 frames at a small size". Choice: 90 frames of 64 × 48 pixels,
   `nominal_rate` 30/1, `display_rotation` 0, and JPEG from Pillow with quality 90 (4:2:0, with a
   JFIF APP0 segment). Alternative: another size or rate.
6. Appendix A says "one with a gap". Choice: camera 1 loses one source frame before position 40.
   The source frame numbers start at 1000 (camera 0) and 500 (camera 1). Each camera has 90 rows,
   so the rows of camera 1 from position 40 are one frame period later than the rows of camera 0
   with the same position (SFF-754 pairs them). Alternative: a gap in camera 0, or a longer gap.
7. The spec does not say if a golden camera has `sample_ns`. Choice: camera 0 has a value in each
   row, and camera 1 has an empty field, so the `records` show a null. Alternative: the two
   cameras the same.
8. SFF-767 does not give the size of a callback block. Choice: 30 blocks of 4,800 samples, each
   with `adc_ns`, and `audio_latency_ns` empty. Alternative: 960 or 1,024 samples; an empty
   `adc_ns`.
9. Appendix A gives no time and no form of a click. Choice: six events, at 100 ms after the take
   start and then each 500 ms. A click is 48 samples of a 4 kHz square wave with a peak of 24,000
   that decays to 0. Its first sample is the sample nearest to the event. The audio between the
   clicks is digital silence, so the mean bitrate of the file is about 94 kbit/s, below the
   128 kbit/s of SFF-762. Alternative: a noise floor between the clicks.
10. Appendix A says "a flash at the time of each click" and SFT-729 says "the matching video
    flash". Neither says which frame shows the flash. Choice: the frame whose fitted time is
    nearest to the event. The whole frame is white. Its fitted time is at most 0.21 ms from the
    event. Alternative: the first frame at or after the event.
11. SFT-723 says "the click offsets equal the source", with no rule to find a click and no
    tolerance. Choice in the cross-check: the first decoded sample with a magnitude of 0.3 or more
    after 100 ms of quiet, within 2 samples of the source. The pinned decoder gives 0 samples.
    A flash frame is a frame with a mean luma above 200.
12. SFF-775 leaves the fit to the writer. Choice: `fitter=goldgen-truth`, `fitter_version=1.0.0`,
    `fitter_params={}`, and one segment for each file, also over the gap of camera 1. The fit is
    the exact line that made the rows: camera 0 `t0_ns` 33483200 and `period_ps` 33333400000;
    camera 1 33133500 and 33333250000; audio `t0_ns` 12345678 and `period_fs` 20833350000.
    Alternative: a fit that a fitter computes from the rows.
13. SFF-700 and SFF-702 do not give the white space of a JSON file. Choice for the manifest and the
    capture info JSON: an indent of 2 spaces, `: ` and `,` as separators, no escape of a character
    above U+007F, and one LF after the last `}`. Alternative: one line.
14. Section 13 does not give the order of the keys of `camera_configs` or of `controls`. Choice:
    `camera_configs` in order of `group_position`, and `controls` in the order of the list of
    SFF-802. Alternative: in order of the key.
15. SFF-881 says "sorted by `file` and then by `field`", with no collation. Choice: the order of
    the UTF-8 bytes. Alternative: the order of the code points (the same for ASCII).
16. SFF-727 allows a text or null in `detail`. Choice: null for the warning `camera_gap`.
    Alternative: a text such as "1 gap".
17. SFF-752 does not decide the text form of `port_path` and `os_device_id`, and it does not say
    if a USB camera has an `os_device_id`. Choice: `vendor_id` `ffff`, `product_id` `0001` and
    `0002`, `port_path` `FAKE-PORT-0` and `FAKE-PORT-1`. Camera 0 has the serial `FAKE-SERIAL-A`
    (form 1) and `os_device_id` null. Camera 1 has no serial and has `os_device_id`
    `FAKE-OS-DEVICE-1`, so its key has form 2 although form 3 is also possible. Alternative:
    `os_device_id` null for each USB camera.
18. The other values of the capture info JSON are free: `user_name` (`Fake camera A`, and null),
    `model`, `os_name`, `backend` `media_foundation`, `os_index`, `requested`, the controls
    (camera 0: `exposure_us` 4000 and `gain` 32; camera 1: `exposure_us` with `value` null and
    `auto` null), `exposure_step` null, and `audio` (`Synthetic Microphone`, `Windows WASAPI`, 1).
    The spec gives no list of values for `backend` and `host_api`.
19. Appendix A does not give the remembered key of the case `confirmed_key`. Choice: the hash of
    the port form with `FAKE-PORT-9`: the camera moved from that port. The case has the same
    `take_uuid` and `<rec>` as `take`. Only camera 1 changes: its key, its label, its file names,
    and the manifest and capture info members that hold them. Alternative: a free 16-character
    value.
20. SFF-891 gives the warning `prerelease` to a file. The manifest also has `format_prerelease` 1,
    but it is never an item of the result (SFF-867), and no take warning has this code (SFF-887).
    Choice: the result shows nothing for the manifest. The `folder_files` item of the capture
    info JSON has `["prerelease"]`. Alternative: a take warning. Confirmed: SFF-891 now states it
    ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 3).
21. The open point "Does a reader check `key_origin`?" applies to `confirmed_key`. Choice: the
    reader does not check it, so the check `camera_key` is `ok` in the two cases.
22. SFF-872 does not say in words if the row-count part of `frames` alone makes the check `ok`
    when the take has no Parquet. Choice: yes. So `frames` is `ok` for the scope `full` and
    `not_checked` for the scope `player`, and this is the only difference between the two
    results of G1. Confirmed: SFF-872 now states it ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 4).
23. **Replaced.** The reader result held no sign of the gap of camera 1: `camera_gap` is a manifest
    warning, not a reader warning, and the flags are not in `records`. Decision: a reader gives a
    camera file the file warning `gap` when one or more usable rows have the flag `gap` (SFF-887).
    The `warnings` of camera 1 are `["gap","prerelease"]` in each result of G1. The `warnings` of
    the take stay `[]` ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 1).
24. SFF-885 does not say if a result file ends with a line end. Choice: no byte after the
    canonical JSON, as for the output of the JavaScript command (SFF-892).
25. Appendix A does not give the format of `SHA256SUMS`. Choice: the format of `sha256sum`: the
    sum, two spaces, the path relative to `G<NN>/` with `/`, LF, in order of the bytes of the
    path. The file does not list itself.
26. Appendix A has no file for the facts that a test needs and that the result does not hold.
    Choice: `<case>.truth.json` beside the case folder, in canonical JSON, with `click_samples`
    and `flash_positions`. SFT-723 and SFT-729 need them. Alternative: constants in the tests.
27. ADR-G21H names the functions that the tests call, and not their module. Choice in
    `tests/conformance/conftest.py`: the fixtures `reader` and `writer` return the module
    `skellyfileformat`, `golden(name, case="take")` returns the case folder, and
    `js_reader(folder, records=False)` returns the bytes of the standard output.
28. Section 6 does not say which other elements a camera file can hold. The pinned FFmpeg writes
    a SeekHead, a Void, Cues, Tags with `DURATION`, a `Duration`, a `Colour` element, a CRC-32
    element in each top element, `DocTypeVersion` 4 and the text `Lavf` as `MuxingApp` and
    `WritingApp`. Choice: keep them. It starts a new Cluster after each 5 frames, so each camera file of
    G1 has 18 Clusters.
29. Section 9 does not say which other boxes an audio file can hold. The pinned FFmpeg writes
    `ftyp` with the brand `iso5`, an empty `udta/meta`, and a `btrt` box in the sample entry.
    Choice: keep them. The last fragment holds one packet with a duration of 312 samples (the
    end of the encoder delay), so the file holds 144,312 − 312 = 144,000 samples (SFF-785).
30. **Replaced.** SFF-736 rounded `DefaultDuration` half up. FFmpeg 9.0.2 rounds it down:
    33,366,666 for 30000/1001, where the spec gave 33,366,667. Decision: SFF-736 now rounds
    `DefaultDuration` down, as the tool does. The block timestamps stay rounded half up. G1 has
    30/1, where the two rules agree (33,333,333), so no byte of G1 changes ([ADR-94YQ](../decisions/entries/94YQ-golden-g1-review-decisions.md) item 2).
31. **Not shown by a file.** The settings `application`, VBR and complexity of SFF-762, and the
    flush after each packet of SFF-764, are not in the file. The generator sets them through
    PyAV. No test of the golden files can check them.
32. **Decoder length.** PyAV decodes 144,648 samples from the audio file: it drops the pre-skip
    and it does not cut the padding of the last packet. A test must use the length of SFF-785,
    not the decoded length.
33. **Tool versions.** `[tool.uv] exclude-newer` is new. With it, `uv lock` moved four packages
    that `pre-commit` needs to older releases (filelock, platformdirs, python-discovery and
    virtualenv): the old lock had releases of less than 14 days.
34. **Stale texts outside this work.** The `description` of `pyproject.toml` says "FLAC audio".
    The `tools/` row of the path table of `AGENTS.md` names only the doc checks.
