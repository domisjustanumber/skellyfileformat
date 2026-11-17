# Q9X2 — Realtime tracking: a CRC-framed binary journal, folded into the Parquet at the end of the take

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **The journal.** During a take, freemocap writes the realtime tracking results to a journal file
   in the take folder. It is a binary file of CRC-framed records: each record has a magic, a length,
   the payload and a CRC-32. The first record is a JSON header that declares each channel in the
   form of a Parquet channel.
2. **The writer** is a node of its own in the freemocap realtime pipeline, a subscriber with its own
   queue, so that the aggregator and the cameras never wait for the disk. It flushes each record
   and forces the file to disk about once a second, off the hot path.
3. **What it stores.** Everything that the realtime pipeline computes: the raw 2D for each camera
   with its confidence; the filtered 2D where it exists; the raw 3D; the filtered 3D; the skeleton
   reconstructions (mapped keypoints, rotations, centre of mass, joint angles); the ChArUco
   observations; the reprojection diagnostics; and the parameter-change events. The values are
   float32.
4. **The fold.** At the end of the take, freemocap folds the journal into a Parquet run with
   `origin` = `realtime` and its coverage block ([ADR-P76Y](P76Y-tracking-parquet.md)).
5. **Delete only after a verified fold.** freemocap deletes the journal only when it has read the
   new Parquet run back and compared the counts and a digest. When the fold fails, it keeps the
   journal. At start-up, freemocap folds each journal that it finds.
6. **Reading a journal.** A reader scans for the magic, checks the length and the CRC of each
   record, skips a bad record, stops at a torn tail and reports the counts.
7. **The journal is freemocap's binary file.** The rule that skellycam writes only standard media
   and human-readable sidecars does not apply to it.
8. **Before adoption,** a load test runs a full realtime session with the journal writer on and
   off, and compares the latency of the aggregator and the dropped frames. A kill test with real
   data (DT11) also runs.

## Reason

- Realtime results must survive a crash. A Parquet file cannot be written live: a test file with 50
  row groups was unreadable until it was closed.
- The CRC-framed journal is the only tested format that survives a kill, a truncation, a 4 KiB hole
  of zeros and a flipped byte without returning wrong data. It costs about 28 µs and 53 KB for
  each frame of four cameras' 2D.
- A CSV journal is about 2.4 times the size and about 68 times the write time (about 1.9 ms for each
  frame). A journal is folded and deleted, so readability gains little.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/docs/realtime_tracking_storage_20261115.md`, §3 and §4;
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 3
  Q12, Q13, Q15; round 7 item 3.

## Alternatives rejected

- A Parquet run written only at the end of the take: a crash loses the realtime results.
- Rolling Parquet segments: many files, about 20 times the CPU, and up to one segment lost.
- An Arrow IPC stream: it returns a wrong batch after a zero-filled tail.
- A CSV journal: size and write time, for a file that nobody reads.

## Open work

[open-work.md](../open-work.md)
