# YBT1 — A spec only: no package, a test adapter for each implementation, marks as labels, Python 3.13.18

**Status:** superseded by [46NQ](46NQ-old-recordings-play-as-they-are-no-upgrade-converter.md), 2026-11-25 (commit on dom/v1-player-rules; was absorbed into
[`README.md#scope-normative`](../../recording-files/README.md#scope-normative),
[`README.md#compatibility-promise-normative`](../../recording-files/README.md#compatibility-promise-normative),
[`README.md#versioning-normative`](../../recording-files/README.md#versioning-normative),
[`README.md#implementations`](../../recording-files/README.md#implementations),
[`README.md#licenses`](../../README.md#licenses),
[`recording-files/AGENTS.md#1-purpose`](../../recording-files/AGENTS.md#1-purpose),
[`recording-files/AGENTS.md#2-test`](../../recording-files/AGENTS.md#2-test),
[`recording-files/AGENTS.md#3-project-rules`](../../recording-files/AGENTS.md#3-project-rules),
[`AGENTS.md#6-git-rules`](../../AGENTS.md#6-git-rules),
[`AGENTS.md#8-private-data`](../../AGENTS.md#8-private-data),
[`spec/SPEC.md#skellyspecs-recording-format-specification`](../../recording-files/SPEC.md#skellyspecs-recording-format-specification),
[`spec/parts/parquet-descriptor.md#structure-rules-and-writer-rules`](../../recording-files/parts/parquet-descriptor.md#structure-rules-and-writer-rules),
[`spec/legacy-annex.md#legacy-annex-freemocap-v1x-recording-folders-informative`](../../recording-files/legacy-annex.md#legacy-annex-freemocap-v1x-recording-folders-informative),
[`spec/conformance.md#skellyspecs-recording-format-conformance-tests`](../../recording-files/conformance.md#skellyspecs-recording-format-conformance-tests),
[`golden/README.md#golden-folders`](../../recording-files/golden/README.md#golden-folders),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; decisions D1 to D6 of a planning
session of skellycam; an agent wrote the restatements))).

## Decision

The user wrote on 2026-11-17: "skellyspecs must just be a spec, implementation is up to the
respective repos". The user accepted these items.

1. **Spec only (D1).** This repository holds no reader, writer, converter, repair tool or
   JavaScript reader. There is no Python package `skellyspecs` and no `skellyspecs[write]`.
   skellycam, freemocap, skellysync and the Blender addon each implement their own reading and
   writing. skellycam owns its Python writer (MKV, CSV sidecars, Opus fMP4, manifest, capture info
   JSON), the crash repair, the opening of a folder with the recognition of old formats, the
   "upgrade recording" converter and a JavaScript reader in skellycam-ui.
2. **What stays (D2).** The spec, `spec/conformance.md`, the golden folders and the runnable tests
   in `tests/conformance/`, the executable form of the conformance list. The tests reach an
   implementation through one configurable seam. Each implementing repository writes a thin test
   adapter and runs this suite at a pinned commit against its own code.
3. **The adapter interface (D3).** The names that the tests call are what a test adapter exposes,
   not a product API: `read_folder`, `canonical_json`, the detail functions, `TakeWriter` and its
   methods, `repair_take`, `release_check`, and the JavaScript command that writes the `player`
   result to standard output. The code behind an adapter can have any form. The argument shapes
   that the tests assume stay undecided.
4. **No build stages here (D4).** The build stages, the end of a stage, the build order, the
   adoption by a program before the next stage, and the limits of stage 1 are removed. Each
   implementing repository plans its own build. The marks `stage1a` to `stage4` keep their names.
   They are labels: a mark tells which program and which need a test serves.
5. **No tests of a staged package (D5).** The two tests of the package in the staged build are
   dropped. With no package, they have no subject.
6. **Python 3.13.18 (D6).** The pins move from 3.13.13 to 3.13.18: the golden bytes do not change
   (Evidence). The sample text "3.13.13" in the golden Parquet descriptors stays.

This entry supersedes ADR-2C9V, ADR-CPM2, ADR-YT1F, ADR-N1AM, ADR-Z641, ADR-G21H, ADR-0JVZ,
ADR-QH61 and ADR-CZQ9 in full, because items 1 to 4 change a rule of each.

**Kept rules.** Each heading states the rules of the items on its line, as changed here.

- README [Scope](../../recording-files/README.md#scope-normative) and
  [Compatibility](../../recording-files/README.md#compatibility-promise-normative): 2C9V 1; CZQ9 1, 2, 5.
  [Licenses](../../README.md#licenses): 2C9V 12.
- AGENTS.md [2](../../recording-files/AGENTS.md#2-test): G21H 1, 9.
  [3](../../recording-files/AGENTS.md#3-project-rules): 2C9V 4, 8 to 11, 13, 14; CPM2 1, 9; N1AM 1; Z641 2; G21H 9.
  [6](../../AGENTS.md#6-git-rules), [8](../../AGENTS.md#8-private-data): 2C9V 12; N1AM 4; Z641 3.
- [SPEC.md](../../recording-files/SPEC.md#skellyspecs-recording-format-specification): 2C9V 2, 3, 7, by its sections 1,
  2, 6, 16, 18.1, 18.4 and Appendix B; N1AM 1. [§3](../../recording-files/SPEC.md#3-versioning),
  [Appendix A](../../recording-files/SPEC.md#appendix-a-golden-folders): 0JVZ 20, 22; QH61 46, 47.
  [§8](../../recording-files/SPEC.md#8-video-timing-sidecar), [§17](../../recording-files/SPEC.md#17-realtime-journal):
  Z641 1. [§21](../../recording-files/SPEC.md#21-legacy-folders) and the
  [legacy annex](../../recording-files/legacy-annex.md#legacy-annex-freemocap-v1x-recording-folders-informative):
  CZQ9 1, 3 to 10. [§23](../../recording-files/SPEC.md#23-the-reader-result): 2C9V 6; 0JVZ 21.
- [conformance.md](../../recording-files/conformance.md#skellyspecs-recording-format-conformance-tests): N1AM 1; QH61 46,
  47. [The test adapter](../../recording-files/conformance.md#the-test-adapter): G21H 2, 3, 4, 8; 0JVZ 21.
  [The stage of each test](../../recording-files/conformance.md#the-stage-of-each-test): CPM2 3 to 6, 8, 9,
  11, 13, 14; YT1F 1 to 7; Z641 2.
- [golden/README.md](../../recording-files/golden/README.md#golden-folders): G21H 5, 6, 7, 10; D6.

**Changed rules.** Each absorb document cites this entry next to the changed rule.

- 2C9V 5 and 6, CZQ9 4, G21H 4: item 1. The scopes `full` and `player` stay rules of a reader. The
  converter of skellycam uses its own writer.
- 2C9V 8: the gate steps of this repository end at gate 2.
- CPM2 2, 7, 10, 12 and 14 (the "not in this version" error and the refusal), N1AM 2 and 3, Z641 4:
  removed. Each other item of CPM2 and YT1F, and Z641 2, gives a mark, not a build stage.
- YT1F 1: a person runs the Blender check of SFT-711 by hand one time. YT1F 2: the converter cases
  run through `TakeWriter` of the adapter, in a conversion.
- G21H 1: with no adapter, each test that calls an implementation fails with one line. G21H 2, 3
  and 8, 0JVZ 21 and QH61 46: the names and the JavaScript command are those of the adapter (item
  3). The detail functions of the adapter give the stored bytes, and the tests decode with PyAV.
- Other entries that say "the reader of this package" keep their rules, now said of "a reader".

## Reason

- The user wants one spec, and the code in the programs that use it.
- A build order is a plan of the program that builds.

## Consequences

- The agent choices for the seam (the variables and the JavaScript adapter) are in [ADR-K4Y1](../../recording-files/decisions/entries/K4Y1-test-adapter-seam-choices.md). The user accepted them on 2026-11-17.

## Evidence

- Python 3.13.18: release date 2026-10-25 (python.org), 23 days before this entry. uv 0.13.7 has
  `cpython-3.13.18+20261026` for Windows x86-64.
- With Python 3.13.18 and the pinned group `golden` (av 19.0.2, numpy 2.4.6, pillow 13.0.0, pyarrow
  26.0.0), `uv run --group golden python tools/make_golden.py --check` gave "the same" for G01 to
  G16 on Windows x86-64. G17 is not built.

## Alternatives rejected

- A copy of the tests in each implementing repository: the copies drift (the user accepted this
  recommendation).

## Open work

See [open-work.md](../open-work.md).

_Edited 2026-11-23 (commit to main): link repair._

_Edited 2026-11-23 (commit to main): rename._
