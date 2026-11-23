# Repository Instructions

All new and changed documentation must use ASD-STE100 Simplified Technical English.
This rule applies to `AGENTS.md`, skills, decision entries and templates.
Use short sentences. Use active voice. Use one instruction per sentence.
Use "must" for a requirement.
Keep technical names, field names, values, formulas, code and YAML unchanged.

## 1. Purpose

skellyspecs holds the specs of the freemocap programs [ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md). Each spec is a module: a folder with
its own `AGENTS.md`, its own decision log and its own conformance material. skellycam, skellysync,
freemocap, skellytracker and the Blender addon each implement a spec in their own repository. Each
of them pins a commit of this repository and runs its tests against its own code. Other programs
can implement a spec from its text alone.

| Path | Role |
|---|---|
| `AGENTS.md` | The root instructions file for coding agents |
| `CLAUDE.md` | Imports this file. It has no other content. Each module has the same `CLAUDE.md`. |
| `README.md` | The list of the specs, the license and the development steps |
| `recording-files/` | Module: the take folder of skellycam, skellysync and freemocap recordings ([`AGENTS.md`](recording-files/AGENTS.md)) |
| `tracker-pipelines/` | Module: the tracker pipelines of skellytracker. Not imported yet. |
| `model-sidecars/` | Module: the model sidecars of skellytracker. Not imported yet. |
| `exporter-guide/` | Module: the guide for model exporters. It comes after an exporter test run passes. |
| `decisions/` | The root decision log ([`README.md`](decisions/README.md)) and its open work ([`open-work.md`](decisions/open-work.md)): the decisions for the whole repository |
| `tools/` | Each tool of each module, with its tests in `tools/tests/`: the doc checks `check_decision_log.py`, `check_links.py`, `check_private_data.py`, `check_ai_attribution.py` and `check_spec_traceability.py`, and `make_golden.py` with `goldgen/` |
| `.claude/skills/` | The skills. Git tracks this folder. |
| `plans/` | A local working folder. Git ignores it. |

## 2. Skills

Load the skill that matches the task.
If your agent does not support skills, read the file `.claude/skills/<skill>/SKILL.md`.
The rules in this file also apply.
Git tracks `.claude/skills/` and ignores the rest of `.claude/`.
The root `AGENTS.md` and the `AGENTS.md` of each module are the only instruction files. Each
`CLAUDE.md`, also in a module, holds only `@AGENTS.md`. Do not put instructions in a `CLAUDE.md`.

This repository has no skills yet.

## 3. Install and Test

