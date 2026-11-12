# VJ14 — One shared package with a descriptive spec

**Status:** accepted, 2026-11-12 (user; backfilled from the skellycam plan rev 3.8).

## Decision

1. The format code is in one shared package: skellyfileformat. The skellycam plan first named it
   `skellyformat`.
2. The package holds the record codecs (the video timing sidecar, the `.skau` and the audio packet
   table), the MKV scanner, the appender, the JavaScript reader and locator, and the golden files.
3. An optional write layer, `skellyfileformat[write]`, holds the decoder, the JPEG encoder choice,
   the MKV writer and the finaliser. The skellycam recorder, the skellycam converter and skellysync
   use it.
4. The package has a detailed descriptive spec: the byte layouts, the field meanings, the clocks,
   the finalisation and recovery rules, the versioning and the test vectors. Another program can
   implement the format from the spec alone.
5. The spec fixes the file, attachment and MIME names.

## Reason

- Three programs write or read the format. One implementation stops them from becoming different.
- A spec lets other programs read the files without the code of this package.

## Evidence

- Plan rows S5, S6, D17 and D23 ([plan](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/CAPTURE_AND_RECORDING_PLAN.md)). The skellycam plan and its evidence are on the `dom/research` branch of the skellycam fork. That branch is not force-pushed, so the permalinks stay valid.
- skellysync decision D-PKG ([SCOPE](https://github.com/domisjustanumber/skellycam/blob/a65e540053073c58f01ef2c8c8297901f6d9517f/research/skellysync_jpeg/SCOPE.md)).
