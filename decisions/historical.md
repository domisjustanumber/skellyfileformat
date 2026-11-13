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
