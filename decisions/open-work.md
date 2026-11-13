# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Gate 1: write spec draft v2.** A sub-agent reviewed draft v1. The user decided its points in
  [ADR-MG7C](entries/MG7C-fit-segments-by-position.md),
  [ADR-PV6S](entries/PV6S-writing-crash-reading-and-repair.md),
  [ADR-D9N1](entries/D9N1-opus-audio-settings-and-timing.md),
  [ADR-5G42](entries/5G42-gate1-names.md),
  [ADR-T24G](entries/T24G-spec-v1-review-fixes-crash-fit-audio.md),
  [ADR-WG08](entries/WG08-reader-result-states-and-codes.md) and
  [ADR-W4PF](entries/W4PF-shared-package-and-no-overlays.md). Write spec draft v2 and its tests
  with these rules. Then the user reviews it (gate 1). After gate 1, write the runnable tests and
  the golden files of SPEC.md Appendix A, then stop for gate 2.
- **Absorb the format entries into the spec.** After gate 1, when `spec/SPEC.md` or `README.md`
  states all rules of an entry, move the entry to Historical as absorbed:
  [ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md),
  [ADR-TDB5](entries/TDB5-whole-recording-no-manifest.md),
  [ADR-752H](entries/752H-timing-fields.md),
  [ADR-MG7C](entries/MG7C-fit-segments-by-position.md),
  [ADR-D9N1](entries/D9N1-opus-audio-settings-and-timing.md),
  [ADR-PV6S](entries/PV6S-writing-crash-reading-and-repair.md),
  [ADR-5G42](entries/5G42-gate1-names.md),
  [ADR-T24G](entries/T24G-spec-v1-review-fixes-crash-fit-audio.md),
  [ADR-WG08](entries/WG08-reader-result-states-and-codes.md),
  [ADR-WD9A](entries/WD9A-lichtblick-reference-viewer.md),
  [ADR-10JC](entries/10JC-lichtblick-audio-checks.md),
  [ADR-W4PF](entries/W4PF-shared-package-and-no-overlays.md),
  [ADR-X1G6](entries/X1G6-read-old-write-mcap.md) (only its items 2 and 3: items 1, 4, 5 and 6 are
  skellycam rules),
  [ADR-7K3C](entries/7K3C-format-versioning-in-metadata.md) and
  [ADR-68Z6](entries/68Z6-rotation-in-metadata-only.md).
- **Provisional parts of spec draft v1.** Close each of them before v2.0.0
  ([ADR-TDB5](entries/TDB5-whole-recording-no-manifest.md),
  [ADR-PV6S](entries/PV6S-writing-crash-reading-and-repair.md)):
  - SFF-213: the audio timestamps against the microphone clock wait for the audio clock drift test
    (A4 of the skellycam plan);
  - SFF-216 and the `audio_latency_ns` key: wait for the microphone latency test (A3);
  - SFF-265: the `clock_id` values 2 and 3 wait for the Linux and macOS timing tests (T-S7);
  - SFF-370: the fsync interval waits for a measurement of its cost;
  - SFF-305, SFF-306, SFF-308 and SFF-309: skellysync files wait for the skellysync decisions D-Q,
    D-FPS, D-HDR, D-DRIFT and D-AUDIO.
- **Permalinks to the skellycam evidence.** The new entries cite skellycam `dom/research` files as
  plain paths. Change them to full-SHA permalinks after that branch is pushed
  ([ADR-DK8S](entries/DK8S-mcap-profile-files-and-names.md)).
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-X1G6](entries/X1G6-read-old-write-mcap.md)). skellycam does the legacy playback, so the
  result goes into a skellycam entry. Delete this item when that entry exists.
