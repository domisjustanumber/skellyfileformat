# 6VRQ — Spec draft v2 details, part 13: ChArUco source, Parquet values, JSON types

**Status:** accepted, 2026-11-16 (user; review of the proposed details).

## Decision

This part holds items 37 to 39 of the proposals that
[ADR-0JVZ](0JVZ-spec-v2-details-part-9.md) introduces. The user accepted
them on 2026-11-16, with the recommended option of each CHOICE. Each alternative stays as a record.

37. **ChArUco rows of G14** (SFF-836; parts/parquet-descriptor.md; SFT-753; G14). CHOICE.
    `<board name>` in `charuco_detector:<board name>` is `<squares_x>x<squares_y>` of the board,
    for example `charuco_detector:5x3`. The board gets no name member. `<id>` in `corner_<id>` is
    the OpenCV corner ID, in decimal. `calibration_take` of G14 gets the processing info JSON and a
    Parquet with one run: the `TIMESTAMPS` rows and the ChArUco `OVERLAY_2D` rows. Appendix A adds
    sections 14 and 16 to G14. Basis (3). Alternative: the fixed name `charuco_detector:board`.

38. **Parquet values that no text defines** (SFF-702, SFF-828, SFF-832, SFF-834, section 17;
    parts/parquet-descriptor.md; SFT-748, SFT-750, SFT-751; G3, G13).
    - a. CHOICE. `segment_topology` has one item for each item of `skeleton.segments`, in that
      order. `name` is the segment name. `parent` is `rest_pose.parents[name]`. `proximal` is
      `frame.origin`, and `distal` is `frame.primary_point`. So the two are landmark names, as in
      `LANDMARKS_3D`. SFF-832 says "landmark names". Alternative: tracker keypoint names.
    - b. Times. s is the strict player time of a frame, in nanoseconds. A camera `timestamp_s` is
      the float64 nearest to s / 10^9. S is the sum of s over the n cameras of the sensor group at
      one frame. The group time is m = ⌊(2 × S + n) / (2 × n)⌋ ns: the mean, rounded half up. ⌊⌋
      rounds down also for a negative value. The group `timestamp_s` is the float64 nearest to
      m / 10^9.
    - c. CHOICE. `coverage`, for one sensor group and stage: `frames_in_take` is `sample_count`.
      `frames_processed` is the number of frames with one or more data records of a channel of the
      group and stage. `skips` is `{"no_record": frames_in_take − frames_processed}`: the journal
      holds no reason. `clean_close` is true when the journal has a good end record. The latency
      of a data record that counts in SFF-845 is `processed_ns` − m. For k latencies in
      increasing order, `p50` is latency ⌈0.5 × k⌉ and `p99` is latency ⌈0.99 × k⌉, each as the
      float64 nearest to ns / 10^6. Each is null when k is 0. Alternative: a journal record type
      that gives the reason of each skip.
    - d. An event has `time_ns` (an integer JSON number: the host-clock time of the change,
      relative to the take start), `stage` (a processing stage), `parameter` (a text) and `value`
      (a JSON value). SFF-702 gets: in version 2.0, no member of a JSON file is an integer in a
      string, because each time in a JSON file is relative to the take start.
    - e. `<stage>` in the `OVERLAY_2D` names is the name of a stage of the tracker: a text with 1
      or more characters and no `.`. It is not a processing stage. The part writes
      `<tracker stage>.<point>`.
    - f. The names of `JOINT_ANGLES` are the names of `joint_angle_names` of the source
      definition: each joint in member order, each name in array order. Writer rule: no two joints
      of a model have an equal angle name. The two joints of the example of the part get different
      names (`base_tip_z` and so on). The load check of
      [ADR-W5JC](W5JC-nested-model-types-in-the-descriptor-part.md) ran again (Evidence).
    - g. `video_filename` and `timing_filename` are file names with no folder. The files are in the
      media folder. The `files` check tests `synchronized_videos/<name>`.

    Basis (2): the evidence below, for items a, e, f and g; (3) for items b, c and d.

39. **JSON types in the structure check** (parts/parquet-descriptor.md; SFF-893; SFT-770). An
    "integer" is a JSON number with no fraction in its value: `1` and `1.0` pass. A "float" is each
    JSON number: `0` passes for `position`. A text is a JSON string. Basis (3): RFC 8259 has one
    number type.

## Reason

- Items 37 and 38: the generator must write the Parquet of G3, G13 and G14 from the spec alone.
- Item 39: two persons must read the same structure check from the part.

## Evidence

- freemocap at c27fc299: `freemocap/core/recording/result_processing/observation_publication.py`,
  line 91 (`video_filename=video.file_path.name`);
  `freemocap/core/recording/sample_encoding/reconstruction_samples.py`, lines 228 to 242 (the
  `JOINT_ANGLES` names); `freemocap/core/reconstruction/recording_timing.py`, lines 44 to 46 (a
  float mean today); `freemocap/core/pipeline/dataflow/recording_pipeline.py`, lines 125 to 127
  (ChArUco is a tracker stage today, not a source).
- Item 38f, 2026-11-16: `RecordedModel` of freemocap at c27fc299, with skellyforge at f5404db and
  skellytracker at 03b9c1d, loads the changed example of the part and gives the same JSON value
  again, and the model restores. No script is tracked.
- skellytracker at 03b9c1d:
  `skellytracker/core/detectors/keypoint_detectors/charuco/charuco_board_definition.py`: the board
  has no name.
- skellycam `dom/research` (local, not committed), `research/skellycam_recording/docs/`:
  `parquet_inventory_20261116.md` section 3.6 (the stage of `<stage>.<point>` is a tracker stage);
  `skeleton_definition_history_20261115.md` ("proximal/distal landmarks");
  `realtime_tracking_storage_20261115.md` section 4 (the skip reasons are only a proposal).

## Open work

[open-work.md](../open-work.md)
