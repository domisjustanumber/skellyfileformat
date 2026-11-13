# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Gate 1 for spec draft v1.** `spec/SPEC.md` and `spec/conformance.md` hold draft v1, the MCAP
  profile. The user reviews them (gate 1)
  ([ADR-TDB5](entries/TDB5-whole-recording-no-manifest.md)). After gate 1, write the runnable tests
  and the golden files of SPEC.md Appendix A, then stop for gate 2.
- **Absorb the format entries into the spec.** After gate 1, when `spec/SPEC.md` or `README.md`
  states all rules of an entry, move the entry to Historical as absorbed:
  [ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md),
  [ADR-TDB5](entries/TDB5-whole-recording-no-manifest.md),
  [ADR-752H](entries/752H-timing-fields.md),
  [ADR-FF01](entries/FF01-fit-and-breakpoints-in-metadata.md),
  [ADR-HD8Z](entries/HD8Z-opus-audio.md),
  [ADR-QDZ7](entries/QDZ7-opus-settings-and-timing.md),
  [ADR-S4FG](entries/S4FG-writing-crash-and-repair.md),
  [ADR-WD9A](entries/WD9A-lichtblick-reference-viewer.md),
  [ADR-10JC](entries/10JC-lichtblick-audio-checks.md),
  [ADR-VJ14](entries/VJ14-shared-package-and-spec.md),
  [ADR-5K7G](entries/5K7G-no-recorded-overlays.md),
  [ADR-X1G6](entries/X1G6-read-old-write-mcap.md),
  [ADR-7K3C](entries/7K3C-format-versioning-in-metadata.md) and
  [ADR-68Z6](entries/68Z6-rotation-in-metadata-only.md).
- **Provisional parts of spec draft v1.** Close each of them before v2.0.0
  ([ADR-TDB5](entries/TDB5-whole-recording-no-manifest.md),
  [ADR-S4FG](entries/S4FG-writing-crash-and-repair.md)):
  - SFF-213: the audio timestamps against the microphone clock wait for the audio clock drift test
    (A4 of the skellycam plan);
  - SFF-216 and the `audio_latency_ns` key: wait for the microphone latency test (A3);
  - SFF-265: the `clock_id` values 2 and 3 wait for the Linux and macOS timing tests (T-S7);
  - SFF-370: the fsync interval waits for a measurement of its cost;
  - SFF-305, SFF-306, SFF-308 and SFF-309: skellysync files wait for the skellysync decisions D-Q,
    D-FPS, D-HDR, D-DRIFT and D-AUDIO.
- **Names that draft v1 adds, for gate 1.** Draft v1 names a `freemocap.repair` Metadata record
  (SFF-376) and the `label` key of the audio channel. It puts `audio_latency_ns` in the audio channel
  metadata, not in `freemocap.recording`. It serialises the reader result of SFF-678 with RFC 8785.
  The user confirms these at gate 1
  ([ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md)).
- **Permalinks to the skellycam evidence.** The new entries cite skellycam `dom/research` files as
  plain paths. Change them to full-SHA permalinks after that branch is pushed
  ([ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md)).
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-X1G6](entries/X1G6-read-old-write-mcap.md)). skellycam does the legacy playback, so the
  result goes into a skellycam entry. Delete this item when that entry exists.
