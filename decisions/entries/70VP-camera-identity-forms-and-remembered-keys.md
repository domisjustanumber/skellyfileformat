# 70VP — Camera identity: four forms, remembered keys, `key_origin`, the user name

**Status:** accepted, 2026-11-16 (user; review of the camera identity).

## Decision

Items 1, 3 and 4 change [ADR-DM9S](DM9S-spec-v2-details-part-7.md) item 16a (two forms, and a key
that is always computed). They add to [ADR-VPD9](VPD9-spec-draft-v2-details.md) item 4. The other
rules of the two entries stay. SFF-752 holds the full text.

1. **Four forms.** The identity string is the first form that applies. Reason: no camera gets an
   OS index as its key, and no camera is refused.
   - (1) `<vendor_id>:<product_id>:serial:<serial>`, when the USB serial number is usable: it is
     not empty, it is not a known placeholder (for example `0001`), and no other connected camera
     with the same vendor ID and product ID has the same serial.
   - (2) `<vendor_id>:<product_id>:port:<port_path>`. The capture writer reads the port path from
     the operating system, never from the capture library.
   - (3) `<vendor_id>:<product_id>:device:<os_device_id>`, for a camera that is not a USB device
     and has a persistent identifier of the operating system (for example a built-in laptop
     camera). `device` gets the member `os_device_id` (a text or null). The privacy `fields` table
     gets a row for it, with the kind `device_path`.
   - (4) `<vendor_id>:<product_id>:assigned:<uuid>`: 32 lowercase hexadecimal characters of a
     random UUID. The capture program makes it one time for the camera and remembers it. The user
     attaches it to the camera again in a later session. It replaces each earlier draft of a last
     resort (an OS index, a session key).
   - A capture writer never refuses a camera for its identity, and never writes `camera_key` 0.
2. **A forgiving match on load.** When a connected camera matches no remembered key, but its
   vendor ID and model name from the OS match a remembered camera that is not connected, the
   capture program asks the user if it is the same camera. When the user agrees, the camera keeps
   the remembered `camera_key`. When several remembered cameras fit, the user selects one from a
   list (by `user_name` and `camera_label`) or says that it is a new camera. Reason: a camera on
   another port must not lose its key and its calibration.
3. **Remembered key and `key_origin`.** A capture writer MAY write the remembered `camera_key` in
   place of the computed one, when the user confirmed that the device is that camera. The camera
   config gets `key_origin` after `user_name`: `"computed"` (the hash of form 1, 2 or 3, built from
   the `device` values of this file), `"confirmed_by_user"` (a remembered key that the camera has
   because the user confirmed the camera, in this session or an earlier one), `"assigned"` (form
   4, made in this session, confirmed by nobody), or null when `camera_key` is 0. Reason: a test
   must know when it can compute the key from the file.
4. **No shared key.** Two different cameras never share a key. The capture program finds a
   remembered camera by its remembered location (serial, port path or OS device identifier), not
   by a new computation of the hash. When the computed key of a camera is equal to the key of a
   remembered camera that has another location, the capture program asks the user, as in item 2,
   before it uses the key. Reason: a second identical camera on the old port of a moved camera
   computes the key of the moved camera.
5. **`user_name` is metadata only.** It is never part of a file name, of `camera_label` or of the
   identity string. It is null, or a text of 1 to 128 bytes of UTF-8 with no control character. A
   writer SHOULD NOT give two cameras of one take the same `user_name` that is not null. A reader
   has no rule for it. Reason: a new name must not change a file name or a link.
6. **The port form stays** for a camera with no serial number. Reason: a rig that does not move
   needs no question to the user.
7. **The list of remembered cameras** is local state of the capture program. It is not in the take
   folder and not in the spec. A capture program can make it from the capture info JSON of any
   take. No file format for a rig is defined. Reason: each take holds `camera_key`, `user_name`,
   the model and `device`.

**Not decided.** The spec marks these parts provisional, and [open-work.md](../open-work.md) lists
them: the source and the text form of `port_path` and `os_device_id` on each OS, which no test on
Linux or macOS supports; and the placeholder list and the character rule of a usable serial, which
are a proposal from the research code.

## Reason

Each item has its reason. The capture library gives no serial number and no port path of the
operating system.

## Consequences

- SFT-717 computes the key only for `computed`. Appendix A gets the case `confirmed_key` of G1.
- skellycam and freemocap need the code changes that open-work.md lists.
- A wrong answer of the user gives one camera the key of another camera. No file shows it.

## Evidence

skellycam `dom/research` (local, not committed):
`research/skellycam_recording/docs/camera_identity_alternatives_20261116.md`,
`research/skellycam_recording/docs/camera_user_labels_design_20261116.md` and
`research/usb_cameras/naming/camera_identity.py` (`serial_is_usable`, `PLACEHOLDER_SERIALS`). Only
the Windows code was run. No test did a reboot, a replug, a port move or two identical cameras.

## Alternatives rejected

- The OS index, or a session key, as the last form: two different cameras can get one key, or the
  key does not stay for the next session.
- To refuse a camera with no identifier, or to write `camera_key` 0: the user decided against both.
- The user name in the file names or in the key: a new name changes the names and the links.
- An assigned key for each camera with no serial: each such rig then needs a question (item 6).

## Open work

[open-work.md](../open-work.md)
