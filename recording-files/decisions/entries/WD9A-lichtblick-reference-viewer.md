# WD9A — Lichtblick is the external test viewer; VLC compatibility is dropped

**Status:** superseded by [92TM](92TM-opus-audio-in-fragmented-mp4.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. Lichtblick (https://github.com/lichtblick-suite/lichtblick) is the external reference viewer for
   tests of the format. A golden file and a test recording must open in it.
2. Foxglove is not the reference viewer.
3. VLC compatibility is not a requirement of the format. No rule of the spec exists only so that VLC
   can play a file.
4. Released Lichtblick has no Audio panel. Until it has one, an audio test in a viewer uses a
   Lichtblick build with an Audio panel, pinned to one commit. The spec or the test names the build.

## Reason

- The user chose Lichtblick. It is open source (MPL-2.0) and it runs in a browser or as a desktop
  app on Linux, Windows and macOS. Foxglove ended open-source development with Foxglove 2.0.
- The format is an MCAP profile ([ADR-SFK5](SFK5-mcap-container.md)). VLC does not read MCAP.

## Evidence

- Lichtblick v1.30.0 (2026-10-22) has no Audio panel and no audio code. Upstream PR #1301 (open)
  and mrkbac/lichtblick PR #116 (merged in that copy at commit
  `70f5900b7a9ecc9b2b223a955615e1abd6220245`) add one: skellycam `dom/research`,
  `research/skellycam_recording/docs/mcap_check_20261113.md` (local commit, not pushed).

## Alternatives rejected

- Foxglove: closed source since Foxglove 2.0.
- VLC: it does not read MCAP.

## Open work

[open-work.md](../open-work.md)
