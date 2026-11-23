# W4PF — One shared package with a descriptive spec; no recorded overlays (consolidation)

**Status:** superseded by [2C9V](2C9V-whole-take-folder-scope-and-package.md), 2026-11-16 (commit to main; was accepted, 2026-11-13).

## Decision

1. The format code is in one shared package: skellyspecs. The skellycam plan first named it
   `skellyformat`.
2. The package holds the spec, the conformance test list, the golden files, a Python reader and
   writer, and a JavaScript reader. An optional write layer, `skellyspecs[write]`, holds the
   writer. The skellycam recorder, the skellycam converter and skellysync use it.
3. The package has a detailed descriptive spec: the channels, the field and key meanings, the
   clocks, the rules for unfinished and repaired files, the versioning and the test vectors.
   Another program can implement the format from the spec and the MCAP specification alone.
4. The spec fixes its own names: the profile, the topics, the Metadata records and keys, and the
   Log names. It fixes no file or folder names
   ([ADR-DK8S](../../recording-files/decisions/entries/DK8S-mcap-profile-files-and-names.md) item 12).
5. skellycam records no overlays. It removes the burned-in `camera.id…fr{N}` stamp from the frames.
6. The format has no overlay file, channel or attachment. `.skov` is not part of the format.
7. The player draws the frame label from the fields of the frame in the file.
8. Recorded overlay data from freemocap is later work. The spec will document it if it comes.

This consolidation entry supersedes
[ADR-VJ14](VJ14-shared-package-and-spec.md) and [ADR-5K7G](../../recording-files/decisions/entries/5K7G-no-recorded-overlays.md) in full.
It changes no decision. Items 1 and 3 restate VJ14 items 1 and 4, without the MKV byte layouts.
Item 2 restates VJ14 items 2 and 3 without the MKV parts that the move to MCAP removed (skellycam
plan D27). Item 4 restates VJ14 item 5 as ADR-DK8S item 12 changed it. Items 5, 6 and 8 restate
5K7G items 1, 2 and 4. Item 7 restates 5K7G item 3, with "the fields of the frame in the file" in
place of "the sidecar".

## Reason

- Three programs write or read the format. One implementation stops them from becoming different.
- A spec lets other programs read the files without the code of this package.
- The stamp was a visual workaround for out-of-sync `<video>` playback
  ([skellycam commit c4b64f5](https://github.com/freemocap/skellycam/commit/c4b64f5f36ede13f12a8409cd9a2886666d7b5a3)).
  No code reads it from the pixels, and the file holds each value that the stamp shows.
- The spec v1 review found that ADR-VJ14 items 2, 3 and 5 and ADR-5K7G item 3 still described the
  MKV and sidecar design. The absorb step needs entries that the spec can state.

## Evidence

- Plan rows S5, S6, S7, D17, D18, D23 and D27 of the skellycam plan, and skellysync decision D-PKG
  ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md),
  [SCOPE](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellysync_jpeg/SCOPE.md)).
  D27 is in the local, unpushed `dom/research` commits.
- skellycam `dom/research` (local commit, not pushed):
  `research/skellycam_recording/docs/spec_v1_review_20261113.md` (S11).

## Alternatives rejected

- `.skov`: a prototype from the overlay study, not a standard.
- SVG overlays: 11 times the size, not safe after a crash, and it stores drawings, not data.

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
