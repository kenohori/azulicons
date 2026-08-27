# Azul icon Blender sources

Per-icon Blender source files for the icons in `../Assets.xcassets`. Each
file is self-contained: opening it and pressing Render (F12) writes
`<icon>.png` next to the `.blend`.

The set is migrating to a shared lighting rig (2026-08). Ten icons
(Building, Railway, Road, SolitaryVegetationObject, CityFurniture, Bridge,
TransportSquare, TINRelief, CityObjectGroup, OtherConstruction) are defined
by the rig below; the other six (GenericCityObject, LandUse, PlantCover,
Tunnel, WaterBody, Waterway) still carry their historical per-icon fitted
values and reproduce their committed PNGs exactly.

## Shared rig (2026-08)

- World background grey **0.82**, point `Light` at **300 W** (radius 0.1) —
  same position in every file: (4.076, 1.005, 5.904).
- Every file shares one camera (35 mm persp) and pose; render settings:
  Cycles, 512 samples, transparent film, Standard view transform, RGBA PNG.
- **Normalized framing**: geometry is scaled/shifted so the rendered alpha
  bbox spans **84 % of the canvas** (±1 px) and is centred. This was done
  with a render-measure-adjust loop probing at 64 px / 24 samples, then
  saving; icons are NOT hand-framed, so don't move geometry without
  re-checking the bbox.
- Road's dash material is plain white (1.0) again; the historical 5.59
  "brighter than white" value existed only to compensate the road's old dim
  per-icon rig.

## Files

- **`<Icon>.blend`** — one per icon, sixteen CityGML/CityJSON types in total:
  `Building.blend`, `TINRelief.blend` (terrain), `Road.blend`,
  `LandUse.blend`, `TransportSquare.blend`, `Bridge.blend`, `Railway.blend`,
  `GenericCityObject.blend`, `SolitaryVegetationObject.blend`,
  `Tunnel.blend`, `PlantCover.blend`, `WaterBody.blend`, `CityFurniture.blend`,
  `CityObjectGroup.blend`, `OtherConstruction.blend`, `Waterway.blend`.
  (A `Track.blend` existed historically but was removed: Track is a CityGML
  Trans-ADE class, not a CityJSON type.)
- **`../icons.blend`** — the combined working file containing eight icon
  scenes as collections, plus camera and lights. The icon scenes overlap in
  world space, so an icon is rendered by isolating its collection.
- **`../azul logo.blend`** — the original Azul logo source (Blender 2.77,
  2016). The Building icon geometry is the same house it contains.

## Structure of each file

- One collection (named after the icon) containing the icon geometry.
- `Camera` — render camera (35 mm, standard icon pose; identical in all
  sixteen files).
- `Light` — point light at (4.076, 1.005, 5.904); 300 W on the shared rig,
  otherwise the per-icon energy from the table below.
- World background grey: 0.82 on the shared rig, otherwise from the table
  below. For most icons the world is the dominant light.
- Render settings: Cycles, 512 samples, 64×64, transparent film, Standard
  view transform, RGBA PNG.

## Per-icon lighting values (legacy tier)

These apply to the six icons **not** on the shared rig. They were fitted
numerically per icon (least squares in linear colour space) so that a render
reproduces the committed PNG.

| Icon                | World grey | Light (W) |
| ------------------- | ---------- | --------- |
| GenericCityObject   | 0.51       | 880       |
| LandUse             | 0.85       | 366       |
| PlantCover          | 0.67       | 985       |
| Tunnel              | 0.26       | 464       |
| WaterBody           | 0.82       | 618       |
| Waterway            | 0.76       | 520       |

Notes:

- The 100 W `Lamp` in `icons.blend` contributes nothing to renders (it is
  effectively invisible), so it is omitted from the per-icon files.
- Both road materials render through the legacy `Diffuse BSDF` branch, not
  the Principled BSDF (the Principled sockets are inert in this file; the
  `active output` flag is misleading). Historically the dash colour was 5.59
  (brighter than white) to match the original icon under the road's dim
  per-icon rig; since the shared-rig migration the dashes are plain white
  (1.0).
- Historical (pre-rig) fitting residuals: Building matched only
  approximately (a small shading residual); all other then-original icons
  rendered essentially pixel-perfect (alpha error at or below the 0.008
  threshold). The shared-rig icons are defined by the rig and framing, not
  by residuals.

## Recreated icons

Six icons were recreated from `icons.blend` leftovers where possible and
otherwise modelled from the committed renders. They use the same camera and
render settings as the other files. SolitaryVegetationObject and
CityFurniture have since moved to the shared rig; their rows below record
the historical fit.

