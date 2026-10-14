# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Personal academic website for Iury Simoes-Sousa (Physical and Computational Oceanographer), built with [Quarto](https://quarto.org/) and deployed to GitHub Pages.

## Environment and Commands

The project uses [pixi](https://pixi.sh/) for dependency management. Quarto, Python, scientific packages (xarray, matplotlib, hvplot, cdsapi, h5netcdf), and ImageMagick are managed as pixi dependencies.

- **Install environment:** `pixi install`
- **Preview locally:** `pixi run preview` (serves at `localhost:4242`)
- **Full render:** `pixi run render` — runs `quarto render`, then copies `resume/` and `pubs.bib` into `docs/`
- **Render single file:** `pixi run quarto render <file>.qmd`
- **Re-render with code execution:** `pixi run quarto render <file>.qmd --execute` (forces re-execution of Python cells, ignoring frozen cache)
- **Optimize new images:** `pixi run optimize-images` — converts any PNG/JPG in `img/research/` to WebP (max 1200px wide, quality 85) and removes the originals
- **Deploy:** Push to `main`; GitHub Actions (`.github/workflows/publish.yml`) renders and publishes to `gh-pages` branch automatically. CI does NOT re-execute Python code — it uses frozen outputs from `_freeze/`.

## Architecture

This is a Quarto website project (`project.type: website`) with output to `docs/`. Only `*.qmd` and `posts/**/*.qmd` are rendered (configured in `_quarto.yml` to exclude AGENTS.md etc.).

### Key Files

- `_quarto.yml` — site-wide config: light navbar, theme (`[cosmo, theme.scss]`), footer, Google Analytics, favicon
- `index.qmd` — landing page: `trestles` about hero, research-interest chips, and a "Recent news" table listing of the latest posts
- `research.qmd` — dedicated research page with Bootstrap image carousels for each topic
- `blog.qmd` — blog listing page, auto-discovers posts from `posts/` directory
- `publications.qmd` — renders bibliography via BibBase from `references.bib` (grouped by year, interactive)
- `theme.scss` — all custom styling (SCSS variables + rules): fonts, palette, navbar, carousels, booking/software/blog tweaks
- `posts/_metadata.yml` — shared blog post config: `freeze: true`

### Content Patterns

- **Blog posts** live in `posts/<slug>/index.qmd` with YAML frontmatter (`title`, `author`, `date`, `categories`)
- **Computational blog posts** use Python code cells in `.qmd` files. The pixi environment provides Python + scientific packages. Outputs are frozen in `_freeze/` so CI doesn't need Python. Use `--execute` flag to re-render after code changes. Delete cached data files in the post directory if download parameters change.
- **Interactive plots** use `hvplot.xarray` with Bokeh backend. Import `hvplot.xarray` to register the `.hvplot` accessor on xarray objects. Use `holoviews` for layout composition (`+` for side-by-side, `.cols(1)` for vertical stacking, `.opts(sublabel_format="")` to remove a/b/c labels).
- **ERA5 data downloads** use `reanalysis-era5-single-levels-timeseries` product (optimized for point time series). Requires `~/.cdsapirc` with CDS API key. The product uses `location: {latitude: ..., longitude: ...}` and `date: ["YYYY-MM-DD/YYYY-MM-DD"]` instead of area/year/month/day. Returns a zip containing a NetCDF that must be extracted.
- **Research images** are WebP files in `img/research/`, displayed via Bootstrap carousels in `research.qmd`. Run `pixi run optimize-images` after adding new PNG/JPG images. For GIFs, convert to MP4 with ffmpeg and use a `<video>` tag instead of `<img>`.
- **CV** is a static PDF at `resume/CV.pdf`, linked from the navbar (direct GitHub raw link, not served from the site)
- **Publications** are driven by `references.bib` rendered via external BibBase script (grouped by year, interactive collapse). User prefers BibBase over Quarto's native bibliography for the interactive grouping.

### Styling Notes

- Minimalist look: white background, light navbar with a hairline border, no title banners (`title-block-banner: false` globally)
- Fonts: Inter (body/UI) + Source Serif 4 (headings), loaded from Google Fonts in `theme.scss`
- Palette: ink `#1d2733`, muted `#5f6b78`, hairlines `#e6e9ed`, single accent `#0b5f86` (ocean blue)
- Carousels: thin border, muted caption strip below the image with the prev/next arrows inside it (responsive heights 460/300/200px)
- Post computational output is frozen by default (`freeze: true` in `posts/_metadata.yml`)

### Workflow Notes

- There is an open PR (`website-redesign` branch) with the theme/image/restructuring changes. The ERA5 tutorial post is being developed on this branch.
- `pixi.toml` has `win-64` in platforms but `imagemagick` is excluded from Windows (not available on conda-forge for Windows)
- The `render` pixi task copies `resume/` and `pubs.bib` to `docs/` but this is only needed for local builds — CI publishes directly to `gh-pages`

### Recent Updates

- Added a dedicated scheduling page at `booking.qmd`, exposed in the navbar as `Schedule`, using an embedded Google Calendar appointment iframe.
- Added a `Software` navbar tab and `software.qmd`. Current entries include:
  - `Where is SWOT?` (Hugging Face Space) with a clickable preview image from `img/software/whereisswot.png`
  - hvPlot/xarray tutorial on plotting large vector fields
  - Earthmover blog post on Icechunk optimization with a clickable preview image from `img/software/earthmover_blog.jpg`
- Added `img/research/eddy_578618_composite.png` to the `Multiscale Oceanographic Datasets for Investigating Ocean Dynamics` carousel in `research.qmd`.
- Added short news-style blog posts for featured media/research coverage:
  - `posts/saving-tico/index.qmd`
  - `posts/southbrazilflood/index.qmd`
  - `posts/radionovelo_tico/index.qmd`
- For these announcement posts, use the publication date of the media feature or podcast episode, not necessarily the scientific paper date.
- Blog post images are now centered globally via `styles.css` using Quarto post selectors, so standalone images in posts do not need custom alignment markup.
- New post asset folders added in this session:
  - `posts/saving-tico/`
  - `posts/southbrazilflood/`
  - `posts/radionovelo_tico/`
- Quarto single-page renders work for verification, but sandboxed runs may intermittently fail on temporary/cache paths under `.quarto/`; rerunning with escalation resolved those verification cases.
