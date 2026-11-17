# skellyfileformat

skellyfileformat defines the take folder of skellycam, skellysync and freemocap recordings: MJPEG
video in MKV and Opus audio in fragmented MP4, each with a CSV timing sidecar, and every folder file
that the programs add, such as the manifest, the info JSONs, the calibration TOML and the tracking
Parquet ([ADR-2C9V](decisions/entries/2C9V-whole-take-folder-scope-and-package.md)). The
[specification](spec/SPEC.md) gives the names, the layouts, the meaning of each field, the clocks, the
writing and recovery rules, and how a reader opens a folder, so that other programs can make a
compatible folder or read the output of freemocap from the spec alone.

**Status: draft.** No format version is released yet. The spec and its conformance tests are written
first and reviewed. Code comes after them ([AGENTS.md section 4](AGENTS.md#4-project-rules)).

The sections marked "normative" are rules. A change to them needs a decision entry
([decisions/](decisions/README.md)).

## Scope (normative)

The format describes one take folder: the files of one synchronised capture and every file that the
programs add to it later ([ADR-2C9V](decisions/entries/2C9V-whole-take-folder-scope-and-package.md),
[ADR-5XNA](decisions/entries/5XNA-folder-layout-names-and-manifest.md)). It covers these files:

- each camera file: an MKV file with one MJPEG track and index timestamps, with its CSV timing
  sidecar ([ADR-6RSB](decisions/entries/6RSB-camera-files-mjpeg-mkv-and-csv-timing.md));
- the audio file: Opus in fragmented MP4, with its CSV timing sidecar
  ([ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md));
- the recording manifest, the capture info JSON, the processing info JSON and the calibration TOML
  ([ADR-N6HS](decisions/entries/N6HS-info-jsons-and-calibration.md));
- the tracking Parquet and the realtime journal
  ([ADR-P76Y](decisions/entries/P76Y-tracking-parquet.md),
  [ADR-Q9X2](decisions/entries/Q9X2-realtime-tracking-journal.md));
- the Blender outputs, the annotated videos, the exports and the logs, by name, container and content
  mapping ([ADR-QS7B](decisions/entries/QS7B-blender-outputs-and-exports.md)).

It also covers the folder as a whole: the fixed names, the links between the files, the clock that
the files share, the writing rules, how a reader opens a folder (also when it is crashed or
incomplete), and how a reader recognises a legacy folder of freemocap v1.x
([ADR-CZQ9](decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md)). The code that reads
legacy folders stays in skellycam and freemocap.

## Compatibility promise (normative)

- A conforming reader must read every released format version.
- A released format version is one with `format_prerelease` = 0 in its files
  ([Versioning](#versioning-normative)).
- A file with `format_prerelease` > 0 has no compatibility promise. A later reader can refuse it.
- A writer writes only the latest format version.
- A rule of the programs, not of the format (as in
  [legacy-annex.md section 8](spec/legacy-annex.md#8-old-recordings-in-skellycam-and-freemocap)):
  new skellycam, skellysync and freemocap write only this format. They write no legacy timestamp
  CSV, no FLAC, WAV or MCAP audio and no burned-in overlay
  ([ADR-CZQ9](decisions/entries/CZQ9-read-old-write-new-and-legacy-recognition.md) item 2,
  [ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md) item 1).

## Versioning (normative)

- **Format version.** The format version is the `major.minor` of the freemocap release that last
  changed any file of the take folder
  ([ADR-9DV4](decisions/entries/9DV4-format-version-from-freemocap.md)).
  - A change that an older reader cannot read needs a new freemocap major version.
  - An added field needs a new freemocap minor version, or a new major version.
  - A freemocap patch release does not change the format.
  - The skellyfileformat package and skellycam release at the same `major.minor` when the format
    changes.
  - freemocap 2.x and skellycam 2.x are released at the same time. Until then, the 2.0.0
    prereleases of skellycam can write prerelease files
    ([ADR-9DV4](decisions/entries/9DV4-format-version-from-freemocap.md) item 9).
- **Version fields.** Each file that the spec names in SFF-707 records the format version under which
  it was written: `format_version` (`major.minor`) and `format_prerelease`. `major`, `minor` and
  `format_prerelease` are unsigned integers that fit in 16 bits. The spec gives the place of the
  fields in each of these files. A camera file and an audio file are standard media files with no
  added field: the timing sidecar holds the fields for its media file
  ([ADR-E45D](decisions/entries/E45D-spec-draft-v2-corrections-after-review.md)).
  - `format_prerelease` is 0 for a released format. For a draft, the spec gives its value (SFF-710).
    The value is 1 until the draft goes to external review. From then on, each revised draft that
    goes to the reviewers adds 1. A reader treats each value above 0 in the same way. The readers of
    this package give the warning `prerelease`
    ([ADR-2MQE](decisions/entries/2MQE-tests-prerelease-serial-and-exports.md) item 8).
  - A reader must refuse a file with a `major` that it does not know.
  - A reader must read a file with a higher `minor` of a `major` that it knows, and skip the fields
    that it does not know.
- **Container versions.** The version of a container (Matroska, MP4, Parquet) is not the format
  version.
- **Writer string.** Each of these files also holds a writer string, for example `skellycam 2.1.0`. It is for
  diagnostics only. A reader must not change its behaviour because of it. skellysync writes the
  format version that skellyfileformat gives, not its own version.
- **Package version.** The skellyfileformat package uses semantic versioning. Its `major.minor` is
  the format version that it implements. Its patch number counts the library fixes that do not change
  the format.

## Conformance (normative)

- A conforming writer writes files that obey each writer requirement of [SPEC.md](spec/SPEC.md),
  and it passes each writer test of [conformance.md](spec/conformance.md).
- A conforming reader obeys each reader requirement of SPEC.md, passes each reader test of
  conformance.md, and reads each golden folder in `golden/` to the expected result.
- Each requirement has an ID `SFF-NNN`. Each test has an ID `SFT-NNN` and names the requirements
  that it checks.

## Package

The format code is in one shared package, skellyfileformat. It holds the spec, the conformance test
list, the golden files, a Python reader and writer, and a JavaScript reader. The optional write
layer `skellyfileformat[write]` holds the writer. The Python reference reader reads each file of the
folder: the scope `full` of SFF-892. The JavaScript reader reads only what the skellycam player
needs: the scope `player`. The writer encodes Opus with libopus through PyAV, at the version that
the exact `av` pin gives (SFF-762, SFF-763)
([ADR-2C9V](decisions/entries/2C9V-whole-take-folder-scope-and-package.md) items 5 and 6,
[ADR-92TM](decisions/entries/92TM-opus-audio-in-fragmented-mp4.md) item 2).

## Licenses

- The spec text (`spec/`) and the normative sections of this README: CC-BY-4.0
  ([spec/LICENSE](spec/LICENSE)).
- All other files: Apache-2.0 ([LICENSE](LICENSE)).

## Development

Read [AGENTS.md](AGENTS.md). Run `uv sync`, then `uv run pre-commit install`, then `uv run pytest`.
