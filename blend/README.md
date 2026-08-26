# Azul icon Blender sources

Per-icon Blender source files that reproduce the existing 64×64 icons in
`../Assets.xcassets`. Each file is self-contained: opening it and pressing
Render (F12) writes `<icon>.png` next to the `.blend`, matching the icon that
is already in the asset catalog.

## Files

- **`<Icon>.blend`** — one per icon, all fourteen CityGML/CityJSON types:
  `Building.blend`, `ReliefFeature.blend` (terrain), `road.blend`,
  `landuse.blend`, `Track.blend`, `bridge.blend`, `railway.blend`,
  `Square.blend`, `GenericCityObject.blend`, `SolitaryVegetationObject.blend`,
  `Tunnel.blend`, `PlantCover.blend`, `WaterBody.blend`, `CityFurniture.blend`.
- **`../icons.blend`** — the combined working file containing all eight icon
  scenes as collections, plus camera and lights. The icon scenes overlap in
  world space, so an icon is rendered by isolating its collection.
- **`../azul logo.blend`** — the original Azul logo source (Blender 2.77,
  2016). The Building icon geometry is the same house it contains.

## Structure of each file

- One collection (named after the icon) containing the icon geometry.
- `Camera` — render camera (35 mm, standard icon pose).
- `Light` — point light with the per-icon energy from the table below.
- World background grey from the table below — for most icons this is the
  dominant light.
- Render settings: Cycles, 512 samples, 64×64, transparent film, Standard
  view transform, RGBA PNG.

## Fitted lighting values

The current lighting state of `icons.blend` (dark world, 1000 W Light) does
not produce the existing icons. The values below were fitted numerically per
icon (least squares in linear colour space) so that a render reproduces the
committed PNG:

| Icon           | World grey | Light (W) |
| -------------- | ---------- | --------- |
| Building       | 0.85       | 176       |
| road           | 0.029      | 564       |
| landuse        | 0.85       | 366       |
| ReliefFeature  | 0.81       | 451       |
| Track          | 0.81       | 0         |
| bridge         | 0.84       | 362       |
| railway        | 0.82       | 421       |
| Square         | 0.81       | 0         |

Notes:

- The 100 W `Lamp` in `icons.blend` contributes nothing to renders (it is
  effectively invisible), so it is omitted from the per-icon files.
- `Track` and `Square` are lit purely by the world; their `Light` object is
  kept at 0 W for structural consistency and may be deleted.
- The road lane markings use a legacy diffuse shader (the `Diffuse BSDF`
  branch of the material — that is the node path the render actually uses,
  not the Principled BSDF); its colour is set to 5.59, brighter than white,
  because the original dashes render about five times brighter than a white
  diffuse under the fitted lighting.
- The Building icon only matches approximately (a small residual concentrated
  in the shading); the other seven icons render essentially pixel-perfect.

## Rendering other sizes

The imagesets in the asset catalog currently store three identical copies of
the 64×64 PNG for the 1x/2x/3x slots. To produce real variants, set the
render resolution to 128 or 192 px (keeping all other settings) and render
again.

## Recreated icons

The last six icons were recreated from `icons.blend` leftovers where
possible and otherwise modelled from the committed renders. They use the
same camera and render settings as the other files.

| Icon | World grey | Light (W) | Based on | Fidelity (interior MAE) |
| ---- | ---------- | --------- | -------- | ----------------------- |
| GenericCityObject | 0.51 | 880 | cube modelled from the icon | 0.014 (exact) |
| SolitaryVegetationObject | 0.80 | 246 | the leftover green cone in `collection 1` as the crown | 0.020 (crown exact; trunk simplified) |
| Tunnel | 0.76 | 0 | the leftover cylinder reworked as an open tube with a track inside | 0.068 (close; interior approximate) |
| PlantCover | 0.67 | 985 | plate, same as the Square icon | 0.035 |
| WaterBody | 0.82 | 618 | plate, same as the Square icon | 0.034 |
| CityFurniture | 0.51 | 593 | bench modelled from the icon (seat, back, legs) | 0.047 (structure matches; proportions approximate) |

Notes:

- `icons.blend` also contains two large untextured cubes (`Cube.005`,
  `Cube.006`) and two `Surface` objects in `Collection 1`; they do not match
  any of the icons and were treated as unrelated leftovers.
- The tunnel, plant, water and bench lighting still match only
  approximately; the values above are the fitted best match.
