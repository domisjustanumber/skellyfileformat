# 69YS — Video timing sidecar: one 64-byte record for each frame

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. The video timing sidecar has a header and one fixed 64-byte record for each frame.
2. Each record holds: the arrival time, the Media Foundation sample time, the legacy time and the
   fitted time, in nanoseconds; the byte offset and the size of the JPEG in the MKV; the JPEG CRC;
   the source frame number; the write index; flags; and a record CRC.
3. The header holds `header_size` and `n_records`. `header_size` is a multiple of 8.
4. The player time never decreases in one file.
5. A JavaScript reader reads each 64-bit integer as two unsigned 32-bit halves. It does not use
   `BigInt`.
6. A reader does not check each record CRC when it loads a finalised file.
7. The sidecar has no columnar or compact section.
8. The spec gives the field order, the types and the flag bits.

## Reason

- A row of fixed size is simple to write live, to recover after a crash and to implement in another
  language.
- The T-S4 load test shows that the row layout is fast enough. A columnar section adds code and
  gives no measurable gain.

## Evidence

- T-S4 ([FINDINGS](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellycam_recording/recording_upgrade/results/sidecar_load/FINDINGS.md)): 16 cameras of 1 h each load in 95–195 ms. The
  first frame takes 3–5 ms with a hybrid load. A lookup costs about 1 µs for each draw.
- Plan row S1 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.

## Alternatives rejected

- A columnar or compact section: T-S4 shows no need for it.
