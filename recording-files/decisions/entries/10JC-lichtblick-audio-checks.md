# 10JC — Audio checks in Lichtblick use an offline build of mrkbac/lichtblick at a pinned commit, at 1x only

**Status:** superseded by [92TM](92TM-opus-audio-in-fragmented-mp4.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. Audio checks in Lichtblick use mrkbac/lichtblick at commit
   `70f5900b7a9ecc9b2b223a955615e1abd6220245` (the Audio panel of its PR #116). This is the pinned
   build of [ADR-WD9A](WD9A-lichtblick-reference-viewer.md) item 4.
2. The build is made with its server address emptied, and it runs offline. It must not contact any
   server.
3. The check picks the Opus topic by hand in the panel settings and sets 48000 Hz.
4. Audio checks run at 1x only.
5. Lichtblick is for listening and visual checks. A/V sync is judged in the skellycam player.
6. A fix to Lichtblick, or a contribution upstream, needs a separate approval of the user.

## Reason

- In the desk test, the Opus audio of that build played correctly at 1x. It broke at 0.5x, at 2x
  and after pause and resume, because Chrome rewrites the decoder output timestamps and the panel
  schedules by them.
- The build called a third-party server (`licht-server.marko.im`) on load. Its build bakes in a
  default API address.
- The panel does not auto-select `foxglove.CompressedAudio`. Its default is 16 kHz.
- It plays about 200 ms behind the playhead by design, so it cannot judge sync.

## Evidence

- skellycam `dom/research` (local commits, not pushed):
  - `research/skellycam_recording/recording_upgrade/results/lichtblick_check/FINDINGS.md`;
  - `research/skellycam_recording/docs/mcap_profile_decisions_20261113.md` (Q19).

## Open work

[open-work.md](../open-work.md)
