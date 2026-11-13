# PV6S — Writing rules and crash reading; the repair of a crashed file cuts after the last good chunk, only after the user agrees

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
   - it cuts the file after the last complete chunk that has a correct CRC, with its complete
     Message Index records. A chunk after a damaged chunk is lost, also when it is good;
   - it appends the `freemocap.timing` record of each camera file, a record of the repair, a DataEnd
     record, a rebuilt summary and a footer.

   It never rewrites a byte before the cut. A repair that stops before its end leaves an unfinished
   file, and a new repair starts again from the same cut.

This entry supersedes [ADR-S4FG](S4FG-writing-crash-and-repair.md) in full. Items 1 to 6 restate
its items 1 to 6. Item 7 restates its item 7, with the cut after the last good chunk in place of
"cuts off any torn bytes after the last complete record".

## Reason

- After a wrong chunk CRC, the bytes after it cannot be trusted. A cut after the last good chunk is
  simple and safe, and it loses data only in the rare damaged case.
- From ADR-S4FG: one frame per chunk lets a reader find any frame from the summary alone, and a
  process kill loses at most the frame being written. The fixed-count rule lets long takes move to
  more frames per chunk with no reader change. One Opus packet per chunk nearly doubled the
  microphone file. JPEG and Opus do not compress further. A process kill keeps the operating
  system's write cache; a power cut does not. A repair in place avoids a copy of hundreds of GB, and
  the user decides because the repair changes their file.

## Evidence

- skellycam `dom/research` (local commits, not pushed), under `research/skellycam_recording/`:
  - `docs/spec_v1_review_20261113.md` (S2) and the answers of the user in it;
  - `recording_upgrade/results/mcap_kill/FINDINGS.md`: 120 kills, no flushed data lost, no torn
    record;
  - `recording_upgrade/results/mcap_electron/FINDINGS.md`: one-request frame reads; the stream
    reader stops at a cut with no error;
  - `recording_upgrade/results/mcap_single_writer/FINDINGS.md`: summary size and memory against
    the chunk count;
  - `docs/mcap_profile_decisions_20261113.md`: Q15 to Q18 and Q20.

## Alternatives rejected

- Cut only the torn bytes after the last complete record (ADR-S4FG item 7): a damaged chunk in the
  middle of the file has no defined repair.
- Time-window chunks across cameras: not possible with one file per device.
- A repair through `mcap recover`: it copies the whole file.
- An automatic repair with no question to the user.

## Open work

[open-work.md](../open-work.md)
