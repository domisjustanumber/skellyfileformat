# T8PK — Private data is allowed and declared; no file runs code when it is read

**Status:** absorbed into
[`spec/SPEC.md#16-tracking-parquet`](../../spec/SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#181-blender`](../../spec/SPEC.md#181-blender),
[`spec/SPEC.md#22-privacy-and-safety`](../../spec/SPEC.md#22-privacy-and-safety),
2026-11-17 (commit to main; was accepted, 2026-11-16 (user; whole-folder grilling, 2026-11-13 to 2026-11-16)).

## Decision

1. **Private data is allowed in any field** of the folder files, including device names, serial
   numbers, user-entered names, the time zone and absolute paths. The goal of a camera identity
   field is to identify a camera as exactly as possible, which needs such data.
2. **The `privacy` list.** The manifest holds a `privacy` list: each field of the take that can hold
   identifying data, and a note that the video, the audio and the tracking data show people.
3. **The reader result** has `may_contain_private_data`. freemocap shows the notice when a user
   exports or shares a take.
4. **No strip option for now.** The spec tells the user what is in the files. A later feature can
   remove fields.
5. **No code in files.** No file of the folder uses a format whose loading runs code, for example
   Python pickle. A reader of this format never runs file content. The realtime ChArUco cache is
   replaced by tracking rows ([ADR-P76Y](P76Y-tracking-parquet.md)). The Blender addon pickle is
   dropped ([ADR-QS7B](QS7B-blender-outputs-and-exports.md)).

This entry replaces the privacy rule of spec v0 (SFF-653: no user names, no raw serial numbers, no
absolute paths) and the "never the raw serial number" part of
[ADR-DK8S](DK8S-mcap-profile-files-and-names.md) item 8. `camera_key` stays a hash
([ADR-6RSB](6RSB-camera-files-mjpeg-mkv-and-csv-timing.md) item 8). The repository rule of
[ADR-0001](0001-decision-log-agents-md-and-private-data.md) (no private data in this repository)
does not change.

## Reason

- Users enter camera names, and those can hold private data. A ban would remove the data that
  identifies a camera.
- A user who shares a take must know what is in it.
- Loading a pickle runs the code inside it. A shared take with a crafted pickle would run that code
  when freemocap opens it. Pickles also break when class names change.

## Evidence

- skellycam `dom/research`, `research/skellycam_recording/docs/whole_folder_spec_plan_20261113.md`,
  "Grilling log": round 3 Q7, Q8; round 4 Q2, the final privacy decision and Q5; round 5 Q8 (local,
  not committed).

## Alternatives rejected

- Ban user-editable names and raw serial numbers: they identify the camera.
- An option to strip private fields: deferred to a later feature.

## Open work

[open-work.md](../open-work.md)
