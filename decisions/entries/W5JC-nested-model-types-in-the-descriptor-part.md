# W5JC — Nested model types in the Parquet descriptor part

**Status:** absorbed into
[`spec/SPEC.md#16-tracking-parquet`](../../spec/SPEC.md#16-tracking-parquet),
[`spec/SPEC.md#23-the-reader-result`](../../spec/SPEC.md#23-the-reader-result),
[`spec/parts/parquet-descriptor.md#parquet-descriptor-normative-part-of-specmd-section-16`](../../spec/parts/parquet-descriptor.md#parquet-descriptor-normative-part-of-specmd-section-16),
[`spec/conformance.md#tracking-parquet-section-16`](../../spec/conformance.md#tracking-parquet-section-16),
2026-11-16 (commit to main; was accepted, 2026-11-16).

## Decision

1. **The nested types are in the part.** `spec/parts/parquet-descriptor.md` defines each nested type
   of `RecordedModel`, with its members, types and rules. The part no longer points to a research
   file. The sources are skellyforge at f5404db, skellytracker at 03b9c1d, skellyforge `sfn26` at
   5f0fd2d and freemocap at c27fc299 and at `sfn26` (ca0c17cc). The part has an informative example.
2. **`presentation` is in the spec.** `SkeletonSnapshot` has the optional member `presentation`. A
   writer omits it when it is null. Its types are `Presentation`, `SuperquadricContours`,
   `PresentationMaterial` and `ConnectionMaterial`, as in skellyforge `sfn26`. `AttachedLines` and
   `AttachedSurface` are compiled output. They are not in the descriptor.
3. **What a reader checks.** The reader of this package checks only the structure of a model: each
   member is present, each member has its type, and a closed type has no other member. A structure
   fault gives `bad_schema`. Each other rule of the model types is a writer rule. A writer must obey
   it. The reader does not check it in version 2.0. A later minor version can add an optional deep
   check. The deep check reports a fault of a writer rule as a warning, and it never refuses the
   file. Nothing more is specified for the deep check.
4. **Consistency repairs.** The code forces these corrections of the part:
   a. `handedness` is the integer 1 or -1. It is the exception to "an enum is its text value".
   b. A quaternion of the rest pose in the descriptor is unit to 1e-9. The 1e-5 of row rule 5 stays
      for the data rows.
   c. `observation_frame` and `presentation` are omitted when null. `tracker_connections` is omitted
      when empty. SFF-832 and SFT-750 say the same.
   d. The keys of `segment_masses` are the segment names that the definitions give after the
      left/right expansion of a sided definition.
5. **`anchor_segment_name`** is a segment of the skeleton, or null. This is a writer rule.

## Reason

A generator must build a valid descriptor from the spec alone. The types were only in a local
research file. The code of freemocap refuses a descriptor that follows the old text of items 4a to
4d. The user decided items 2 and 3. For item 3: the code of freemocap applies most of these rules only
when it restores a model, and it loads a descriptor that breaks them.

## Consequences

A reader of version 2.0 can accept a model that freemocap cannot restore. The types from `sfn26` have
no pinned commit in freemocap.

## Evidence

- skellyforge f5404db: `skellyforge/core/skeleton/skeleton_snapshot.py`, `skeleton_definition.py`,
  `components/`, `linkage/joint_definition.py`, `chain/kinematic_chain.py`,
  `core/biomechanics/center_of_mass.py`, `core/math/geometry/rotation_quaternion.py` and
  `orthonormal_basis/handedness.py`.
- skellyforge `sfn26` 5f0fd2d: `skellyforge/core/skeleton/presentation.py`, and `presentation` in
  `skeleton_snapshot.py` and `skeleton_definition.py`. In `skellyforge/core`, of the files that hold
  the nested types, only these two differ from f5404db.
- skellytracker 03b9c1d: `skellytracker/core/io/tracker_mapping.py`.
- freemocap c27fc299 and `sfn26`: `freemocap/core/recording/data_descriptors/recording_model.py`
  (the members, the omitted members and the `segment_masses` check),
  `freemocap/core/skeletons/tracked_skeleton_bundle.py` (the anchor) and, at `sfn26`,
  `freemocap/core/skeletons/rigid_object_geometry.py`.
- The example of the part loads in the `RecordedModel` class of freemocap c27fc299, with skellyforge
  f5404db and skellytracker 03b9c1d. The class writes the same JSON value again, and
  `to_bundle()` passes. The class refuses the text `RIGHT_HANDED` and a quaternion with a norm error
  of 1e-8.
- A model with the configuration of `RecordedModel` and the `SkeletonSnapshot` of skellyforge 5f0fd2d
  refuses an unknown member in each presentation type. It refuses a bad `color` or `opacity` at
  load. The other presentation rules fail only at restore.

## Not repeated

- Do not round a descriptor quaternion to float32.
- Do not use the keys of `center_of_mass.definitions` as the keys of `segment_masses`.

## Open work

See [open-work.md](../open-work.md).
