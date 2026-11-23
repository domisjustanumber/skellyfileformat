# T24G — Spec v1 review fixes: crash reading, repair details, fit evaluation, audio and camera details

**Status:** superseded by [G1YG](G1YG-writing-crash-reading-and-repair.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

The user accepted each item. The source of each item in the review is in brackets. These items
add to [ADR-MG7C](MG7C-fit-segments-by-position.md),
[ADR-PV6S](PV6S-writing-crash-reading-and-repair.md) and
[ADR-D9N1](D9N1-opus-audio-settings-and-timing.md). They change none of their rules.

1. **Records before the first chunk.** A writer writes the Metadata records of the file facts, then
   each Schema and Channel record of the file (also the log channel), outside chunks and before
   the first chunk. [S1]
2. **Chunk CRC checks.** A reader checks the CRC of each chunk that it reads, in a finished or an
   unfinished file. A wrong CRC makes the file `damaged`, with the reason `crc_mismatch`. A computed
   CRC of 0 is allowed, and a reader does not check a CRC of 0 (MCAP). A reader can skip the
   data-section CRC. [S5]
3. **End of a crash read.** A record with the opcode 0x00, or with a length that goes past the end
   of the file, is not complete. It ends the read, and its bytes count in `torn_bytes`. [S4]
4. **Repair cut details.** The repair keeps a chunk only when all of its Message Index records are
   complete. With no chunk to keep, it cuts after the last record before the first chunk. [S2]
5. **Re-chunked files.** A reader of a finished file compares the image message count in the
   Statistics record with the number of image chunks and `frames_per_chunk`. On a mismatch, it
   refuses the file. [S2]
6. **Interrupted repair.** `cut_bytes` counts the bytes that this repair removed. After an
   interrupted repair, a new repair gives the same Messages, the same `freemocap.timing` record and
   the same bytes before the cut, but `cut_bytes` can differ. [S3]
7. **Fit evaluation.** The fitted time of the frame at position p in a segment is
   `t0_ns` + ⌊d × `period_ps` / 1000⌋, where d = (sequence(p) − sequence(`pos_first`)) modulo 2^32.
   A reader computes it with integers of unlimited size (Python `int`, JavaScript `BigInt`). The
   result is less than 2^64. In a segment, the `sequence` increases from each position to the next,
   modulo 2^32. [B1, S13]
8. **Fit cover.** The segments together hold each position of the file. [S13]
9. **Unfinished files.** A reader of an unfinished file does not use a `freemocap.timing` record. It
   uses the arrival times. [nit]
10. **Output gain.** A reader does not apply an output gain. [S6]
11. **First packets after a seek.** To start at packet k, a reader decodes from packet max(0, k − 4).
    When it starts at packet 0, it drops the `pre_skip` samples. [S18]
12. **EXIF orientation.** A reader ignores an EXIF orientation tag in a JPEG. (The writer rule is
    already ADR-68Z6 item 3.) [S9]
13. **Encoder-skip details.** The Log Message of an encoder skip has `publish_time` = `log_time` and
    `sequence` = the frame number of the skipped frame modulo 2^32, or 0 when it is not known. A
    reader gives the warning `encode_skip` when the count is more than 0. [S15]
14. **Schema imports.** The FileDescriptorSet of each Schema includes its imports, as
    `protoc --include_imports` makes it (the MCAP registry rule). [S17]
15. **skellysync and the fit.** A reader does not give `missing_fit` for a file with `clock_id`
    128, because skellysync writes no fit. [nit]

## Reason

- The spec v1 review found these gaps. Each item gives one answer where two readers could do
  different things, or where a crash or a rare value has no rule.
- Item 1: a crashed file whose first chunk is torn still gives its label and channel facts.
- Item 2: a CRC-32 of 0 occurs about once in 40,000 camera-hours at 30 fps.
- Item 3: after a power loss, a file tail can be zeros, and MCAP defines no opcode 0x00.
- Item 5: `mcap recover` writes chunks by size, so a position would show the wrong frame.
- Item 7: d × `period_ps` passes 2^53 after about 2.5 h at 30 fps.
- Item 12: browser decoders apply EXIF orientation by default, which would rotate a frame twice.

## Evidence

- skellycam `dom/research` (local commit, not pushed):
  `research/skellycam_recording/docs/spec_v1_review_20261113.md`.

## Consequences

- Item 1 needs a writer that writes Schema and Channel records outside chunks. The `mcap` 1.6.0
  Python `Writer` puts them in the first chunk, so the writer of this package needs its own record
  order.
