# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Absorb the format entries into the spec.** When `spec/SPEC.md` or `README.md` states all rules of
  an entry, move the entry to Historical as absorbed:
  [ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md),
  [ADR-0YV1](entries/0YV1-fitted-time-in-sidecar.md),
  [ADR-HD8Z](entries/HD8Z-opus-audio.md),
  [ADR-VJ14](entries/VJ14-shared-package-and-spec.md),
  [ADR-5K7G](entries/5K7G-no-recorded-overlays.md),
  [ADR-X1G6](entries/X1G6-read-old-write-mcap.md),
  [ADR-7K3C](entries/7K3C-format-versioning-in-metadata.md),
  [ADR-41VF](entries/41VF-whole-recording-scope-mcap.md) and
  [ADR-68Z6](entries/68Z6-rotation-in-metadata-only.md).
- **Rewrite the spec as an MCAP profile.** `spec/SPEC.md` and `spec/conformance.md` hold the v0
  draft of the MKV design, which [ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md) withdraws. Keep the
  parts that do not depend on the container: the scope and the terms, the versioning, the clocks,
  the times and the fitted time, the files that are not in this format, the recording as a whole,
  the rotation. Withdraw the IDs of the MKV profile, the sidecar layouts, embedding, offsets and the
  sidecar names. Then the user reviews the new draft (gate 1)
  ([ADR-41VF](entries/41VF-whole-recording-scope-mcap.md)). After gate 1, write the runnable tests
  and the golden files, then stop for gate 2.
- **MCAP profile choices.** The user decides these before the new draft
  ([ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md)):
  - one MCAP file for each device of a take, or one file for the take;
  - the message encoding of the schemas (protobuf, FlatBuffers, ROS 2 or JSON);
  - which MCAP field holds the arrival time and which holds the sample time, for video and for
    audio, and the metadata keys that name each clock;
  - the legacy time, the encoder-skip flag and the fitted time: a companion schema, a value that a
    reader computes, or nothing. [ADR-0YV1](entries/0YV1-fitted-time-in-sidecar.md) says that the
    fitted time is in the sidecar record. Supersede it with the answer;
  - chunking (one chunk for each frame or not), chunk compression, and the data section CRC;
  - crashed files: a reader reads them in place, or a writer rewrites them with a recovery step;
  - the metadata record names, the keys and the channel topics;
  - the Opus settings: bitrate, mono or stereo, packet length, application mode
    ([ADR-HD8Z](entries/HD8Z-opus-audio.md)), and whether the player gives the `OpusHead` to
    WebCodecs as `description` (the WebCodecs registration then assumes an Ogg bitstream);
  - from the third review of spec v0: F2 (stale files), F3 (sign of the audio latency), F4 (a
    canonical reader-result JSON) and F6 (bounds of the nominal rate). F1 and F5 are withdrawn
    with the embed and the FLAC file.
- **MCAP desk tests.** Before the new draft, measure: a kill test of the camera and the audio MCAP
  writers with recovery; the files in Lichtblick; Range reads and WebCodecs Opus in Electron; the
  write throughput of four cameras and the microphone ([ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md)).
  The skellycam permalinks of the evidence wait for a push of the skellycam `dom/research` branch.
- **Provisional parts of spec v0.** Mark these parts provisional in `spec/SPEC.md`. Close each of
  them before v2.0.0: the fields that wait for the audio clock drift test and for the Linux and
  macOS audio timing test, and the skellysync camera sidecar header, which waits for the skellysync
  decisions D-Q, D-FPS, D-HDR and D-DRIFT
  ([ADR-41VF](entries/41VF-whole-recording-scope-mcap.md)).
- **Provisional: clock ids and audio latency.** SFF-165 waits for the Linux and macOS video timing
  tests (T-S7 of the skellycam plan). SFF-251 waits for the microphone latency test (A3 of the
  skellycam plan) ([ADR-41VF](entries/41VF-whole-recording-scope-mcap.md)).
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-X1G6](entries/X1G6-read-old-write-mcap.md)). skellycam does the legacy playback, so the
  result goes into a skellycam entry. Delete this item when that entry exists.
