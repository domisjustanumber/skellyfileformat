# Decision log of recording-files

This log records the decisions of the module `recording-files/`: the take-folder spec, its
conformance list, its golden folders and its conformance tests
([ADR-YYP7](../../decisions/entries/YYP7-skellyspecs-one-repository-for-the-specs.md) item 4).
Read this file and [open-work.md](open-work.md) before you change a file of this module. The
[Rules](../../decisions/README.md#rules) and the [template](../../decisions/template.md) of the root
log apply. The root log has the decisions for the whole repository.

## Index

### Active

These entries are `accepted` or `evidence`.

| # | Decision | Status |
|---|----------|--------|
| [5B03](entries/5B03-choices-for-the-format-changes-f1-to-f10.md) | Choices for F-1 to F-10: player marks, completion after a write error, tail repair, summary nulls, DHT order, F-5 as a player rule, test inputs | accepted |
| [76NN](entries/76NN-details-for-the-format-changes-f1-to-f10.md) | Details for F-1 to F-10 from a review: byte-field rows, tail repair steps, SFF-828, no-block file, terms, `stored_px`, tests | accepted |
| [6PNN](entries/6PNN-format-field-skellyspecs.md) | The format field is `skellyspecs`; no old name; adapter variables; golden folders made again | accepted |
| [91PB](entries/91PB-choices-for-the-v1-camera-file-rules.md) | Choices for SFF-896 to SFF-903 and SFT-774 to SFT-778: place, draft form, scope beyond Q741 and Q765, refusals, roundings, tests | accepted |
| [3XYN](entries/3XYN-v1-camera-file-rules-move-to-recording-files.md) | The v1 camera-file rules (time map, refused eras, frame table) move here from the skellycam player spec | accepted |

### Proposed

These entries wait for a decision of the user. Section is the section or area of the change, or
`none`.

| # | Decision | Section | Status |
|---|----------|---------|--------|
| [VS9Z](entries/VS9Z-converter-cases-keep-the-mark-stage1a.md) | The converter cases of SFT-705 and SFT-717 keep the mark `stage1a`; they stand for the converter of skellysync | `conformance.stages` | proposed |

The entries that are `rejected`, `superseded by XXXX`, `absorbed into <path>#<anchor>`,
`evidence; used by XXXX` or `done` are in [historical.md](historical.md).

## Open work

The open work is in [open-work.md](open-work.md).
