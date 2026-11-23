# Open work

This file holds the open work of the [decision log](README.md). Read the items that apply to your
task. Delete an item when its work is done. The PR that closes an item records the result.

- **The move to skellyspecs** ([ADR-YYP7](entries/YYP7-skellyspecs-one-repository-for-the-specs.md)).
  - The user renames the GitHub repository and the local folder to `skellyspecs` after the first
    push of the move.
  - The import of `tracker-pipelines/` and `model-sidecars/` with four skills, from one pushed
    skellytracker commit after its LF commit, with an import entry and its link script. Then the
    port of the four skills.
  - When the first proposal record lands in `tracker-pipelines/proposals/`, the link check must
    skip it, as it skips the records of `model-sidecars/proposals/`.
  - The full-SHA links to the skellytracker root log, after that log is on the skellytracker
    default branch.
  - The kit sync from the kit commit of the two-way hub, after the import.
