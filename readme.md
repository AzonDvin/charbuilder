# Savage Worlds Star Wars Character Builder

A desktop wizard for creating **Savage Worlds** Star Wars characters step-by-step.

The app is built with Python and Tkinter, uses JSON for game data, and exports completed characters to a JSON file.

## Current Project Process

The character builder walks through this process in order:

1. **Concept & Species** - Set character name and species.
2. **Hindrances** - Select up to 4 hindrance points (Major = 2, Minor = 1).
3. **Attributes** - Spend base attribute points plus any converted hindrance points.
4. **Skills** - Spend base skill points plus any converted hindrance points.
5. **Edges** - Purchase edges with hindrance points (2 points each). Human gets one free edge.
6. **Weapons, Armor & Gear** - Buy equipment using starting credits.
7. **Summary** - Review final sheet and save to JSON.

## Features Implemented

- Guided multi-step UI flow with Previous/Next navigation.
- Species-aware setup (including Human free-edge handling).
- Hindrance point tracking across attributes, skills, and edges.
- Edge requirement checks for rank, attributes, and skills.
- Equipment shop with buy/sell and live credit recalculation.
- Derived stat calculation (`Toughness` and `Parry`).
- Final character export to `.json`.
- Optional **print-friendly** exports: HTML layout or plain text (from the Summary step, or from a saved JSON file via CLI).

## Run the Project

### Requirements

- Python 3.10+ (Tkinter included with standard Python installs)
- No external packages required

### Start

From the project root:

```bash
python main.py
```

## Project Structure

- `main.py` - App entry point.
- `gui.py` - Tkinter wizard UI and step logic.
- `character.py` - Character model and derived stat logic.
- `character_sheet.py` - Text/HTML character sheet from exported JSON (used by CLI and Summary exports).
- `data.py` - JSON data loader and data grouping.
- `data/` - Source game content:
  - `attributes.json`
  - `edges.json`
  - `gear.json`
  - `hindrances.json`
  - `species.json`
- `docs/race_building_rules.md` - Reference notes for custom race/species design.

## Data-Driven Content

Most rules content is loaded from JSON files in `data/`. To expand options:

- Add or edit edges in `data/edges.json`
- Add or edit hindrances in `data/hindrances.json`
- Add or edit species in `data/species.json`
- Add or edit equipment in `data/gear.json`
- Update skills/attributes in `data/attributes.json`

## Save Output

When the build is complete, the app saves a character JSON that includes:

- Character identity and species data
- Attributes and skills
- Hindrances and edges
- Equipment and credits
- Derived values (`toughness`, `parry`)

## Display and print from JSON

After you have a character `.json` file, you can turn it into something easy to read or print in several ways:

1. **Summary step in the app** — On the last step, use **Export printable HTML…** or **Export text sheet…** (same layout as the on-screen summary, plus a styled HTML page for printing).

2. **Command-line renderer** — From the project directory (so `data/` can resolve armor names for the armor bonus line):

   ```bash
   python character_sheet.py path/to/character.json --html sheet.html --open
   ```

   Other flags:

   - `--text sheet.txt` — plain text sheet
   - `--stdout` — print plain text to the terminal
   - With no `--html` / `--text` / `--stdout`, prints plain text and a short tip on stderr

3. **Browser print to PDF** — Open the generated HTML, use the browser’s **Print** dialog, and choose **Save as PDF** if you want a PDF without extra Python libraries.

4. **Bring your own template** — The JSON is a simple structure (`name`, `species`, `attributes`, `skills`, `edges`, etc.). You can import it into a word processor, Obsidian, or another tool and format it however you like.

The logic for the text/HTML sheet lives in `character_sheet.py` (`character_sheet_text`, `character_sheet_html`).

## Notes

- Existing docs include race balancing guidance in `docs/race_building_rules.md`.
- `requirements.txt` is informational; the app currently relies on Python standard library modules.
