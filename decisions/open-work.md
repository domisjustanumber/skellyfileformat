# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **Absorb the format entries into the spec.** When `spec/SPEC.md` or `README.md` states all rules of
  an entry, move the entry to Historical as absorbed:
  [ADR-69YS](entries/69YS-video-sidecar-record.md),
  [ADR-0YV1](entries/0YV1-fitted-time-in-sidecar.md),
  [ADR-CA03](entries/CA03-flac-audio.md),
  [ADR-77Z3](entries/77Z3-finalisation-embed-verify-delete.md),
  [ADR-VJ14](entries/VJ14-shared-package-and-spec.md),
  [ADR-5K7G](entries/5K7G-no-recorded-overlays.md),
  [ADR-X7FT](entries/X7FT-read-old-write-new.md),
  [ADR-M4DF](entries/M4DF-format-versioning.md) and
  [ADR-CD4G](entries/CD4G-spec-first-and-repository-rules.md).
- **Spec v0 and its conformance list.** `spec/SPEC.md` and `spec/conformance.md` hold only headings.
  Write them, then stop for the review of the user (gate 1)
  ([ADR-CD4G](entries/CD4G-spec-first-and-repository-rules.md)).
- **Provisional parts of spec v0.** Mark these parts provisional in `spec/SPEC.md`. Close each of
  them before v2.0.0: the fields that wait for the audio clock drift test and for the Linux and
  macOS audio timing test, and the skellysync camera sidecar header, which waits for the skellysync
  decisions D-Q, D-FPS, D-HDR and D-DRIFT
  ([ADR-CD4G](entries/CD4G-spec-first-and-repository-rules.md)).
- **Recording manifest: in the spec or in skellycam?** [ADR-83Y4](entries/83Y4-recording-manifest.md)
  puts the files, the key and the Segment UID of each camera in skellycam's recording info JSON.
  The key is the stable camera key: the serial number, else the port path (skellycam plan row 2.6).
  The scope of spec v0 does not list the manifest. The user must decide if `spec/SPEC.md` defines
  these fields, or if skellycam defines them.
- **S10b: correct the audio start of old recordings?** The audio of old skellycam recordings is
  9–74 ms early. The user must decide if playback corrects it
  ([ADR-X7FT](entries/X7FT-read-old-write-new.md)). skellycam does the legacy playback, so the
  result goes into a skellycam entry. Delete this item when that entry exists.
