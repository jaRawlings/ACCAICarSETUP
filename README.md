# MoTeC CSV Splitter & Setup Aggregator for ACC

This project processes **MoTeC telemetry exports** and **corner-specific setup files** from Assetto Corsa Competizione (ACC).  
It can split a lap into **corner-by-corner CSV files**, annotate a full lap with corner/straight segments, and aggregate multiple setup JSONs into a single compromise setup using telemetry-derived weights.

---

## Features
- **Robust CSV loader**: Handles MoTeC metadata and normalizes headers.
- **Corner detection**: Uses steering angle and lateral G-force to identify corners dynamically.
- **Adaptive thresholds (WIP)**: Iteratively tunes thresholds to match the expected track corner count.
- **Per-corner exports**: Generates individual CSVs for each detected corner.
- **Zip ingestion**: Reads setup JSONs and MoTeC CSV telemetry directly from `.zip`.
- **Setup aggregation**: Produces a master compromise setup from corner-specific JSONs, weighted by sector times or lap deltas.

---

## Project Structure
- `MotecCSVSplitter.py` — corner detection and CSV processing
- `SetupAggregator.py` — JSON + CSV ingestion (from zip) and compromise setup generation
- `README.md` — project overview and usage guide
- `ROADMAP.md` — development plan
- `docs/` — extended documentation and examples

---

## Usage

### 1. Split MoTeC CSV into per-corner files
Run the splitter script with your input CSV. The script will output corner CSVs and a console summary.

```bash
python MotecCSVSplitter.py --input path/to/your_motec.csv --output-prefix output/run1
```
### Expected outputs:
```bash
output/run1_corner1.csv
output/run1_corner2.csv
```

### Console summary of detected corners
If your script currently uses hardcoded paths in if __name__ == "__main__":, set:
```python
INPUT_CSV = "path/to/your_motec.csv"
OUTPUT_PREFIX = "output/run1"
```
## 2. Aggregate corner setups using telemetry weights
Bundle your corner setup JSONs and the MoTeC CSV into a single zip, then run the aggregator:
```bash
python SetupAggregator.py --zip path/to/corner_setups_and_motec.zip --out master_setup.json
```
The zip should contain:
- corner_*.json files (one per corner)
- A MoTeC telemetry CSV (e.g., session.csv)

The aggregator will:
- Load JSONs and the CSV from the zip
- Derive corner weights from sector times or lap deltas in the CSV
- Output master_setup.json

---

### How It Works
- **Corner detection:** Monitors steering angle (STEERANGLE) and lateral G (G_LAT). Consecutive rows over thresholds form corners. Adaptive tuning (if enabled) adjusts thresholds to better match the track’s corner count.

- *Setup aggregation:*
  - Numeric parameters → weighted averages (weights from sector times/lap deltas)
  - Categorical parameters → majority vote
  -Outputs a balanced master_setup.json
---
### Roadmap Highlights
- Unified CSV export with SegmentType (corner/straight)
- Corner summaries (duration, avg steering angle, entry/exit speeds, lap deltas)
- Advanced metrics: oversteer angle replication, handling balance analysis
- Visualization (corner speeds, steering traces, G-force maps)
- AI integration (LangChain) for automated setup recommendations
---
### License
MIT License — use, modify, and contribute freely.
---
### Contributing
Pull requests welcome. For major changes, open an issue to discuss design and interfaces. Track profiles, metrics, and AI workflow integrations are great contributions.
---
### Author
Developed by John, motorsport enthusiast and AI workflow engineer, focused on data-driven setup optimization with open-source polish.