Run `uv sync`.
Then run `uv run pre-commit install` once in the clone ([section 8](#8-private-data)).
It installs the pre-commit hooks, the commit-msg hook and the pre-push hook.
Run it again in each clone after `.pre-commit-config.yaml` changes.
Use `uv run` for project commands.
Do not depend on an activated virtual environment.

Run `uv run pytest`.
These tests must pass.
Run `uv run pytest tools/tests` to run only the doc checks.
The doc checks test the decision logs, the relative links, the private-data rule and the links
between the spec requirements and the conformance tests.
The `AGENTS.md` of each module gives the commands for its conformance tests and its golden files.
Report each new test failure to the user.
Fix the failures of one root cause in one PR.

## 4. Project Rules

- The `AGENTS.md` of each module names its normative documents. Code must agree with them.
- A change to a rule in a normative document needs a decision entry.
- This repository holds no reader and no writer of a format that a program implements [ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 3.
  A module can hold reference modules when its spec makes them part of the spec. The `AGENTS.md`
  of the module names them.
- No tool, test or reference module imports a package of another repository.
- A spec change lands here first. A program then moves its pin to the new commit.
- Each file has the license Apache-2.0 ([LICENSE](LICENSE), [ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 6).
- A bug fix needs a test that fails before the fix.
- Pin each dependency, tool, toolchain and CI action to an exact version. Use a release that is at
  least 14 days old.
- Do not change code that your task does not need.

## 5. Decision Log

Read [`decisions/README.md`](decisions/README.md) and
[`open-work.md`](decisions/open-work.md) before you change a spec, the README, the golden files,
the tools or these instructions.
For a task in a module with a log, also read the `decisions/README.md` and the
`decisions/open-work.md` of that module. The `AGENTS.md` of the module links to its log.
An entry goes in the log of a module when its decision affects only that module. A root tool that
only that module uses counts as part of the module ([ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 4).
All other entries go in the root log: an entry with a rule for the repository or for two or more
modules, and each case that you cannot decide.
A new module log needs the approval of the user. The PR that adds it also adds its folder to
`LOG_DIRS` of `tools/check_decision_log.py`.
Each log has a `README.md` with an Active table, a Proposed table and `## Open work`, a
`historical.md`, an `open-work.md` and its entry files in `entries/`. The Rules and `template.md` are only in the root log.
All logs have one ID space. Do not add a module name to an ID.
When the scope of a module entry grows to more than one module, a new root entry supersedes it.
A tool is code that a test, a hook, a CI job, a skill or a workflow step runs, or code that writes a
tracked file. It is in the root `tools/`, also when only one module uses it. It has tests.
A script made the evidence for an entry or did its one-off job, and the entry names it. It is in
`scripts/` of the log that holds the entry. Its own tests, if any, are in `scripts/tests/`.
A script does not change after its entry is decided. When a step starts to run it, move it to
`tools/` and add a test.
The [Rules](decisions/README.md#rules) of the index give the allowed edits, the status changes and
the other rules that an agent needs and that no tool checks and no loaded document states. `tools/check_decision_log.py` checks the tables, the IDs and the
limits.
Add one entry for each new decision or measurement.
Get its ID from `uv run python tools/check_decision_log.py --new`.
End each commit subject that adds or changes an entry with `(ADR-<ID>)`.
Cite each entry as a Markdown link with `ADR-<ID>` as the link text, in upper case, for example
[ADR-0001](decisions/entries/0001-decision-log-agents-md-and-private-data.md).
This rule applies to each text that you write: a tracked file, a plan, a PR body and a reply to the
user. In a reply or a plan, the path is relative to the repository root or to the file.
A commit message cannot hold a working link. In the commit body, write `ADR-<ID>` with no link.
Cite an entry of another repository with the repository name and `ADR-<ID>`. Also link it with a
full-SHA permalink when the entry is on the default branch of that repository
(see the [Rules](decisions/README.md#rules)).

## 6. Git Rules

- `plans/` is a local working folder. Git ignores it. Do not commit it. Do not cite or link to
  `plans/`, or cite the content of a plan: its sections, its item numbers or its local PR labels
  ([ADR-0001](decisions/entries/0001-decision-log-agents-md-and-private-data.md)).
- Do not push to a git remote without the approval of the user. One approval for a PR covers its
  push, its draft PR and its description.
- Ask the user before any other action that is visible outside this machine, for example a PR
  comment, a later change to a PR description, a change of a draft PR to ready, a release or a
  published image. A force-push is a new push. It needs its own approval.
- Do not add AI attribution, for example a `Co-Authored-By:` trailer, to a commit or a PR. This
  rule overrides a default of a tool or a harness that adds attribution.
- Until v2.0.0 of the skellyspecs recording format is released, commit to `main` directly.
- After v2.0.0 is released, open each PR against `main`.
- Put one kind of change in each PR: "code", "docs" or "CI".
- Use the GitHub `noreply` address as the commit email. Do not write the email address of a person
  in a commit, a file or a PR.

## 7. Tool Calls

Before a tool call that needs user permission, write a one-line summary of the call.
The summary must tell what the call does and what it changes.
Write the summary in the message text, not only in the tool description.

## 8. Private Data

This repository is public, or it can become public. Git history is permanent
([ADR-0001](decisions/entries/0001-decision-log-agents-md-and-private-data.md)).
Do not write these in a tracked file, a commit message or a PR body:

- a credential, a token, a password or a private key;
- an absolute path in a user folder;
- a hostname or a user name in prose;
- an email address that is not on the allowlist of `tools/check_private_data.py`;
- a private URL or a private IP address;
- a raw dump of `env`, `pip list`, `nvidia-smi` or `docker inspect`.

- Use paths relative to the repository, for example `../skellycam/research/`.
- Give a measurement as a summary with its tool and its version.
- A report field or a test fake can contain a hostname.
- Text from `plans/` must obey these rules before it goes into a tracked file.
- To also block a hostname or a user name, put it in `.private-terms` in the repository root. Git
  ignores that file. Do not commit it.
- If you find private data in a tracked file, remove it with a redaction edit. Then tell the user,
  because git history keeps the data. Also revoke a leaked credential.
- The pre-commit hook runs `gitleaks` and `tools/check_private_data.py`. CI runs `gitleaks` on each
  push and PR. `.gitleaks.toml` holds the reviewed false positives.
- The commit-msg hook warns about AI attribution. If you are an AI agent and you see
  this warning, tell the user.
- Turn on secret scanning and push protection for a private repository on the day that it becomes
  public.
