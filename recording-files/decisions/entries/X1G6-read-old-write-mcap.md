# X1G6 — Old recordings stay readable; new skellycam and skellysync write only the MCAP profile

**Status:** superseded by [CZQ9](CZQ9-read-old-write-new-and-legacy-recognition.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. New skellycam and freemocap keep reading each recording format that the current code writes.
2. New skellycam and skellysync write only this format: MCAP files with JPEG video
   ([ADR-SFK5](SFK5-mcap-container.md)) and Opus audio ([ADR-HD8Z](HD8Z-opus-audio.md)).
3. A recording with no file of this format is a legacy recording. The spec defines how a reader
   recognises a file of this format.
4. skellycam plays old H.264 recordings through a legacy `<video>` path. It also gives an explicit
   "upgrade recording" conversion, for the other old files and on request.
5. skellycam owns the converter. The converter uses `skellyspecs[write]`.
6. This spec covers only the new format. skellycam defines how it reads legacy recordings.

This entry supersedes [ADR-X7FT](X7FT-read-old-write-new.md) in full. Items 1 and 4 to 6 restate
its items 1 and 4 to 6. Item 2 replaces "JPEG in MKV with skellyspecs sidecars, and FLAC
audio". Item 3 replaces "no skellyspecs sidecar" with "no file of this format".

## Reason

- The reasons of ADR-X7FT stay: users keep their old recordings, and a program that writes two
  formats doubles the test work.
- The write format changed to MCAP with Opus ([ADR-SFK5](SFK5-mcap-container.md),
  [ADR-HD8Z](HD8Z-opus-audio.md)).

## Open work

[open-work.md](../open-work.md)

_Edited 2026-11-23 (commit to main): rename._
