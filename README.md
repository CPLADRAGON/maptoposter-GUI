# City Map Poster Generator GUI

Generate beautiful, minimalist map posters for any city in the world.

This fork adds a dark-mode PyQt6 desktop GUI on top of the original command-line generator. The original CLI workflow is still available.

## Added in this GUI Fork

- **Dark-mode desktop GUI** built with PyQt6.
- **Same core poster generator** as the CLI, using OpenStreetMap data through OSMnx.
- **Form-based controls** for city, country, coordinates, theme, distance, poster size, output format, display labels, and custom fonts.
- **Live theme preview** with palette swatches before generation.
- **Fast preview defaults** for quicker iteration with smaller map radius and canvas size.
- **Background generation worker** so the UI stays responsive while downloading and rendering.
- **Progress and cancellation controls** with clear status messages.
- **Zoomable and draggable PNG preview** after generation.
- **Saved-file actions**: show full output path, open file, open folder, and copy path.
- **Optional GUI dependency** so CLI-only users do not need PyQt6.

<img src="posters/singapore_neon_cyberpunk_20260118_153328.png" width="250">
<img src="posters/dubai_midnight_blue_20260118_140807.png" width="250">

## Examples

| Country      | City           | Theme           | Poster |
|:------------:|:--------------:|:---------------:|:------:|
| USA          | San Francisco  | sunset          | <img src="posters/san_francisco_sunset_20260118_144726.png" width="250"> |
| Spain        | Barcelona      | warm_beige      | <img src="posters/barcelona_warm_beige_20260118_140048.png" width="250"> |
| Italy        | Venice         | blueprint       | <img src="posters/venice_blueprint_20260118_140505.png" width="250"> |
| Japan        | Tokyo          | japanese_ink    | <img src="posters/tokyo_japanese_ink_20260118_142446.png" width="250"> |
| India        | Mumbai         | contrast_zones  | <img src="posters/mumbai_contrast_zones_20260118_145843.png" width="250"> |
| Morocco      | Marrakech      | terracotta      | <img src="posters/marrakech_terracotta_20260118_143253.png" width="250"> |
| Singapore    | Singapore      | neon_cyberpunk  | <img src="posters/singapore_neon_cyberpunk_20260118_153328.png" width="250"> |
| Australia    | Melbourne      | forest          | <img src="posters/melbourne_forest_20260118_153446.png" width="250"> |
| UAE          | Dubai          | midnight_blue   | <img src="posters/dubai_midnight_blue_20260118_140807.png" width="250"> |
| USA          | Seattle        | emerald         | <img src="posters/seattle_emerald_20260124_162244.png" width="250"> |

## Installation

### GUI Fork Quick Start

```bash
git clone https://github.com/CPLADRAGON/maptoposter-GUI.git
cd maptoposter-GUI
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m pip install "PyQt6>=6.7"
.\run_gui.ps1
```

On macOS/Linux, activate the virtual environment and run:

```bash
python -m maptoposter_gui.app
```

### With uv (Recommended)

