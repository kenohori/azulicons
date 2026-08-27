# Azul icon Blender sources

Per-icon Blender source files for the icons in `../Assets.xcassets`. Each
file is self-contained: opening it and pressing Render (F12) writes
`<icon>.png` next to the `.blend`.

All sixteen icons use the shared lighting rig (2026-08): one world/point
light pair and normalized framing, so the set is uniformly lit and framed.
The historical per-icon fitted values that reproduced the pre-rig committed
PNGs are kept below for provenance only.

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
- `Light` — point light at (4.076, 1.005, 5.904), 300 W (shared rig).
- World background grey 0.82 (shared rig) — the dominant light.
- Render settings: Cycles, 512 samples, 64×64, transparent film, Standard
  view transform, RGBA PNG.

## Historical per-icon fitted lighting (pre-rig, provenance only)

Until 2026-08 each icon carried its own world/light pair, fitted numerically
(least squares in linear colour space) so a render reproduced the committed
PNG. All files now use the shared rig; these values are kept for reference.

| Icon                | World grey | Light (W) |
| ------------------- | ---------- | --------- |
| Building            | 0.85       | 176       |
| Road                | 0.173      | 81        |
| LandUse             | 0.85       | 366       |
| TINRelief           | 0.81       | 451       |
| Bridge              | 0.84       | 362       |
| Railway             | 0.82       | 421       |
| TransportSquare     | 0.81       | 0         |
| GenericCityObject   | 0.51       | 880       |
| SolitaryVegetationObject | 0.80  | 246       |
| Tunnel              | 0.26       | 464       |
| PlantCover          | 0.67       | 985       |
| WaterBody           | 0.82       | 618       |
| CityFurniture       | 0.81       | 441       |
| CityObjectGroup     | 0.51       | 880       |
| OtherConstruction   | 0.65       | 520       |
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
otherwise modelled from the committed renders, before the shared rig
existed. The world/light and fidelity columns below are historical; all six
are on the shared rig now.

| Icon | World grey | Light (W) | Based on |
| ---- | ---------- | --------- | -------- |
| GenericCityObject | 0.51 | 880 | cube from the icon, fitted in scale and pose |
| SolitaryVegetationObject | 0.80 | 246 | the original leftover `Cone` mesh from `icons.blend` `Collection 1` as the crown, trunk fitted underneath |
| Tunnel | 0.26 | 464 | open tube (fitted scale and pose) with the railway objects (`Cube.011`-`Cube.019`) as the interior track |
| PlantCover | 0.67 | 985 | plate (scaled to 0.974, pose fitted, material hue corrected) |
| WaterBody | 0.82 | 618 | plate (scaled to 0.974, pose fitted, material hue corrected) |
| CityFurniture | 0.81 | 441 | original bench geometry found in `bench?.blend` (2022 working file): three seat slats, two back slats, four legs |

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

Seven icons were redesigned under the shared rig (world 0.82 / 300 W,
84 % normalized framing) so each has a distinct, readable silhouette at UI
sizes. The first pass replaced the interchangeable grey shapes; the second
pass gave the flat surface plates internal detail and outline variation, so
no two icons share a silhouette any more.

- **TransportSquare** — raised concrete plaza (light top, dark sides) with a
  central blue fountain and four corner bollards, replacing the featureless
  dark slab that was invisible on dark backgrounds.
- **TINRelief** — irregular faceted terrain patch (jittered 6×6 grid
  triangulation, flat-shaded, two hills) in an olive-green, replacing the
  smooth dome that read as generic foliage.
- **CityObjectGroup** — three distinct city objects (white house with red
  roof — echoing the Building icon, tree, grey block) in a loose cluster,
  replacing three interpenetrating grey boxes that read as a modelling
  error.
- **OtherConstruction** — a concrete silo (cylinder, dome, dark annex)
  replacing the abstract wall corner that was hard to name even at full
  size.
- **PlantCover** — a green base with rounded bush mounds in three greens,
  replacing the flat plate that was silhouette-identical to WaterBody (and
  distinct from the single-tree cone of SolitaryVegetationObject).
- **WaterBody** — an irregular lake outline with a grey island and islet,
  replacing the flat blue square.
- **LandUse** — the four zoning quadrants kept but at stepped heights with
  thin grooves between them (a zoning-model look), replacing the perfectly
  flat four-colour checker.

The Building icon kept its 2016 logo geometry but was recoloured to cut the
number of blue icons in the set: roof red (the LandUse zone red), door
brown (the bench timber brown), window glass kept blue. The
CityObjectGroup mini-house roof follows the Building colour so the echo
stays consistent.

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
  water colour and a bank grey. Migrated to the shared rig in 2026-08,
  which also pulled the strip fully into frame.

Each was built in a fresh scene derived from the `WaterBody.blend` template
(same camera, light, world and render settings) and follows the same
per-file structure as the rest of the set.

## Rendering other sizes

The imagesets in the asset catalog store real 64/128/192 px renders in the
1x/2x/3x slots. To regenerate a variant, set the render resolution to 128 or
192 px (keeping all other settings) and render again.
