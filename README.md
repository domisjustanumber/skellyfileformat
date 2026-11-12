# skellyfileformat

skellyfileformat defines the file format of skellycam and skellysync recordings: JPEG video in
Matroska (MKV) with a timing sidecar, and FLAC audio with its timing sidecar. The
[specification](spec/SPEC.md) gives the byte layouts, the field meanings, the clocks and the
finalisation and recovery rules, so that other programs can implement the format from the spec
alone.

**Status: draft.** No format version is released yet. The spec and its conformance tests are written
first and reviewed. Code comes after them ([AGENTS.md section 4](AGENTS.md#4-project-rules)).

The sections marked "normative" are rules. A change to them needs a decision entry
([decisions/](decisions/README.md)).

## Scope (normative)

The format covers these files:

- the camera video: an MKV file with one JPEG video track, in which every frame is a key frame;
- the video timing sidecar: an attachment in the camera MKV, or a separate file until the MKV is
  finalised or after a crash;
- the skellycam audio: a `.audio.mka` file with one FLAC track, and its timing sidecar `.skau` as an
  attachment;
- the skellysync audio: a FLAC track in each camera MKV.

The format does not cover recordings that older programs wrote, for example H.264 MP4 files and
timestamp CSV files. The programs that read those recordings define how they read them. Section 13
of the spec tells how to find a file that is not in this format.

## Compatibility promise (normative)

- A conforming reader must read every released format version.
- A released format version is one with `prerelease` = 0 in its header
  ([Versioning](#versioning-normative)).
- A file with `prerelease` > 0 has no compatibility promise. A later reader can refuse it.
- A writer writes only the latest format version.

## Versioning (normative)

- **Format version.** The format version is the `major.minor` of the skellycam release that last
  changed the format.
  - A change that an older reader cannot read needs a new skellycam major version.
  - An added field needs a new skellycam minor version, or a new major version.
  - A skellycam patch release does not change the format.
- **Header fields.** Each sidecar header (the video timing sidecar and the `.skau`) holds three
  unsigned 16-bit fields: `major`, `minor` and `prerelease`.
  - `prerelease` is 0 for a released format, and N for the Nth prerelease revision.
  - A reader must refuse a file with a `major` that it does not know.
  - A reader must read a file with a higher `minor` of a `major` that it knows, and skip the fields
    that it does not know.
- **Writer string.** Each sidecar also holds a writer string, for example `skellycam 2.1.0`. It is
  for diagnostics only. A reader must not change its behaviour because of it. skellysync writes the
  format version that skellyfileformat gives, not its own version.
- **Package version.** The skellyfileformat package uses semantic versioning. Its `major.minor` is
  the format version that it implements. Its patch number counts the library fixes that do not
  change the format.

## Conformance (normative)

- A conforming writer writes files that obey each writer requirement of [SPEC.md](spec/SPEC.md),
  and it passes each writer test of [conformance.md](spec/conformance.md).
- A conforming reader obeys each reader requirement of SPEC.md, passes each reader test of
  conformance.md, and reads each golden file in `golden/` to the expected result.
- Each requirement has an ID `SFF-NNN`. Each test has an ID `SFT-NNN` and names the requirements
  that it checks.

## Licenses

- The spec text (`spec/`) and the normative sections of this README: CC-BY-4.0
  ([spec/LICENSE](spec/LICENSE)).
- All other files: Apache-2.0 ([LICENSE](LICENSE)).

## Development

Read [AGENTS.md](AGENTS.md). Run `uv sync`, then `uv run pre-commit install`, then `uv run pytest`.