Make sure [uv](https://docs.astral.sh/uv/) is installed. Running the script by prepending `uv run` automatically creates and manages a virtual environment.

```bash
# First run will automatically install dependencies
uv run ./create_map_poster.py --city "Paris" --country "France"

# Or sync dependencies explicitly first (using locked versions)
uv sync --locked
uv run ./create_map_poster.py --city "Paris" --country "France"
```

### With pip + venv

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Desktop GUI

The GUI is an optional PyQt6 desktop interface for generating posters without typing CLI commands. It uses a dark-mode-first design with elevated dark surfaces, off-white text, accessible focus states, live theme swatches, background generation, progress updates, and inline PNG preview.

#### Install GUI Dependencies

Install GUI dependencies with uv:

```bash
uv sync --extra gui
uv run maptoposter-gui
```

Or with pip + venv:

```bash
pip install -r requirements.txt
pip install "PyQt6>=6.7"
.venv\Scripts\python -m maptoposter_gui.app
```

#### Launch the GUI

On Windows, you can also launch the GUI from PowerShell with:

```powershell
.\run_gui.ps1
```

If you see `ModuleNotFoundError` for packages such as `lat_lon_parser`, you are likely using your global Python instead of the virtual environment. Use `run_gui.ps1` or `.venv\Scripts\python -m maptoposter_gui.app` from the project root.

#### GUI User Manual

1. **Enter location**
    - Fill in **City** and **Country**.
    - Optional: use **Latitude** and **Longitude** together to override the geocoded map center.

2. **Choose poster settings**
    - Pick a **Theme** from the dropdown.
    - Use **Fast preview defaults** while experimenting. This sets a smaller radius and canvas for quicker generation.
    - Adjust **Distance** to control how much of the city is included.
    - Adjust **Width** and **Height** in inches.
    - Select output **Format**: `png`, `svg`, or `pdf`.

3. **Customize text**
    - Optional **Display city** and **Display country** fields change the text printed on the poster.
    - Optional **Country label** overrides the country label shown on the poster.
    - Optional **Font family** downloads a Google Font, useful for non-Latin scripts.

4. **Preview the theme**
    - The right panel shows the selected theme name, description, and color swatches.
    - Changing the theme updates the swatches immediately without downloading map data.

5. **Generate**
    - Click **Generate Poster**.
    - The app downloads OpenStreetMap data, renders the poster, and saves it to `posters/`.
    - The UI remains responsive during generation.

6. **Cancel if needed**
    - Click **Cancel** to request cancellation.
    - Cancellation is cooperative: it stops at the next safe checkpoint and may wait for the current OpenStreetMap or rendering operation to finish.

7. **Review output**
    - PNG files appear in the preview panel.
    - Use mouse wheel or the `+` / `-` buttons to zoom.
    - Drag the poster to pan while zoomed.
    - Click **Fit** to reset the preview.
    - SVG and PDF files are saved and can be opened externally.

8. **Find the saved file**
    - The GUI shows the full saved file path after generation.
    - Use **Open File**, **Open Folder**, or **Copy Path** from the preview panel.

#### GUI Controls Reference

| Control | Purpose | Tip |
|---------|---------|-----|
| City / Country | Location to geocode | Required unless future coordinate-only mode is added |
| Latitude / Longitude | Manual center override | Must be provided together |
| Theme | Poster color theme | Preview swatches update instantly |
| Fast preview defaults | Smaller/faster working settings | Recommended while experimenting |
| Distance | Map radius in meters | 4000-8000m is faster; 15000m+ can be slow |
| Width / Height | Output size in inches | Max 20 inches each |
| Format | `png`, `svg`, or `pdf` | PNG supports inline preview |
| Display city / country | Poster label override | Useful for native/localized names |
| Font family | Google Font family | Useful for CJK, Arabic, Thai, Khmer, etc. |

#### Output Location

Posters are saved to `posters/` with filenames like:

```text
{city}_{theme}_{YYYYMMDD_HHMMSS}.{format}
```

The GUI also displays the exact saved path after generation.

Performance note: the first street-network step uses a single blocking OpenStreetMap/Overpass request through OSMnx, so progress may appear paused while the remote service responds. Use **Fast preview defaults** or keep distance around 4000-8000m while iterating. Larger radii such as 15000-20000m download much more map data and can take several minutes, especially for dense cities.

#### Troubleshooting

| Problem | What to do |
|---------|------------|
| `ModuleNotFoundError` when launching | Run with `.venv\Scripts\python -m maptoposter_gui.app` or `run_gui.ps1` |
| Street network download stays at the same progress value | Wait, or reduce distance. The OSMnx street-network request is blocking and can take minutes |
| Output preview is blank for SVG/PDF | Use **Open File**. Inline preview is currently PNG-focused |
| Generate button is hard to see | Use the latest fork version; the action bar is pinned near the top |
| Poster is too slow to iterate on | Enable **Fast preview defaults**, then increase distance/size for final output |

### Generate Poster

If you're using `uv`:

```bash
uv run ./create_map_poster.py --city <city> --country <country> [options]
```

Otherwise (pip + venv):

```bash
python create_map_poster.py --city <city> --country <country> [options]
```

### Required Options

| Option | Short | Description |
|--------|-------|-------------|
| `--city` | `-c` | City name (used for geocoding) |
| `--country` | `-C` | Country name (used for geocoding) |

### Optional Flags

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| **OPTIONAL:** `--latitude` | `-lat` | Override latitude center point (use with --longitude) | |
| **OPTIONAL:** `--longitude` | `-long` | Override longitude center point (use with --latitude) | |
| **OPTIONAL:** `--country-label` | | Override country text displayed on poster | |
| **OPTIONAL:** `--theme` | `-t` | Theme name | terracotta |
| **OPTIONAL:** `--distance` | `-d` | Map radius in meters | 18000 |
| **OPTIONAL:** `--list-themes` | | List all available themes | |
| **OPTIONAL:** `--all-themes` | | Generate posters for all available themes | |
| **OPTIONAL:** `--width` | `-W` | Image width in inches | 12 (max: 20) |
| **OPTIONAL:** `--height` | `-H` | Image height in inches | 16 (max: 20) |

### Multilingual Support - i18n

Display city and country names in your language with custom fonts from google fonts:

| Option | Short | Description |
|--------|-------|-------------|
| `--display-city` | `-dc` | Custom display name for city (e.g., "東京") |
| `--display-country` | `-dC` | Custom display name for country (e.g., "日本") |
| `--font-family` | | Google Fonts family name (e.g., "Noto Sans JP") |

**Examples:**

```bash
# Japanese
python create_map_poster.py -c "Tokyo" -C "Japan" -dc "東京" -dC "日本" --font-family "Noto Sans JP"

# Korean
python create_map_poster.py -c "Seoul" -C "South Korea" -dc "서울" -dC "대한민국" --font-family "Noto Sans KR"

# Arabic
python create_map_poster.py -c "Dubai" -C "UAE" -dc "دبي" -dC "الإمارات" --font-family "Cairo"
```

**Note**: Fonts are automatically downloaded from Google Fonts and cached locally in `fonts/cache/`.

### Resolution Guide (300 DPI)

Use these values for `-W` and `-H` to target specific resolutions:

| Target | Resolution (px) | Inches (-W / -H) |
|--------|-----------------|------------------|
| **Instagram Post** | 1080 x 1080 | 3.6 x 3.6 |
| **Mobile Wallpaper** | 1080 x 1920 | 3.6 x 6.4 |
| **HD Wallpaper** | 1920 x 1080 | 6.4 x 3.6 |
| **4K Wallpaper** | 3840 x 2160 | 12.8 x 7.2 |
| **A4 Print** | 2480 x 3508 | 8.3 x 11.7 |

### Usage Examples

#### Basic Examples

```bash
# Simple usage with default theme
python create_map_poster.py -c "Paris" -C "France"

# With custom theme and distance
python create_map_poster.py -c "New York" -C "USA" -t noir -d 12000
```

#### Multilingual Examples (Non-Latin Scripts)

Display city names in their native scripts:

```bash
# Japanese
python create_map_poster.py -c "Tokyo" -C "Japan" -dc "東京" -dC "日本" --font-family "Noto Sans JP" -t japanese_ink

# Korean
python create_map_poster.py -c "Seoul" -C "South Korea" -dc "서울" -dC "대한민국" --font-family "Noto Sans KR" -t midnight_blue

# Thai
python create_map_poster.py -c "Bangkok" -C "Thailand" -dc "กรุงเทพมหานคร" -dC "ประเทศไทย" --font-family "Noto Sans Thai" -t sunset

# Arabic
python create_map_poster.py -c "Dubai" -C "UAE" -dc "دبي" -dC "الإمارات" --font-family "Cairo" -t terracotta

# Chinese (Simplified)
python create_map_poster.py -c "Beijing" -C "China" -dc "北京" -dC "中国" --font-family "Noto Sans SC"

# Khmer
python create_map_poster.py -c "Phnom Penh" -C "Cambodia" -dc "ភ្នំពេញ" -dC "កម្ពុជា" --font-family "Noto Sans Khmer"
```

#### Advanced Examples

```bash
# Iconic grid patterns
python create_map_poster.py -c "New York" -C "USA" -t noir -d 12000           # Manhattan grid
python create_map_poster.py -c "Barcelona" -C "Spain" -t warm_beige -d 8000   # Eixample district

# Waterfront & canals
python create_map_poster.py -c "Venice" -C "Italy" -t blueprint -d 4000       # Canal network
python create_map_poster.py -c "Amsterdam" -C "Netherlands" -t ocean -d 6000  # Concentric canals
python create_map_poster.py -c "Dubai" -C "UAE" -t midnight_blue -d 15000     # Palm & coastline

# Radial patterns
python create_map_poster.py -c "Paris" -C "France" -t pastel_dream -d 10000   # Haussmann boulevards
python create_map_poster.py -c "Moscow" -C "Russia" -t noir -d 12000          # Ring roads

# Organic old cities
python create_map_poster.py -c "Tokyo" -C "Japan" -t japanese_ink -d 15000    # Dense organic streets
python create_map_poster.py -c "Marrakech" -C "Morocco" -t terracotta -d 5000 # Medina maze
python create_map_poster.py -c "Rome" -C "Italy" -t warm_beige -d 8000        # Ancient layout

# Coastal cities
python create_map_poster.py -c "San Francisco" -C "USA" -t sunset -d 10000    # Peninsula grid
python create_map_poster.py -c "Sydney" -C "Australia" -t ocean -d 12000      # Harbor city
python create_map_poster.py -c "Mumbai" -C "India" -t contrast_zones -d 18000 # Coastal peninsula

# River cities
python create_map_poster.py -c "London" -C "UK" -t noir -d 15000              # Thames curves
python create_map_poster.py -c "Budapest" -C "Hungary" -t copper_patina -d 8000  # Danube split

# Override center coordinates
python create_map_poster.py --city "New York" --country "USA" -lat 40.776676 -long -73.971321 -t noir

# List available themes
python create_map_poster.py --list-themes

# Generate posters for every theme
python create_map_poster.py -c "Tokyo" -C "Japan" --all-themes
```

### Distance Guide

| Distance | Best for |
|----------|----------|
| 4000-6000m | Small/dense cities (Venice, Amsterdam center) |
| 8000-12000m | Medium cities, focused downtown (Paris, Barcelona) |
| 15000-20000m | Large metros, full city view (Tokyo, Mumbai) |

## Themes

17 themes available in `themes/` directory:

| Theme | Style |
|-------|-------|
| `gradient_roads` | Smooth gradient shading |
| `contrast_zones` | High contrast urban density |
| `noir` | Pure black background, white roads |
| `midnight_blue` | Navy background with gold roads |
| `blueprint` | Architectural blueprint aesthetic |
| `neon_cyberpunk` | Dark with electric pink/cyan |
| `warm_beige` | Vintage sepia tones |
| `pastel_dream` | Soft muted pastels |
| `japanese_ink` | Minimalist ink wash style |
| `emerald`      | Lush dark green aesthetic |
| `forest` | Deep greens and sage |
| `ocean` | Blues and teals for coastal cities |
| `terracotta` | Mediterranean warmth |
| `sunset` | Warm oranges and pinks |
| `autumn` | Seasonal burnt oranges and reds |
| `copper_patina` | Oxidized copper aesthetic |
| `monochrome_blue` | Single blue color family |

## Output

Posters are saved to `posters/` directory with format:

```text
{city}_{theme}_{YYYYMMDD_HHMMSS}.png
```

## Adding Custom Themes

Create a JSON file in `themes/` directory:

```json
{
  "name": "My Theme",
  "description": "Description of the theme",
  "bg": "#FFFFFF",
  "text": "#000000",
  "gradient_color": "#FFFFFF",
  "water": "#C0C0C0",
  "parks": "#F0F0F0",
  "road_motorway": "#0A0A0A",
  "road_primary": "#1A1A1A",
  "road_secondary": "#2A2A2A",
  "road_tertiary": "#3A3A3A",
  "road_residential": "#4A4A4A",
  "road_default": "#3A3A3A"
}
```

## Project Structure

```text
map_poster/
├── create_map_poster.py       # Original CLI script
├── font_management.py         # Font loading and Google Fonts integration
├── maptoposter_core/          # Shared request/theme/generator interfaces used by GUI
├── maptoposter_gui/           # PyQt6 desktop application
│   ├── app.py                 # GUI entry point
│   ├── main_window.py         # Main window and form workflow
│   ├── widgets.py             # Theme swatches and zoomable poster preview
│   ├── worker.py              # Background generation worker
│   └── style.py               # Dark-mode style tokens and stylesheet
├── run_gui.ps1                # Windows launcher using the local virtual environment
├── themes/                    # Theme JSON files
├── fonts/                     # Font files
│   ├── Roboto-*.ttf           # Default Roboto fonts
│   └── cache/                 # Downloaded Google Fonts (auto-generated)
├── posters/                   # Generated posters
└── README.md
```


## Hacker's Guide

Quick reference for contributors who want to extend or modify the script.

### Contributors Guide

- Bug fixes are welcomed
- Don't submit user interface (web/desktop)
- Don't Dockerize for now
- If you vibe code any fix please test it and see before and after version of poster
- Before embarking on a big feature please ask in Discussions/Issue if it will be merged

### Architecture Overview

The original CLI pipeline remains intact. The GUI fork adds a thin desktop layer around shared generation interfaces.

```text
┌─────────────────┐     ┌──────────────┐     ┌─────────────────┐
│   CLI Parser    │────▶│  Geocoding   │────▶│  Data Fetching  │
│   (argparse)    │     │  (Nominatim) │     │    (OSMnx)      │
└─────────────────┘     └──────────────┘     └─────────────────┘
                                                     │
                        ┌──────────────┐             ▼
                        │    Output    │◀────┌─────────────────┐
                        │  (matplotlib)│     │   Rendering     │
                        └──────────────┘     │  (matplotlib)   │
                                             └─────────────────┘
```

GUI architecture:

```text
┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│ PyQt6 Main Window  │────▶│ Generation Worker  │────▶│ MapPosterGenerator │
│ forms + preview    │     │ QThread background │     │ shared core API    │
└────────────────────┘     └────────────────────┘     └────────────────────┘
          │                                                     │
          ▼                                                     ▼
┌────────────────────┐                              ┌────────────────────┐
│ Theme Swatch Card  │                              │ Legacy Renderer    │
│ Preview / actions  │                              │ matplotlib + OSMnx │
└────────────────────┘                              └────────────────────┘
```

### Key Functions

| Function | Purpose | Modify when... |
|----------|---------|----------------|
| `get_coordinates()` | City → lat/lon via Nominatim | Switching geocoding provider |
| `create_poster()` | Main rendering pipeline | Adding new map layers |
| `get_edge_colors_by_type()` | Road color by OSM highway tag | Changing road styling |
| `get_edge_widths_by_type()` | Road width by importance | Adjusting line weights |
| `create_gradient_fade()` | Top/bottom fade effect | Modifying gradient overlay |
| `load_theme()` | JSON theme → dict | Adding new theme properties |
| `is_latin_script()` | Detects script for typography | Supporting new scripts |
| `load_fonts()` | Load custom/default fonts | Changing font loading logic |

### GUI Components

| File | Purpose | Modify when... |
|------|---------|----------------|
| `maptoposter_gui/app.py` | Starts the PyQt6 application | Changing launch behavior |
| `maptoposter_gui/main_window.py` | Main form, layout, validation, generate/cancel flow | Adding GUI controls or workflows |
| `maptoposter_gui/widgets.py` | Theme preview, zoomable image preview, file actions | Improving preview or reusable widgets |
| `maptoposter_gui/worker.py` | Runs generation in a background `QThread` | Changing progress/cancel behavior |
| `maptoposter_gui/style.py` | Dark-mode semantic tokens and Qt stylesheet | Changing GUI visual design |
| `maptoposter_core/models.py` | Shared request/result/progress dataclasses | Adding generation options |
| `maptoposter_core/themes.py` | Theme discovery and metadata | Changing theme dropdown/preview data |
| `maptoposter_core/generator.py` | GUI-facing generation wrapper | Changing GUI generation flow |

### Rendering Layers (z-order)

```text
z=11  Text labels (city, country, coords)
z=10  Gradient fades (top & bottom)
z=3   Roads (via ox.plot_graph)
z=2   Parks (green polygons)
z=1   Water (blue polygons)
z=0   Background color
```

### OSM Highway Types → Road Hierarchy

```python
# In get_edge_colors_by_type() and get_edge_widths_by_type()
motorway, motorway_link     → Thickest (1.2), darkest
trunk, primary              → Thick (1.0)
secondary                   → Medium (0.8)
tertiary                    → Thin (0.6)
residential, living_street  → Thinnest (0.4), lightest
```

### Typography & Script Detection

The script automatically detects text scripts to apply appropriate typography:

- **Latin scripts** (English, French, Spanish, etc.): Letter spacing applied for elegant "P  A  R  I  S" effect
- **Non-Latin scripts** (Japanese, Arabic, Thai, Korean, etc.): Natural spacing for "東京" (no gaps between characters)

Script detection uses Unicode ranges (U+0000-U+024F for Latin). If >80% of alphabetic characters are Latin, spacing is applied.

### Adding New Features

**New map layer (e.g., railways):**

```python
# In create_poster(), after parks fetch:
try:
    railways = ox.features_from_point(point, tags={'railway': 'rail'}, dist=dist)
except:
    railways = None

# Then plot before roads:
if railways is not None and not railways.empty:
    railways = railways.to_crs(g_proj.graph["crs"])
    railways.plot(ax=ax, color=THEME['railway'], linewidth=0.5, zorder=2.5)
```

**New theme property:**

1. Add to theme JSON: `"railway": "#FF0000"`
2. Use in code: `THEME['railway']`
3. Add fallback in `load_theme()` default dict

### Typography Positioning

All text uses `transform=ax.transAxes` (0-1 normalized coordinates):

```text
y=0.14  City name (spaced letters for Latin scripts)
y=0.125 Decorative line
y=0.10  Country name
y=0.07  Coordinates
y=0.02  Attribution (bottom-right)
```

### Useful OSMnx Patterns

```python
# Get all buildings
buildings = ox.features_from_point(point, tags={'building': True}, dist=dist)

# Get specific amenities
cafes = ox.features_from_point(point, tags={'amenity': 'cafe'}, dist=dist)

# Different network types
G = ox.graph_from_point(point, dist=dist, network_type='drive')  # roads only
G = ox.graph_from_point(point, dist=dist, network_type='bike')   # bike paths
G = ox.graph_from_point(point, dist=dist, network_type='walk')   # pedestrian
```

### Performance Tips

- Large `dist` values (>20km) = slow downloads + memory heavy
- Cache coordinates locally to avoid Nominatim rate limits
- Use `network_type='drive'` instead of `'all'` for faster renders
- Reduce `dpi` from 300 to 150 for quick previews
