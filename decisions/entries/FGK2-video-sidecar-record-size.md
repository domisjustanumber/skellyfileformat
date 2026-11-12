# FGK2 — Video timing sidecar: one record for each frame, with a `record_size`

**Status:** accepted, 2026-11-12 (user).

## Decision

1. The video timing sidecar has a header and one record for each frame. The header holds
   `record_size`. In format version 2.0, `record_size` is 64. A later minor version can make the
   record larger. Its new fields go after the fields of version 2.0 and before the record CRC.
2. The record CRC is always the last 4 bytes of the record. It covers all the bytes of the record
   before it. A reader steps through the records by `record_size`.
3. Each record holds: the arrival time, the sample time, the legacy time and the fitted time, in
   nanoseconds; the byte offset and the size of the JPEG in the MKV; the JPEG CRC; the source frame
   number; the write index; flags; and the record CRC.
4. The header holds `header_size` and `n_records`. `header_size` and `record_size` are multiples of
   8.
5. The player time never decreases in one file.
6. A JavaScript reader reads each 64-bit integer as two unsigned 32-bit halves. It does not use
   `BigInt`.
7. A reader does not check each record CRC when it loads a finalised file. A finalised sidecar holds
   a CRC of all the bytes after the header (`body_crc32`) and a header CRC. A reader that checks
   `body_crc32` does not need to check the record CRCs.
8. The sidecar has no columnar or compact section.
9. The spec gives the field order, the types and the flag bits.

This entry supersedes [ADR-69YS](69YS-video-sidecar-record.md) in full. Items 3 to 6, 8 and 9
restate its rules that stay. Items 1, 2 and 7 change its item 1 (a fixed 64-byte record) and add to
its item 6.

## Reason

- skellysync needs more per-frame fields later (a source presentation time and a source frame index
  of 64 bits). With a fixed 64-byte record, each new per-frame field needs a new major version or a
  second table. With `record_size`, a minor version can add it, and older readers still read the
  file.
- A reader that knows where the CRC is can check a record that has fields it does not know.
- `body_crc32` lets a reader find damage in a finalised sidecar without a check of each record CRC.
  The JavaScript check of each record CRC costs about 8 times the parse time.
- The reasons of ADR-69YS for a row of fixed size stay: it is simple to write live, to recover after
  a crash and to implement in another language, and the row layout loads fast enough.

## Evidence

- T-S4 ([FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/sidecar_load/FINDINGS.md)):
  16 cameras of 1 h each load in 95–195 ms. The JavaScript check of each record CRC adds 210–767 ms.

## Alternatives rejected

- A fixed 64-byte record for the whole major version: each new per-frame field then needs a new
  major version or a second table.
- A columnar or compact section: T-S4 shows no need for it.
