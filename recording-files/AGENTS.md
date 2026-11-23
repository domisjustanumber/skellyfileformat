# recording-files: module instructions

The rules of the root [`AGENTS.md`](../AGENTS.md) also apply. This file adds the rules of this
module ([ADR-YYP7](../decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 2).

## 1. Purpose

This module defines the skellyspecs recording format: the take folder of skellycam, skellysync and
freemocap recordings. It covers MJPEG in MKV and Opus in fragmented MP4, each with a CSV timing
sidecar, and every folder file that the programs add
([ADR-2C9V](../decisions/entries/2C9V-whole-take-folder-scope-and-package.md),
[ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md),
[ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md)). It holds the normative spec,
the conformance test list, the golden folders and the runnable conformance tests. It holds no reader
and no writer. skellycam, skellysync, freemocap and the Blender addon each implement the format in
their own repository. Each of them runs the conformance tests against its own code through a test
adapter ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).

| Path | Role |
|---|---|
| `README.md` | Normative: the scope, the compatibility promise, the versioning and what "conforming" means |
| `SPEC.md`, `parts/` | Normative: the spec |
| `conformance.md` | Normative: the conformance test list |
| `legacy-annex.md` | Informative ([ADR-VPD9](decisions/entries/VPD9-spec-draft-v2-details.md)) |
| `golden/` | The golden folders of SPEC.md Appendix A, each with its `SHA256SUMS` and its expected reader results ([`README.md`](golden/README.md)). `tools/make_golden.py` makes them ([ADR-G21H](decisions/entries/G21H-gate-2-tests-location-and-interfaces.md)). |
| `tests/conformance/` | The runnable conformance tests of `conformance.md`. They reach an implementation through its test adapter. They are not in the default pytest run. |
| `decisions/` | The decision log of this module ([`README.md`](decisions/README.md)) and its open work ([`open-work.md`](decisions/open-work.md)) |

## 2. Test

Run `uv run --group conformance pytest recording-files/tests/conformance` to run the conformance
tests. They need the test adapter of an implementation. With no adapter, each test that calls a
reader or a writer fails with one line
([conformance.md, "The test adapter"](conformance.md#the-test-adapter)).
Add `-m stage1a` to run only the tests with the mark `stage1a`. The other marks are `stage1b`,
`stage2`, `stage3` and `stage4`. A mark is a label, not a build stage ([section 3](#3-project-rules)).
Run `uv run --group golden python tools/make_golden.py --check` to check the golden files against a
new run of the generator.

## 3. Project Rules

- `README.md`, `SPEC.md` and `conformance.md` of this module are normative.
- A change to a file of the take folder needs a change of the spec first. The owner of the
  repository must approve it. The `RECORDING_CONTRACT.md` of freemocap points to the spec for the
  folder ([ADR-2C9V](../decisions/entries/2C9V-whole-take-folder-scope-and-package.md) item 4).
- Write the spec first. Do the work for each part of the format in this order:
  1. Write the spec text and the conformance test list.
  2. Stop. The user reviews them (gate 1).
  3. Write the runnable tests and the golden files. The tests fail here, because this repository
     has no implementation.
  4. Stop. The user reviews them (gate 2).
- Do not write a reader, a writer or other implementation code for this format. Each implementing
  repository writes its own code and plans its own build order. It runs the conformance tests of a
  pinned commit of this repository through its test adapter
  ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md)).
- Each test has a mark: `stage1a`, `stage1b`, `stage2`, `stage3` or `stage4`. A mark is a label. It
  tells which program and which need a test serves. It is not a build stage
  ([ADR-YBT1](../decisions/entries/YBT1-spec-only-test-adapter-and-labels.md) item 4).
  The section [The stage of each test](conformance.md#the-stage-of-each-test) gives the mark of
  each test and each golden folder.
- The user approves gate 2 for the tests and the golden folders of each mark. The review of a mark
  covers only its tests and golden folders. The user reviews a later mark when its program needs it
  ([ADR-CPM2](decisions/entries/CPM2-stages-of-the-implementation.md) item 1).
- The user approved gate 2 for stage 1, the marks `stage1a` and `stage1b`
  ([ADR-N1AM](decisions/entries/N1AM-gate-2-approval-of-stage-1.md)). The tests of `stage1b`
  (SFT-760 and G17) are provisional: they wait for the skellysync decisions
  ([open-work.md](decisions/open-work.md)). The user has not approved gate 2 for `stage2`, `stage3`
  and `stage4`.
- The approval does not cover the provisional points that wait for a desk test or a hardware test.
  For these, an implementation writes only the provisional behaviour that the spec gives now
  ([ADR-Z641](decisions/entries/Z641-program-guidance-gate-2-scope-and-no-push.md) item 2).
- When the freemocap exporter and the Blender addon are ported, this module accepts their output as
  golden files of the marks `stage3` and `stage4`. It also keeps the spec text correct.
- Each requirement in `SPEC.md` has an ID `SFF-NNN`. Each test in `conformance.md` has an ID
  `SFT-NNN` and cites the SFF IDs that it checks.
- Give a new requirement or test the next free number. Do not reuse or renumber an ID.
- Mark a removed requirement or test "withdrawn". Do not delete its ID.
- `tools/check_spec_traceability.py` checks the IDs and the links between requirements and tests.
- Commit each golden file in `golden/` with its SHA-256 sum and the script that made it.
- A change to a golden file needs a decision entry.

## 4. Decision Log

Read [`decisions/README.md`](decisions/README.md) and [`open-work.md`](decisions/open-work.md) of
this module before you change a file of this module. The root
[section 5](../AGENTS.md#5-decision-log) gives the rules of each log.
