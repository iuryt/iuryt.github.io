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
- **Regenerate icons and link-preview images:** `pixi run social-images` — rebuilds `favicon.svg`/`favicon.png`/`apple-touch-icon.png` (eddy spiral), the site card `img/social/card.jpg` (from `profile.jpg`), and one card per research project in `img/social/` (first gallery image), updating each project's `image:`. Run after changing the photo, title/role, or a project's first figure. Fonts are downloaded to `.cache/` (gitignored); scripts live in `scripts/`
- **Optimize new images:** `pixi run optimize-images` — converts any PNG/JPG in `img/research/` to WebP (max 1200px wide, quality 85) and removes the originals
- **Deploy:** Push to `main`; GitHub Actions (`.github/workflows/publish.yml`) renders and publishes to `gh-pages` branch automatically. CI does NOT re-execute Python code — it uses frozen outputs from `_freeze/`.

## Architecture

This is a Quarto website project (`project.type: website`) with output to `docs/`. Only `*.qmd` and `posts/**/*.qmd` are rendered (configured in `_quarto.yml` to exclude AGENTS.md etc.).

### Key Files

- `_quarto.yml` — site-wide config: light navbar, theme (`[cosmo, theme.scss]`), footer, Google Analytics, favicon, Open Graph / Twitter Card link previews (default image `img/social/card.jpg`, 1200×630; the home page sets its own `open-graph`/`twitter-card` title and image; project pages use their `img/social/<slug>.jpg`). Use JPG/PNG for preview images — WhatsApp/LinkedIn may not render WebP. `_includes/icons.html` adds the SVG favicon and the iOS home-screen icon
- `index.qmd` — landing page: `trestles` about hero, research-interest chips, and a "Recent news" table listing of the latest posts
- `research.qmd` — research page organized by three lines (Data-driven / Dynamics / Impacts, plus Teaching), each a Quarto grid listing of cards pulled from `research/<line>-*.qmd` (sorted by an `order` field)
- `research/*.qmd` — one subpage per project. Front matter: `title`, `subtitle` (research line), `description`, `image` (social/fallback), `body-classes` (line color), `order`, and `gallery:` — a list of `{src: ../img/research/..., caption: "..."}` (`.mp4` sources render as autoplaying video). The page body uses `{{< gallery >}}` to render the gallery as a carousel. **To add a figure to a project, add one item to its `gallery:` list** — both the project page and its card on the Research page update.
- `_extensions/gallery/gallery.lua` — the `{{< gallery >}}` shortcode: Bootstrap carousel (or a single figure) with `<a class="lightbox">` links for click-to-zoom. GLightbox is loaded from cdnjs via `research/_metadata.yml` → `research/_lightbox.html`. Galleries break out of the text column (up to 1100px wide, 620px tall; 320px on mobile)
- `research-cards.ejs` — custom listing template for the Research page: each card is an auto-advancing, fading mini-carousel of the project's `gallery` (intervals staggered per card). Output is wrapped in a ```` ```{=html} ```` fence because Quarto parses listing-template output as Markdown (indented HTML would become a code block). The grid is CSS grid (`.research-cards`, 3/2/1 columns), since Quarto's Bootstrap build lacks `row-cols-*`
- `research.qmd` uses `page-layout: full` + `body-classes: research-wide` (capped at 1120px) so cards are larger
- `group.qmd` — group page: people + "Join us" (grad students, postdocs, undergrads, how to get in touch by email)
- `blog.qmd` — blog listing page, auto-discovers posts from `posts/` directory
- `publications.qmd` — hand-curated "Selected publications" (one per research line) on top, then the full BibBase list from `references.bib` (BibBase reads the file from the `main` branch on GitHub), restyled via `.bibbase-wrap` rules in `theme.scss`
- `theme.scss` — all custom styling (SCSS variables + rules): fonts, palette, navbar, carousels, booking/software/blog tweaks
- `posts/_metadata.yml` — shared blog post config: `freeze: true`

### Content Patterns

- **Blog posts** live in `posts/<slug>/index.qmd` with YAML frontmatter (`title`, `author`, `date`, `categories`)
- **Computational blog posts** use Python code cells in `.qmd` files. The pixi environment provides Python + scientific packages. Outputs are frozen in `_freeze/` so CI doesn't need Python. Use `--execute` flag to re-render after code changes. Delete cached data files in the post directory if download parameters change.
- **Interactive plots** use `hvplot.xarray` with Bokeh backend. Import `hvplot.xarray` to register the `.hvplot` accessor on xarray objects. Use `holoviews` for layout composition (`+` for side-by-side, `.cols(1)` for vertical stacking, `.opts(sublabel_format="")` to remove a/b/c labels).
- **ERA5 data downloads** use `reanalysis-era5-single-levels-timeseries` product (optimized for point time series). Requires `~/.cdsapirc` with CDS API key. The product uses `location: {latitude: ..., longitude: ...}` and `date: ["YYYY-MM-DD/YYYY-MM-DD"]` instead of area/year/month/day. Returns a zip containing a NetCDF that must be extracted.
- **Research images** are WebP files in `img/research/`, displayed via Bootstrap carousels in the `research/*.qmd` project pages (paths are `../img/research/...`). Run `pixi run optimize-images` after adding new PNG/JPG images. For GIFs, convert to MP4 with ffmpeg and use a `<video>` tag instead of `<img>`.
- **CV** is a static PDF at `resume/CV.pdf`, linked from the navbar (direct GitHub raw link, not served from the site)
- **Publications** are driven by `references.bib` rendered via external BibBase script (grouped by year, interactive collapse). User prefers BibBase over Quarto's native bibliography for the interactive grouping.

### Styling Notes

- Minimalist look: white background, light navbar with a hairline border, no title banners (`title-block-banner: false` globally)
- Fonts: Inter (body/UI) + Source Serif 4 (headings), loaded from Google Fonts in `theme.scss`
- Palette: ink `#1d2733`, muted `#5f6b78`, hairlines `#e6e9ed`, accent `#0b5f86` (ocean blue)
- Research-line color coding: Data-driven = blue `#0b5f86`, Dynamics = sea green `#2a9d8f`, Impacts = coral `#e76f51` (darker `*-text` shades for small labels). Classes `.line-data` / `.line-dyn` / `.line-imp` set CSS variables `--line`, `--line-text`, `--line-tint`; used on the research-line blocks, selected publications, research section headings/cards, and project subpages (`body-classes` in their front matter). Active navbar item has a coral underline.
- Carousels: thin border, muted caption strip below the image with the prev/next arrows inside it (responsive heights 460/300/200px)
- Post computational output is frozen by default (`freeze: true` in `posts/_metadata.yml`)

### Workflow Notes

- There is an open PR (`website-redesign` branch) with the theme/image/restructuring changes. The ERA5 tutorial post is being developed on this branch.
- `pixi.toml` has `win-64` in platforms but `imagemagick` is excluded from Windows (not available on conda-forge for Windows)
- The `render` pixi task copies `resume/` and `pubs.bib` to `docs/` but this is only needed for local builds — CI publishes directly to `gh-pages`

### Recent Updates

- The scheduling page (`booking.qmd`) was removed; contact is by email (see `group.qmd`).
- `references.bib` uses CRLF line endings — preserve them when editing, or the whole file shows as changed in git.
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
