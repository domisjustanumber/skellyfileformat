# WD1R — File, attachment and MIME names: `.skvt` and `.skat`

**Status:** superseded by [SFK5](SFK5-mcap-container.md), 2026-11-13 (commit to main; was accepted, 2026-11-12).

## Decision

1. The video timing sidecar has the magic `SKVT` and the extension `.skvt` ("video timing"). The
   audio timing sidecar has the magic `SKAT` and the extension `.skat` ("audio timing").
2. The attachment names are `video_timing.skvt` and `audio_timing.skat`. The attachment media types
   are `application/x-skellyfileformat-video-timing` and
   `application/x-skellyfileformat-audio-timing`. A reader matches an attachment by its name and its
   media type together.
3. A separate sidecar is named `<stem>.skvt` or `<stem>.skat`, where `<stem>` is the name of its
   media file without the last extension. The live audio sidecar is `<stem>.skat.live`, with the
   stem of the `.flac` file. While the writer records, it writes one live audio sidecar, which holds
   the timing records and the packet records in the order that it writes them.
4. The recording manifest is `<rec>.skellyrec.json`.
5. The spec fixes no other file names. The media file names and the folder names belong to the
   writer (skellycam's own spec).
6. The audio timing sidecar that [ADR-CA03](CA03-flac-audio.md), [ADR-M4DF](M4DF-format-versioning.md)
   and [ADR-VJ14](VJ14-shared-package-and-spec.md) call `.skau` is the `.skat`. This is the naming
   that ADR-VJ14 item 5 gives to the spec. It changes no other rule of those entries.

## Reason

- The names are brand-neutral. skellysync and the skellycam converter also write these files, so a
  name with "skellycam" in it is wrong.
- `.skvt` and `.skat` are a pair, and each is equal to its 4-byte magic.
- One live audio sidecar, not two, gives one file fewer while the writer records. The writer already
  writes both kinds of record in one loop, and one file keeps their order.
- Media file names are part of the contract between skellycam and freemocap, which waits for phase 2
  of the skellycam plan.

## Alternatives rejected

- `.skfr` ("skellycam frames") and `.skau` ("skellycam audio"), the prototype names: they name
  skellycam, and they are not a pair.
- Two live audio files (timing and packets): one more file, and recovery must match two files.
- `vnd.` media types: they need an IANA registration.

## Open work

[open-work.md](../open-work.md)
