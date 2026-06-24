# Schematics

Source for the circuit schematics on the site. These are **build inputs**, not
content — the committed SVGs under `docs/images/schematics/` are what the site
serves. Articles reference those SVGs by filename, so they never depend on this
tooling directly.

## How it fits together

```
schematics/
  style.py            # shared dark-theme styling — the ONE place colours live
  build.py            # regenerates every SVG from circuits/
  circuits/<name>.py  # one circuit per file, exposes build(path)
docs/images/schematics/<name>.svg   # generated output (committed, served by MkDocs)
```

## Regenerate all schematics

```bash
poetry run python schematics/build.py
```

Each `circuits/<name>.py` becomes `docs/images/schematics/<name>.svg`.

## Add a new schematic

1. Create `circuits/<name>.py` with a `build(path)` function (copy an existing
   one as a template).
2. Build **every** drawing through `dark_drawing()` from `style.py` — never use
   `schemdraw.Drawing` directly, or it renders black-on-white and looks broken
   on the dark theme.
3. Run the build command above.
4. **Check it's electrically correct, not just visually tidy.** schemdraw draws
   exactly what you tell it and performs no electrical check, so verify by eye:
   - **Battery / cell polarity** — the long plate is positive. `Battery().up()`
     puts the long (+) plate at the *bottom*; add `.reverse()` to put it on top.
   - **Polarized parts point the right way** — an LED or diode drawn pointing
     "down" only conducts with current flowing down through it. Make sure the
     positive terminal feeds the side current should enter, or the LED is
     reverse-biased and (in reality) wouldn't light.
   - **The loop actually closes** — source → load → back to source, no floating
     ends.
5. Reference it in an article:

   ```markdown
   <figure markdown>
     ![Alt text describing the circuit](../images/schematics/<name>.svg){ width="500" }
     <figcaption>Caption.</figcaption>
   </figure>
   ```

## Dependencies

`schemdraw` lives in the `schematics` Poetry group (build-time only — not needed
to serve the site, since the SVGs are committed):

```bash
poetry install --with schematics   # only when regenerating diagrams
```

## Migrating to another tool later

Articles reference SVG filenames, not this code. To switch tools, point a new
builder at the same output filenames in `docs/images/schematics/` and
re-implement the palette from `style.py`. The markdown never changes, and old
and new SVGs can coexist with no visual seam.
