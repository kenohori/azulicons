# Azul icon Blender sources

Per-icon Blender source files that reproduce the existing 64×64 icons in
`../Assets.xcassets`. Each file is self-contained: opening it and pressing
Render (F12) writes `<icon>.png` next to the `.blend`, matching the icon that
is already in the asset catalog.

## Files

- **`<Icon>.blend`** — one per recoverable icon: `Building.blend`,
  `ReliefFeature.blend` (terrain), `road.blend`, `landuse.blend`,
  `Track.blend`, `bridge.blend`, `railway.blend`, `Square.blend`.
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
- The Building and road icons only match approximately (small residuals
  concentrated in shading and the road's lane markings); the other six render
  essentially pixel-perfect.

## Rendering other sizes

The imagesets in the asset catalog currently store three identical copies of
the 64×64 PNG for the 1x/2x/3x slots. To produce real variants, set the
render resolution to 128 or 192 px (keeping all other settings) and render
again.

## Missing sources

Six of the fourteen CityGML/CityJSON icons exist only as PNGs, without
Blender sources: `CityFurniture` (bench), `GenericCityObject`,
`PlantCover`, `SolitaryVegetationObject` (tree), `Tunnel` and `WaterBody`.
`Collection 1` of `icons.blend` contains leftover objects that may be their
remains — a green cone (possibly the tree crown), two untextured cubes, a
vertical cylinder and two Surface objects — but this is unconfirmed.