| Icon | World grey | Light (W) | Based on | Fidelity (interior MAE / alpha MAE) |
| ---- | ---------- | --------- | -------- | ----------------------------------- |
| GenericCityObject | 0.51 | 880 | cube from the icon, fitted in scale and pose | 0.014 / 0.002 (exact) |
| SolitaryVegetationObject | (rig) | (rig) | the original leftover `Cone` mesh from `icons.blend` `Collection 1` as the crown, trunk fitted underneath | — |
| Tunnel | 0.26 | 464 | open tube (fitted scale and pose) with the railway objects (`Cube.011`-`Cube.019`) as the interior track | 0.033 / 0.004 (silhouette matches; the interior track is the railway icon's) |
| PlantCover | 0.67 | 985 | plate (scaled to 0.974, pose fitted, material hue corrected) | 0.010 / 0.004 (exact) |
| WaterBody | 0.82 | 618 | plate (scaled to 0.974, pose fitted, material hue corrected) | 0.015 / 0.004 (exact) |
| CityFurniture | (rig) | (rig) | original bench geometry found in `bench?.blend` (2022 working file): three seat slats, two back slats, four legs | — |

Notes:

- `icons.blend` also contains two large untextured cubes (`Cube.005`,
  `Cube.006`) and two `Surface` objects in `Collection 1`; they do not match
  any of the icons and were treated as unrelated leftovers.
- The plant and water plate colours were corrected per-channel (the albedo
  was fitted from the committed icons), which removed the previous hue
  mismatch; both now match closely.
- The tunnel icon was rebuilt to match the original design: the interior
  track is the railway icon's own geometry (`Cube.011`-`Cube.019`), and the
  tube is an open grey cylinder whose scale and pose were fitted to the
  icon's silhouette. The bench uses its original
  geometry and matches exactly.
- The pre-fix versions of the recreated assets remain in the gitignored
  `blend/*.blend1` backups.

## Redesigned icons (2026-08, shared rig)

Four weak icons were redesigned under the shared rig (world 0.82 / 300 W,
84 % normalized framing) so each has a distinct, readable silhouette at UI
sizes:

- **TransportSquare** — raised concrete plaza (light top, dark sides) with a
  central blue fountain and four corner bollards, replacing the featureless
  dark slab that was invisible on dark backgrounds.
- **TINRelief** — irregular faceted terrain patch (jittered 6×6 grid
  triangulation, flat-shaded, two hills) in an olive-green, replacing the
  smooth dome that read as generic foliage.
- **CityObjectGroup** — three distinct city objects (white house with blue
  roof, tree, grey block) in a loose cluster, replacing three
  interpenetrating grey boxes that read as a modelling error.
- **OtherConstruction** — a concrete silo (cylinder, dome, dark annex)
  replacing the abstract wall corner that was hard to name even at full
  size.

## New icons (2026-08)

Three new icons were designed and added for CityJSON 1.1.3 object types that
had no icon, and `Square` was renamed to `TransportSquare` (the CityJSON
name); `Track` was removed (not a CityJSON type); `ReliefFeature` was renamed
to `TINRelief` (the CityJSON name).

Note on type-name coverage vs CityJSON 1.1.3: the set matches fifteen of the
sixteen independent object types exactly. `GenericCityObject` is not a
CityJSON 1.1 type — 1.1 removed it in favour of `OtherConstruction` — but it
is a CityJSON 1.0/2.0 and CityGML type, so its icon is kept (azul supports
CityJSON 1.0 files too). The seventeen types without icons are all nested
sub-objects (parts, installations, constructive elements, furniture, rooms,
storeys, units, hollow spaces), which never appear as independent objects.

- **CityObjectGroup** — first version was three overlapping grey boxes; see
  *Redesigned icons* above for the current design.
- **OtherConstruction** — first version was a concrete corner of two walls;
  see *Redesigned icons* above for the current design.
- **Waterway** — a blue canal strip with grey banks, using the WaterBody
  water colour and a bank grey. Still on its original per-icon lighting;
  due to migrate to the shared rig.

Each was built in a fresh scene derived from the `WaterBody.blend` template
(same camera, light, world and render settings) and follows the same
per-file structure as the rest of the set.

## Rendering other sizes

The imagesets in the asset catalog store real 64/128/192 px renders in the
1x/2x/3x slots. To regenerate a variant, set the render resolution to 128 or
192 px (keeping all other settings) and render again.
