# 4EZ2 — Kit sync: absorb at landing, restate by link, and changes before the first push

**Status:** absorbed into
[`decisions/README.md#rules`](../README.md#rules),
[`decisions/template.md#decision-log-entry-template`](../template.md#decision-log-entry-template),
[`tools/check_links.py`](../../tools/check_links.py),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; sync of the agents and ADR kit)).

## Decision

This repository takes the kit rules that changed after its bootstrap on 2026-11-12
([ADR-0001](0001-decision-log-agents-md-and-private-data.md)). The source is the kit in
`../project/agents-and-adr-process/bootstrap/`, from its sync commits of 2026-11-12 and
2026-11-15. These commits are not pushed. The text of each rule is the kit text, with
`{{DEFAULT_BRANCH}}` filled in as `main`.

1. **Changes before the first push.** An entry in a commit that is not pushed to a remote can
   change in that commit, in each part. The four edits of the Rules apply from the first push
   (skellytracker ADR-C3E5, PR pending, `C3E5-one-place-for-the-form-of-a-question`).
2. **Absorb at landing.** The commit group that writes or lands an entry, or that writes its rules
   into the absorb documents, absorbs the entry in its last commit when the absorb documents state
   all of its rules. `template.md` gets the bullet **Absorb at landing**
   (skellytracker ADR-W823, PR pending, `W823-absorb-in-the-commit-group-that-states-the-rules`).
3. **Restate by link.** An entry that supersedes an old entry links the heading of each kept rule
   that a heading states. It writes text only for a changed rule and for a kept rule that no heading
   states. The **Decision** bullet of `template.md` gets the same sentence (skellytracker ADR-W823).
4. **The link check docstring.** `tools/check_links.py` is a byte copy of the kit copy. Its
   docstring now states that the check skips the folders of `specs/model-sidecar/proposals/`. This
   repository has no such folder. The code did not change
   (skellytracker ADR-1HKJ, PR pending, `1HKJ-proposal-record-links-not-checked`).

## Reason

The user asked on 2026-11-17 for this repository to agree with the latest kit. A Rules change
needs an entry ([Rules](../README.md#rules)). Item 2 also keeps the index under its limit: the
entries of the commits that are not pushed go to Historical when the spec states all of their
rules.

## Consequences

- The same commit group absorbs [ADR-64ER](64ER-unknown-major-form-audio-fit-rows-and-refused-pair-counts.md),
  [ADR-B6WH](B6WH-repair-equal-pair-cut-and-no-normal-end.md) and
  [ADR-1P4N](1P4N-timing-coverage-of-a-realtime-run-and-latency-at-the-fold.md). The other
  entries of these commits stay `accepted`: an absorb document does not state one or more of their
  rules. The consolidation of [ADR-H2HQ](H2HQ-descriptor-members-deferred-points-and-old-audio.md)
  item 6 does not change.
- `AGENTS.md` does not change. Its shared blocks already have the kit text. Step 3 of the kit guide
  removes the kit marker lines, so they are not added.
- The CI versions, `.gitleaks.toml`, `ALLOWED_EMAILS` and its test stay as this repository has them.
