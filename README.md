# MoTeC CSV Splitter & Setup Aggregator for ACC

This project provides a Python utility to process **MoTeC telemetry exports** and **corner-specific setup files** from Assetto Corsa Competizione (ACC).  
It automatically splits a lap into **corner-by-corner CSV files**, annotates the full lap with corner/straight segments, and aggregates multiple setup JSONs into a single compromise setup using telemetry-derived weights.  
The goal is to bridge raw motorsport data with **AI-assisted car setup optimization**.

---

## Features
- **Robust CSV loader**: Handles MoTeC metadata and normalizes headers.
- **Corner detection**: Uses steering angle and lateral G-force to identify corners dynamically.
- **Adaptive thresholds**: Iteratively adjusts detection thresholds until the number of detected corners matches the expected track layout.
- **Per-corner exports**: Generates individual CSV files for each detected corner.
- **Zip ingestion**: Reads both setup JSON files and MoTeC CSV telemetry directly from `.zip` archives.
- **Setup aggregation**: Combines corner-specific setups into a master compromise setup, weighted by sector times or lap deltas.
- **Recruiter-friendly design**: Clean modular functions (`load_motec_rows`, `detect_corners`, `aggregate_setups`) for easy extension and demonstration of workflow skills.

---

## Project Structure
- `MotecCSVSplitter.py` — main corner detection and CSV processing script  
- `SetupAggregator.py` — JSON + CSV ingestion and compromise setup generation  
- `README.md` — project overview and usage guide  
- `ROADMAP.md` — planned development and future direction  
- `docs/` — extended documentation and examples  

---

## Usage

### 1. Install Requirements
This project uses only Python’s standard library (`csv`, `json`, `zipfile`), so no external dependencies are required.

### 2. Run in PyCharm or CLI
```bash
python MotecCSVSplitter.py
```

### 3. Configure Parameters
In the main block of MotecCSVSplitter.py, set:
```python
adaptive_corner_split(
    input_csv="Your_motec_csv_file.csv",
    output_prefix="your_output_prefix",
    target_turns=14   # expected number of corners at Valencia
)

```
### 4. Outputs
- Individual corner files:
```bash
your_output_prefix_corner1.csv
your_output_prefix_corner2.csv
...
```
- Console summary of iterations and detected corners.

- master_setup.json compromise setup generated from JSON + CSV data.

### How Corner Detection & Aggregation Work
- **Corner detection:** Steering angle (STEERANGLE) and lateral G (G_LAT) are monitored. Consecutive rows above thresholds are grouped into corners. Adaptive mode adjusts thresholds until the number of detected corners matches the expected track layout.

- **Setup aggregation:** Each corner’s setup JSON is weighted by its lap-time impact (from MoTeC CSV sector times). Numeric parameters are averaged with weights; categorical parameters use majority vote. The result is a balanced master setup.

### Next Steps
- Add combined CSV export with a SegmentType column (corner / straight).
- Extend metrics: average steering angle, entry/exit speed, oversteer angle replication, handling balance analysis.
- Visualization tools: plots for corner speeds, steering traces, and G-force maps.
- AI integration: connect telemetry outputs to LangChain pipelines for automated setup recommendations.

### License
MIT License — feel free to use, modify, and contribute.

### Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to improve. Contributors are encouraged to add track profiles, new metrics, or AI workflow integrations.

### Author
Developed by John, motorsport enthusiast and AI workflow engineer. Focused on blending data-driven car setup optimization with open-source polish and recruiter-friendly workflows.