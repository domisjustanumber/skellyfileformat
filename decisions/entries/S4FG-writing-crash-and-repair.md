# S4FG — Writing rules: fixed-count chunks, no compression, data CRC, fsync; repair of a crashed file only after the user agrees

**Status:** accepted, 2026-11-13 (user).

## Decision

1. **Video chunks.** Each video chunk holds exactly `frames_per_chunk` frames, except that the last
   chunk can hold fewer. `frames_per_chunk` is in the channel metadata. A writer uses 1. A reader
   handles any value: the chunk of frame position p is chunk p ÷ `frames_per_chunk`, rounded down.
2. **Audio chunks.** Each audio chunk holds 5 Opus packets (100 ms), except that the last can hold
   fewer.
3. **Compression.** Chunk compression is none.
4. **CRCs.** Chunk CRCs are on. A file that finishes normally also has the data-section CRC. A
   repaired file writes 0 there, which MCAP defines as "not available".
5. **fsync.** While it records, a writer forces its file to disk about once a second. The spec
   fixes the interval after its cost is measured.
6. **Crashed files, read in place.** A reader reads a file with no summary in place: it reads each
   complete chunk in file order, and it reports the file as unfinished. It checks that the read
   reached a clean end, because a streaming reader can stop at a torn tail with no error.
7. **Repair only after the user agrees.** When skellycam finds an unfinished file that it owns, it
   asks the user: "An incomplete recording was found. Would you like to repair it?" Only when the
   user agrees does it repair the file in place:
   - it cuts off any torn bytes after the last complete record;
   - it appends a DataEnd record, a rebuilt summary and a footer;
   - it adds the `freemocap.timing` record of each camera file.

   It never rewrites a byte before the torn tail.

## Reason

- One frame per chunk lets a reader find any frame from the summary alone, with one request per
  frame. A process kill then loses at most the frame being written. The cost is about 10 MB of
  summary per camera-hour.
- The fixed-count rule lets long takes move to more frames per chunk later with no reader change.
- One Opus packet per chunk nearly doubled the microphone file.
- JPEG and Opus do not compress further, and compression would stop one-request frame reads. Raw
  capture can add compression later.
- A process kill keeps the operating system's write cache; a power cut or an OS crash does not.
- A repair in place avoids a copy of hundreds of GB. The user decides, because the repair changes
  their file.

## Evidence

- skellycam `dom/research` (local commits, not pushed), under `research/skellycam_recording/`:
  - `recording_upgrade/results/mcap_kill/FINDINGS.md`: 120 kills, no flushed data lost, no torn
    record;
  - `recording_upgrade/results/mcap_electron/FINDINGS.md`: one-request frame reads; the stream
    reader stops at a cut with no error;
  - `recording_upgrade/results/mcap_single_writer/FINDINGS.md`: summary size and memory against
    the chunk count;
  - `docs/mcap_profile_decisions_20261113.md`: Q15 to Q18 and Q20.

## Alternatives rejected

- Time-window chunks across cameras: not possible with one file per device.
- A repair through `mcap recover`: it copies the whole file.
- An automatic repair with no question to the user.

## Open work

[open-work.md](../open-work.md)
