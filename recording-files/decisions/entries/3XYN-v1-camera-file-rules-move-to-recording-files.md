# 3XYN — The reading rules of v1 camera files move to recording-files

**Status:** accepted, 2026-11-25 (user; answers Q743, Q765 and Q798 of the owner session of 2026-11-25, with the rule content of his answers Q738, Q740 and Q741 of the same session).

## Decision

1. **Q743 (session Q15).** The owner put the v1 playback rules in skellyspecs ("in skellyspecs, and
   yes"). The player spec of skellycam stays its own file, `specs/player-legacy.md`, linked from
   section 1.3 of the 6a player spec, as the v1 part of step 6c.
2. **Q765 (session Q37), option B: split.** The rules of the v1 files go into this module, because
   freemocap and skellysync also read v1 files: the time map, the folders that a reader refuses and
   the frame table. The behaviour of the player stays in skellycam: its routes by codec, the WASM
   decoder, the CSP, the secret header and the rule that switches a tile.
3. **Q798 (session Q70).** A spec agent writes the rules on the branch `dom/v1-player-rules`. The
   normative rules go into SPEC.md section 21. The background goes into the legacy annex. The
   entries go into the log of this module. `specs/player-legacy.md` of skellycam links to the rules
   by a pinned commit. Nothing is pushed without a yes of the owner.
4. **The rule content.** The owner accepted these answers of the skellycam spec on the same day.
   This module states them for each reader:
   - **Q738 (session Q10; spec Q711), the time map.** The time of a frame is the mean of the time
     files of the cameras, from the base time, and it never decreases. With no usable time file,
     the median header rate gives the time, and the time is marked as an estimate. A gap in the
     capture plays as a gap in real time.
   - **Q740 (session Q12; spec Q713), the other eras.** A reader refuses a v2 alpha folder with a
     clear message. A reader does not refuse a v0.1.0 folder, but it gets no test and no support.
   - **Q741 (session Q13; spec Q714), the demuxer.** The WASM route of skellycam uses FFmpeg's own
     demuxer in the worker. The TypeScript MP4 reader of skellycam makes the frame table and picks
     the route, with a cross-check between the two at open. This module states the frame table.
     The choice of the demuxer and of the route stays in skellycam.
5. **Scope.** The spec now gives the rules to read the camera files and the time files of a v1
   folder, in addition to the recognition of SFF-875 to SFF-880. The code that reads the old files
   stays in skellycam and freemocap
   ([ADR-YBT1](../../../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).

## Reason

- One rule for each v1 file, in the place where each program that reads it can pin it.
- skellyspecs holds shared formats and no internals of a program.

## Consequences

- The rules are a draft for gate 1. Each program implements them after gate 2.
- skellycam's `specs/player-legacy.md` replaces its own text of these rules with a link to a pinned
  commit of this repository.

## Evidence

The owner session of 2026-11-25, rounds 1, 2 and 5 (skellycam, local and not committed). The rules
come from skellycam `dom/legacy-player`, `specs/player-legacy.md`, revision 5, sections 2, 3.7 and
6 (commit c0d61ee107c3c5b9ad203be09bccd21c8dcf619b).

## Alternatives rejected

- Option A (Q765): the whole `player-legacy.md` as a new module here. One player would then be
  specified across two repositories.
- Option C (Q765): each skellycam spec moves here. This repository holds no internals of a program.

## Open work

[open-work.md](../open-work.md)
