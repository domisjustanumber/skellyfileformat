# skellyspecs

This repository holds the specs of the freemocap programs
([ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md)). Each spec is in its
own folder, with its own rules and decision log:

| Folder | Spec |
|---|---|
| [`recording-files/`](recording-files/README.md) | The take folder of skellycam, skellysync and freemocap recordings |
| `tracker-pipelines/` | The tracker pipelines of skellytracker (not imported yet) |
| `model-sidecars/` | The model sidecars of skellytracker (not imported yet) |
| `exporter-guide/` | The guide for model exporters (after an exporter test run passes) |

This repository holds no reader and no writer of a format that a program implements. The programs
pin a commit of this repository and run its tests against their own code.

## Licenses

Each file of this repository, also the spec text, has the license Apache-2.0 ([LICENSE](LICENSE),
[ADR-YYP7](decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 6).

## Development

Read [AGENTS.md](AGENTS.md). Run `uv sync`, then `uv run pre-commit install`, then `uv run pytest`.
