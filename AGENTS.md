# Agent guide for the azulicons repository

Assets for the [azul](https://github.com/tudelft3d/azul) 3D city model viewer:
an Xcode asset catalog with icons for the fourteen CityGML/CityJSON object
types, plus the Blender sources that reproduce them.

## Layout

- `Assets.xcassets/` — Xcode asset catalog. Each icon has its own imageset
  folder (e.g. `CityFurniture.imageset/`) with three PNGs for the 1x/2x/3x
  scales: real 64/128/192 px renders. `AppIcon.appiconset` holds the
  macOS/iOS app icon.
- `blend/<Icon>.blend` — per-icon Blender source, one per icon (all fourteen).
  Self-contained: a collection named after the icon holding the geometry, the
  render `Camera`, the `Light`, the fitted world color, and the render
  settings.
- `blend/README.md` — per-icon fitted lighting values and fidelity numbers.
  Read this before changing any blend file.
- `icons.blend` — combined working file: all icon scenes as collections in one
  shared (overlapping) world space; an icon is rendered by isolating its
  collection.
- `azul logo.blend` — the 2016 logo source (Blender 2.77); the Building icon
  geometry derives from it.
- `bench?.blend` — 2022-era working file containing the original CityFurniture
  bench (and other mid-edit objects). The `?` in the name is literal.

## Rendering an icon

Open `blend/<Icon>.blend` in Blender and press Render (F12), or:

```
/Applications/Blender.app/Contents/MacOS/Blender --background blend/<Icon>.blend \
  --python-expr "import bpy; bpy.ops.render.render(write_still=True)"
```

Renders are written to `//<Icon>.png`, next to the `.blend`. Settings: Cycles,
512 samples, 64×64, transparent film, Standard view transform, RGBA PNG. For
1x/2x/3x outputs, render at 64/128/192 px.

## Verification

To check a render matches the committed icon:

1. Render at 64×64.
2. Compare against `Assets.xcassets/<Icon>.imageset/<file>.png`. The alpha
   (silhouette) error should be ≤ 0.008; all fourteen icons currently pass,
   with per-icon interior color errors listed in `blend/README.md` (range
   ~0.0003–0.025 in sRGB MAE; Building and road are the two approximate
   ones).
3. If lighting needs re-fitting: render two basis images (world-only with the
   Light at 0 W, then Light-only with the world black), and least-squares fit
   the scale factors in linear sRGB space. The world color is the dominant
   light for most icons.

## Gotchas (learned the hard way)

- In background-mode Blender scripts, `bpy.context.view_layer.update()` is
  required after moving/scaling objects before projecting or rendering,
  otherwise stale `matrix_world` values are used.
- Setting `o.dimensions` in a background script can silently fail on some
  objects; prefer setting `o.scale` directly when in doubt.
- Save the file and render in a fresh session to be sure the saved state is
  what gets rendered.
- The `Lamp` in `icons.blend` contributes nothing to renders.
- In the road icon, both materials render through the legacy `Diffuse BSDF`
  branch, not the Principled BSDF (the `active output` flag in the file is
  misleading); the dash color is 5.59 (brighter than white) to match the
  original icon, and the surface color is 0.1523 under the re-fitted
  world 0.173 / 81 W lighting.
- Blender material colors are linear; PNG pixel values are sRGB — convert
  between the two.
- `icons.blend` `Collection 1` contains leftover objects, some of which are
  parts of old icons (the Cone is the tree crown; `Cylinder.001` is the
  tunnel tube). Do not delete objects that look unassigned without checking
  with the maintainer — an original working file was nearly lost this way.

## Conventions

- Icon sources live in `blend/<Icon>.blend`, named after the imageset folder.
- Keep per-icon files self-contained (geometry + camera + light + world +
  render settings in the file).
- One commit per logical change; no remote is configured, commits land on
  `main`.
