# YYP7 — skellyspecs: one repository for the freemocap specs, module logs and one licence

**Status:** accepted, 2026-11-23 (user; questions Q1 to Q14 of the owner session of this
repository, which confirm the rulings Q105, Q108 and Q110 to Q122 of a skellytracker session).

## Decision

1. **Name.** The repository is `skellyspecs`. The name `skellyfileformat` is replaced by
   `skellyspecs` wherever it appears. [ADR-6PNN](6PNN-format-field-skellyspecs.md) gives the change
   of the format. The IDs `SFF-NNN` and `SFT-NNN` keep their prefix.
2. **Folders.** The repository holds four spec folders at its root. Each folder is a module with its
   own `AGENTS.md` and `CLAUDE.md`, and its log is at `<folder>/decisions/`.
   - `recording-files/`: the take-folder spec, its conformance list, its golden folders and its
     conformance tests (before: `spec/`, `golden/`, `tests/conformance/` and the normative sections
     of `README.md`).
   - `tracker-pipelines/` and `model-sidecars/`: the pipeline spec and the model sidecar spec of
     skellytracker, with their module logs.
   - `exporter-guide/`: the exporter guide of skellytracker. It comes only after an exporter test
     run passes.
   - The tools stay in the root `tools/`, with their tests in `tools/tests/`. The skills are in the
     root `.claude/skills/`.
3. **Implementation code.** This rule replaces "it holds no reader, no writer and no other
   implementation code" of `AGENTS.md`. The repository holds no reader and no writer of a format
   that a program implements. For `recording-files/`, [ADR-YBT1](YBT1-spec-only-test-adapter-and-labels.md)
   item 1 stays. A spec folder can hold reference modules when its spec makes them part of the
   spec. Its `AGENTS.md` names them. No tool, test or reference module imports a package of another
   repository.
4. **Entry placement.** An entry goes in the log of a module when its decision affects only that
   module. A root tool that only that module uses counts as part of the module. An entry with a rule
   for the repository or for two or more modules goes in the root log. Each existing entry moves by
   this rule.
5. **Rename edit.** The Rules allow a fifth edit of a decided entry: the one-time replacement of
   `skellyfileformat` by `skellyspecs`, with the edit kind `rename`.
6. **One licence.** Apache-2.0 applies to each file. The CC-BY-4.0 licence of the spec text ends
   ([ADR-CD4G](CD4G-spec-first-and-repository-rules.md) item 5), and `spec/LICENSE` goes.
7. **Import from skellytracker.** The two specs come as a copy, not as a history split. The copy
   comes from one pushed skellytracker commit, after its change to LF line ends, and the import entry
   records that commit. A script of the import entry rewrites each link that leaves the two folders.
   A link to an entry of the skellytracker root log becomes the plain text `skellytracker ADR-<ID>`.
   The full-SHA links come in one later commit, after that log is on the skellytracker default
   branch. The proposal records of `model-sidecars/proposals/` stay byte copies. The skills
   `author-sidecar`, `propose-sidecar-change`, `change-sidecar-spec` and `change-pipeline-spec` come
   in two commits: the copy, then a port to the rules of this repository.
8. **What stays in skellytracker.** `intakes/`, the parity files of real models, the
   implementation plan and the package code. The tool `intake_bundle.py` moves without its package
   parts, and its `--root` is required, with no default. One made-up sample parity file goes to
   `model-sidecars/examples/parity/`. The lead copy of the sidecar normalizer is a reference module
   here. A skellytracker test keeps the package copy equal to it.
9. **Versions and pins.** The two skellytracker specs keep the skellytracker spec version
   (skellytracker ADR-6GE2). The format version of `recording-files/` covers only that folder.
   skellytracker pins one commit of this repository and reads the sibling checkout `../skellyspecs`.
   A spec change lands here first.

## Reason

- The user wants all the freemocap specs in one repository that the programs pin.
- One licence has no line between prose and code. The moved specs mix both. Apache-2.0 also gives a
  patent grant to the implementers.
- A module log keeps the read path of each spec short.

## Evidence

- Authors (git, skellytracker at abec9a06, the moving paths): one author name, the user's, in 106
  commits. The older history has one commit of a second contributor on the ancestor of the sidecar
  spec. 2 of its 28 added lines are in the moving files, and both are trivial (a heading and a
  folder-tree comment). The script `match_lines.py` of the skellytracker session found them by exact
  match after a whitespace change.
- Three node modules name AGPL package code as their source. With each identifier replaced by one
  placeholder, they share 0, 3 and 1 generic statements of 55, 62 and 114 with that code. The user
  accepted this as a re-implementation (Q5).
- This repository: one author name in 96 commits.

## Alternatives rejected

- A history split of skellytracker: its history stays readable there.
- A dependency on the skellytracker package: the two repositories would depend on each other.
- A default `--root` of `../skellytracker/intakes`: a tool here would hold a path of another
  repository.
- CC-BY-4.0 for the spec text, kept: see Reason.
- `skellyfileformat` kept in the recorded files: the user wants one name. No file outside the
  machine of the owner holds it.

## Open work

See [open-work.md](../open-work.md).
