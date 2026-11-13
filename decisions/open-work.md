# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Absorb the format entries into the spec.** When `spec/SPEC.md` or `README.md` states all rules of
  an entry, move the entry to Historical as absorbed:
  [ADR-FGK2](entries/FGK2-video-sidecar-record-size.md),
  [ADR-0YV1](entries/0YV1-fitted-time-in-sidecar.md),
  [ADR-CA03](entries/CA03-flac-audio.md),
  [ADR-3KH3](entries/3KH3-finalisation-embed-fallback.md),
  [ADR-WD1R](entries/WD1R-file-attachment-and-mime-names.md),
  [ADR-VJ14](entries/VJ14-shared-package-and-spec.md),
  [ADR-5K7G](entries/5K7G-no-recorded-overlays.md),
  [ADR-X7FT](entries/X7FT-read-old-write-new.md),
  [ADR-M4DF](entries/M4DF-format-versioning.md),
  [ADR-25VV](entries/25VV-whole-recording-scope-names.md) and
  [ADR-CE4D](entries/CE4D-rotation-in-header-only.md).
- **Gate 1 for spec v0.** `spec/SPEC.md` and `spec/conformance.md` hold the v0 draft. The user
  reviews them (gate 1) ([ADR-25VV](entries/25VV-whole-recording-scope-names.md)). After gate 1,
  write the runnable tests and the golden files of SPEC.md Appendix A, then stop for gate 2.
- **Provisional parts of spec v0.** Mark these parts provisional in `spec/SPEC.md`. Close each of
  them before v2.0.0: the fields that wait for the audio clock drift test and for the Linux and
  macOS audio timing test, and the skellysync camera sidecar header, which waits for the skellysync
  decisions D-Q, D-FPS, D-HDR and D-DRIFT
  ([ADR-25VV](entries/25VV-whole-recording-scope-names.md)).
- **Provisional: clock ids and audio latency.** SFF-165 waits for the Linux and macOS video timing
  tests (T-S7 of the skellycam plan). SFF-251 waits for the microphone latency test (A3 of the
  skellycam plan) ([ADR-25VV](entries/25VV-whole-recording-scope-names.md)).
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-X7FT](entries/X7FT-read-old-write-new.md)). skellycam does the legacy playback, so the
  result goes into a skellycam entry. Delete this item when that entry exists.
