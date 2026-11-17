# N1AM — The gate 2 approval of stage 1

**Status:** absorbed into
[`AGENTS.md#4-project-rules`](../../AGENTS.md#4-project-rules),
[`AGENTS.md#6-git-rules`](../../AGENTS.md#6-git-rules),
[`spec/SPEC.md#skellyfileformat-specification`](../../spec/SPEC.md#skellyfileformat-specification),
[`spec/conformance.md#skellyfileformat-conformance-tests`](../../spec/conformance.md#skellyfileformat-conformance-tests),
2026-11-17 (commit to main; was accepted, 2026-11-17 (user; "stage 1 approved")).

## Decision

The user wrote on 2026-11-17: "stage 1 approved. Research can be pushed. I'll start a new session
in skellycam to begin implementation".

1. **Gate 2 for stage 1.** The user approved gate 2 for stage 1 of
   [ADR-CPM2](CPM2-stages-of-the-implementation.md) on 2026-11-17. Stage 1a starts now. Stage 1b
   (the skellysync folders, G17) starts only after the five skellysync decisions D-Q, D-FPS, D-HDR,
   D-DRIFT and D-AUDIO ([ADR-CPM2](CPM2-stages-of-the-implementation.md) item 3). The approval does
   not change this. The user has not approved gate 2 for stages 2, 3 and 4.
2. **The order of stage 1a.** The implementation of stage 1a can start, in the order of
   [ADR-Z641](Z641-program-guidance-gate-2-scope-and-no-push.md) item 4: the Python reader, then the
   Python writer, then the JavaScript reader.
3. **The two tests of the package.** The two tests of the package in the staged build
   ([ADR-CPM2](CPM2-stages-of-the-implementation.md) items 10 and 12) are not part of this approval.
   The user must review them as additions to the tests before the code of stage 1a starts.
4. **Push.** The approval of stage 1 ends the agreement of no push
   ([ADR-Z641](Z641-program-guidance-gate-2-scope-and-no-push.md) item 3). The agent still asks the
   user before the first push of skellyfileformat. "Research can be pushed" is about the research
   branch of skellycam. It is not an approval of a push of this repository. The user
   then approved the first push of skellyfileformat on 2026-11-17 (question Q193).

## Reason

- Items 1 and 2: an agent must know which stage it can implement, and in which order.
- Item 3: the user did not review the two tests at gate 2. `open-work.md` holds them.
- Item 4: section 6 of `AGENTS.md` needs the approval of the user for each push. The words of the
  user name no push of this repository.

## Open work

See [open-work.md](../open-work.md).
