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
| road (refit)   | 0.173      | 81        |
| PlantCover     | 0.67       | 985       |
| WaterBody      | 0.82       | 618       |

Notes:

- The 100 W `Lamp` in `icons.blend` contributes nothing to renders (it is
  effectively invisible), so it is omitted from the per-icon files.
- `Track` and `Square` are lit purely by the world; their `Light` object is
  kept at 0 W for structural consistency and may be deleted.
- Both road materials render through the legacy `Diffuse BSDF` branch, not
  the Principled BSDF (the Principled sockets are inert in this file; the
  `active output` flag is misleading). The dash colour is 5.59, brighter
  than white, because the original dashes render about five times brighter
  than a white diffuse under the fitted lighting. The road's world/light
  pair was re-fitted against the committed icon in 2026-08; the surface
  keeps a small shading-gradient residual (interior MAE 0.022 in sRGB).
- The Building icon only matches approximately (a small residual concentrated
  in the shading); all other icons render essentially pixel-perfect (every
  icon is now at or below the 0.008 alpha error threshold, see the two tables
  below).

## Rendering other sizes

The imagesets in the asset catalog store real 64/128/192 px renders in the
1x/2x/3x slots. To regenerate a variant, set the render resolution to 128 or
192 px (keeping all other settings) and render again.

## Recreated icons

The last six icons were recreated from `icons.blend` leftovers where
possible and otherwise modelled from the committed renders. They use the
same camera and render settings as the other files.

| Icon | World grey | Light (W) | Based on | Fidelity (interior MAE / alpha MAE) |
| ---- | ---------- | --------- | -------- | ----------------------------------- |
| GenericCityObject | 0.51 | 880 | cube from the icon, fitted in scale and pose | 0.014 / 0.002 (exact) |
| SolitaryVegetationObject | 0.80 | 246 | the original leftover `Cone` mesh from `icons.blend` `Collection 1` as the crown, trunk fitted underneath | 0.015 / 0.006 |
| Tunnel | 0.26 | 464 | open tube (fitted scale and pose) with the railway objects (`Cube.011`-`Cube.019`) as the interior track | 0.033 / 0.004 (silhouette matches; the interior track is the railway icon's) |
| PlantCover | 0.67 | 985 | plate (scaled to 0.974, pose fitted, material hue corrected) | 0.010 / 0.004 (exact) |
| WaterBody | 0.82 | 618 | plate (scaled to 0.974, pose fitted, material hue corrected) | 0.015 / 0.004 (exact) |
| CityFurniture | 0.81 | 441 | original bench geometry found in `bench?.blend` (2022 working file): three seat slats, two back slats, four legs | 0.008 / 0.003 (exact) |

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
- The six recreated icons all started from fitted states; in 2026-08 the
  crown/trunk (SolitaryVegetationObject), tube pose (Tunnel), cube
  scale/pose (GenericCityObject) and plate pose/scale/materials
  (PlantCover, WaterBody) were re-fitted, plus the road lighting. The
  pre-fix versions of the six recreated assets remain in the gitignored
  `blend/*.blend1` backups.
- `bench?.blend` is a July-2022-era working file (same object-naming scheme as
  `icons.blend`) that turned out to contain the original CityFurniture bench
  (objects `Cube.020`–`Cube.024` and `Cylinder.002`–`Cylinder.005`).
