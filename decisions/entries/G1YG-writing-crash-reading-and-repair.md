# G1YG — Writing rules for the folder; crashed files read in place; repair only after the user agrees

**Status:** superseded by [G9ER](G9ER-consolidation-of-the-pushed-entries.md),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **Files written whole** (the manifest, the info JSONs, the calibration TOML, the Parquet): the
   writer writes `<name>.tmp`, forces it to disk, then replaces the old file with it. A crash leaves
   the old file, or no file, and a stray `.tmp`. It never leaves a half-written file.
2. **Files written live** (the MKV, the CSV sidecars, the MP4 audio, the realtime journal): the
   writer appends and flushes each record, so that a crash leaves a valid prefix.
3. **fsync.** While it records, a writer forces each live file to disk about once a second. The
   spec fixes the interval after its cost is measured.
4. **Stray temporary files.** A reader ignores a `.tmp` file and reports it.
5. **Crashed files, read in place.** A reader reads an unfinished file in place and reports it as
   unfinished. It reads each complete record in file order, and it checks that the read reached a
   clean end, because a streaming reader can stop at a torn tail with no error. A record that is
   not complete ends the read. Its bytes count in `torn_bytes`.
6. **CRC checks.** A reader checks the CRC of each CSV row and each journal record that it reads. A
   wrong CRC makes the file `damaged`, with the reason `crc_mismatch`.
7. **Repair only after the user agrees.** When a program finds an unfinished file of a take that it
   owns, it asks the user: "An incomplete recording was found. Would you like to repair it?" Only
   when the user agrees does it repair the file in place. A repair never rewrites a byte before its
   cut. It appends what a clean end writes, for example the fit and end lines of a CSV, and a record
   of the repair: the number of bytes that it cut and the writer string of the repairing program. A
   reader reports a file with that record as `repaired`.
8. **Interrupted repair.** A repair that stops before its end leaves an unfinished file. A new
   repair starts again from the same cut and gives the same result, except for the count of cut
   bytes.
9. **The repair rebuilds the fit** of a camera from the rows of its CSV.
10. **Windows replace test.** Before the writing rules are final, a desk test kills a writer during
    a replace on Windows and checks that the old or the new file stays complete.

This entry supersedes [ADR-PV6S](PV6S-writing-crash-reading-and-repair.md),
[ADR-T24G](T24G-spec-v1-review-fixes-crash-fit-audio.md) and [ADR-5G42](5G42-gate1-names.md) in
full.
- Item 3 restates PV6S item 5. Item 5 restates PV6S item 6 and T24G item 3, for any file. Item 6
  restates T24G item 2, with row and record CRCs in place of chunk CRCs. Item 7 restates PV6S item 7
  and 5G42 item 1 for any file, with the CSV lines in place of the MCAP summary. Item 8 restates
  T24G items 4 and 6. Item 9 restates [ADR-MG7C](MG7C-fit-segments-by-position.md) item 9.
- PV6S items 1 to 4 and T24G items 1, 5 and 14 (MCAP chunks, compression, schemas) are withdrawn.
- T24G items 7 to 9 and 15 are in [ADR-6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) and
  [ADR-KW3G](KW3G-reader-result-for-the-folder.md). T24G items 10 and 11 are in
  [ADR-92TM](92TM-opus-audio-in-fragmented-mp4.md). T24G item 12 is in
  [ADR-DE9S](DE9S-rotation-in-the-video-csv-header.md). T24G item 13 (the encoder-skip log) is
  replaced in [ADR-VPD9](VPD9-spec-draft-v2-details.md).
- 5G42 item 2 (the audio label) is withdrawn: the audio file has a fixed name. 5G42 item 3 is in
  ADR-92TM. 5G42 item 4 is in ADR-KW3G.
- Items 1, 2, 4 and 10 are new.

## Reason

- A file written whole is either the old or the new file after a crash, never a truncated JSON.
- A live file that is flushed for each record survives a process kill: 1, 37 and 500 of 1, 37 and
  500 rows were kept, for both CSV and binary.
- A replace is atomic only on one drive, and power loss needs the flush to disk before the replace.
  The Windows behaviour is not measured yet.
- The reasons of ADR-PV6S stay: a repair changes the user's file, so the user decides.

## Evidence

skellycam `dom/research` (local, not committed):
- `research/skellycam_recording/recording_upgrade/results/crash_resilience/sidecar_durability.md`;
- `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`, "Grilling log": round 2
  Q15; round 3 Q9.

## Open work

[open-work.md](../open-work.md)
