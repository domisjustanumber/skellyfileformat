# Decision log: historical entries

These entries are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done`. They are not in the read path. Read an entry here only to find
the reason for a decision. The [index](README.md) has the Active and Proposed entries and the
[Rules](README.md#rules).

### Historical

| # | Decision | Status |
|---|----------|--------|
| [CD4G](entries/CD4G-spec-first-and-repository-rules.md) | Spec first with two review gates; normative documents; IDs; golden files; licenses; commits to main until v2.0.0 | superseded by 5PP8 |
| [83Y4](entries/83Y4-recording-manifest.md) | The recording info JSON lists each camera's MKV, sidecar, key and Segment UID | superseded by 5PP8 |
| [69YS](entries/69YS-video-sidecar-record.md) | Video timing sidecar: a header plus one 64-byte record for each frame; no columnar section | superseded by FGK2 |
| [77Z3](entries/77Z3-finalisation-embed-verify-delete.md) | At finalisation, append each sidecar as an MKV attachment at the end of the file, verify, then delete the separate files | superseded by 3KH3 |
| [5PP8](entries/5PP8-whole-recording-scope.md) | The format describes a whole synchronised recording; headers authoritative; a derived recording manifest; spec first; repository rules | superseded by 25VV |
| [FGK2](entries/FGK2-video-sidecar-record-size.md) | Video timing sidecar: a header plus one record for each frame; `record_size` (64 in 2.0) lets a minor add fields; CRC last | superseded by SFK5 |
| [3KH3](entries/3KH3-finalisation-embed-fallback.md) | Embed each sidecar at the end of its file when the appender can, else keep it separate; verify, then delete; recover an interrupted embed | superseded by SFK5 |
| [WD1R](entries/WD1R-file-attachment-and-mime-names.md) | Names: `.skvt`/`.skat` (magics `SKVT`/`SKAT`), attachment names and MIME types; one live audio sidecar; manifest name | superseded by SFK5 |
| [CA03](entries/CA03-flac-audio.md) | FLAC is the audio codec; skellycam writes `.audio.mka` with `.skau`, skellysync a FLAC track in each camera MKV | superseded by HD8Z |
| [X7FT](entries/X7FT-read-old-write-new.md) | Old recordings stay readable; new skellycam and skellysync write only this format; no sidecar means legacy | superseded by X1G6 |
| [M4DF](entries/M4DF-format-versioning.md) | Format version = major.minor of the skellycam release that last changed the format; u16 major/minor/prerelease in each header | superseded by 7K3C |
| [25VV](entries/25VV-whole-recording-scope-names.md) | The format describes a whole synchronised recording; headers authoritative; derived manifest; spec fixes only its own names; repo rules | superseded by 41VF |
| [CE4D](entries/CE4D-rotation-in-header-only.md) | Frames stored unrotated; `display_rotation` in the sidecar header only; no container rotation flag; readers apply it | superseded by 68Z6 |
| [SFK5](entries/SFK5-mcap-container.md) | Each file is an MCAP file; JPEG frames as `foxglove.CompressedImage`; timing in MCAP fields; facts in metadata; no MKV, sidecar or embed | superseded by DK8S |
| [41VF](entries/41VF-whole-recording-scope-mcap.md) | The format describes a whole synchronised recording of MCAP files; file metadata authoritative; derived manifest; spec fixes only its own names; repo rules | superseded by TDB5 |
| [0YV1](entries/0YV1-fitted-time-in-sidecar.md) | The sidecar holds the fitted time of each frame; the player uses it, or the arrival time before finalisation | superseded by FF01 |
| [FF01](entries/FF01-fit-and-breakpoints-in-metadata.md) | Fit segments, fitter and sequence breakpoints per camera in the `freemocap.timing` Metadata record, written before `finish()` | superseded by MG7C |
| [S4FG](entries/S4FG-writing-crash-and-repair.md) | Fixed-count chunks (1 frame, 5 Opus packets), no compression, data CRC, fsync about 1 s; crashed files repaired only if the user agrees | superseded by PV6S |
| [HD8Z](entries/HD8Z-opus-audio.md) | Opus audio as raw packets in `foxglove.CompressedAudio`; OpusHead fields in channel metadata; pre-skip and 80 ms seek pre-roll | superseded by D9N1 |
| [QDZ7](entries/QDZ7-opus-settings-and-timing.md) | Opus: device channels (max 2), 48 kHz, 20 ms, `audio`, VBR 128/256 kbit/s; timestamp = first decoded sample; reader drops pre-skip | superseded by D9N1 |
| [VJ14](entries/VJ14-shared-package-and-spec.md) | skellyfileformat is the one shared package for the format, with a descriptive spec; the spec fixes the names | superseded by W4PF |
| [5K7G](entries/5K7G-no-recorded-overlays.md) | No recorded overlays: no burned-in stamp, no overlay file or attachment; the player draws the frame label | superseded by W4PF |
| [TDB5](entries/TDB5-whole-recording-no-manifest.md) | Whole recording of per-device MCAP files; no manifest; takes grouped by `take_uuid`; canonical reader-result JSON; repo rules | superseded by 2C9V |
| [W4PF](entries/W4PF-shared-package-and-no-overlays.md) | One shared package (spec, tests, golden files, Python and JS readers, writer); spec fixes its own names, not file names; no recorded overlays | superseded by 2C9V |
| [DK8S](entries/DK8S-mcap-profile-files-and-names.md) | One MCAP file per device; profile `freemocap`; protobuf; topics carry the label; `freemocap.*` metadata records; writer in Header `library` | superseded by 6RSB |
| [752H](entries/752H-timing-fields.md) | Arrival in `log_time`, sample time in `timestamp`, `sequence` = frame or packet number; no legacy time; encoder skips as `foxglove.Log` | superseded by 6RSB |
| [MG7C](entries/MG7C-fit-segments-by-position.md) | Fit segments keyed by position (`pos_first`, `pos_last`), in position order with no gap; fitter named; breakpoints give `sequence` | superseded by 6RSB |
| [D9N1](entries/D9N1-opus-audio-settings-and-timing.md) | Opus in `foxglove.CompressedAudio`; OpusHead fields in channel metadata, `sample_rate` = decode rate, gain 0; 48 kHz 20 ms VBR; log_time = arrival | superseded by 92TM |
| [WD9A](entries/WD9A-lichtblick-reference-viewer.md) | Lichtblick is the external test viewer, not Foxglove; VLC compatibility dropped; audio tests use a pinned Lichtblick build with an Audio panel | superseded by 92TM |
| [10JC](entries/10JC-lichtblick-audio-checks.md) | Lichtblick audio checks: mrkbac/lichtblick at 70f5900, built offline, Opus picked by hand at 48 kHz, 1x only; sync judged in skellycam | superseded by 92TM |
| [7K3C](entries/7K3C-format-versioning-in-metadata.md) | Format version = major.minor of the skellycam release that last changed the format; major/minor/prerelease in each file's metadata | superseded by 9DV4 |
| [X1G6](entries/X1G6-read-old-write-mcap.md) | Old recordings stay readable; new skellycam and skellysync write only MCAP with JPEG and Opus; no file of this format means legacy | superseded by CZQ9 |
| [68Z6](entries/68Z6-rotation-in-metadata-only.md) | Frames stored unrotated; `display_rotation` in the camera file's metadata only; no other rotation; readers apply it | superseded by DE9S |
| [PV6S](entries/PV6S-writing-crash-reading-and-repair.md) | Fixed-count chunks, no compression, data CRC, fsync ~1 s; crashed files read in place; user-approved repair cuts after the last good chunk | superseded by G1YG |
| [T24G](entries/T24G-spec-v1-review-fixes-crash-fit-audio.md) | Spec v1 review fixes, 15 items: records before first chunk, CRC checks, crash-read end, repair details, fit maths and cover, Opus and camera details | superseded by G1YG |
| [5G42](entries/5G42-gate1-names.md) | Gate 1 names: `freemocap.repair` record, audio `label`, `audio_latency_ns` in the audio channel metadata, RFC 8785 reader result | superseded by G1YG |
| [WG08](entries/WG08-reader-result-states-and-codes.md) | Reader result: `invalid` state, folder states, reason and warning codes, `audio_count`, take counting, null members, integer types, sort orders | superseded by KW3G |
