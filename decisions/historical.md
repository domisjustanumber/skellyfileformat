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
