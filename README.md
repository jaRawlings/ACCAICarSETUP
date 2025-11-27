# MoTeC CSV Splitter & Corner Detection for ACC

This project provides a Python utility to process **MoTeC telemetry exports** from Assetto Corsa Competizione (ACC).  
It automatically splits a lap into **corner-by-corner CSV files** or annotates the full lap with corner/straight segments, enabling deeper analysis of car setup, driver inputs, and vehicle dynamics.

---

## Features
- Robust CSV loader: Handles MoTeC metadata and normalizes headers.
- Corner detection: Uses steering angle and lateral G-force to identify corners dynamically.
- Adaptive thresholds: Specify the expected number of turns, and the script iteratively adjusts detection thresholds until it matches.
- Exports per corner: Generates individual CSV files for each detected corner.
- Recruiter-friendly design: Clean modular functions (`load_motec_rows`, `detect_corners`, `adaptive_corner_split`) for easy extension.

---

## Project Structure
MotecCSVSplitter.py <br>
Main script README.md <br>
Documentation

---

## Usage

### 1. Install Requirements
This script uses only Python’s standard library (`csv`), so no external dependencies are required.

### 2. Run in PyCharm or CLI
```bash
python MotecCSVSplitter.py
``` 
### 3. Configure Parameters
In the main block of MotecCSVSplitter.py, set:
```python
adaptive_corner_split(
    input_csv="Your_motec_scv_file.csv",
    output_prefix="your_output_Prefix",
    target_turns=14   # expected number of corners at Valencia
)
```
### 4 Outputs
Individual corner files:
``` bash
your_output_Prefix_corner1.csv
your_output_Prefix_corner2.csv
...
```
Console summary of iterations and detected corners.

## How Corner Detection Works
Steering angle (STEERANGLE) and lateral G (G_LAT) are monitored.

Consecutive rows above thresholds are grouped into corners.

Adaptive mode adjusts thresholds until the number of detected corners matches the expected track layout.

## Next Steps
Add combined CSV export with a SegmentType column (corner / straight).

Extend metrics: average steering angle, entry/exit speed, oversteer angle replication.

Integrate with AI setup optimization pipeline.

## License
MIT License — feel free to use, modify, and contribute.

Contributing
Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to improve.

## Author
Developed by John, motorsport enthusiast and AI workflow engineer. Focused on blending data-driven car setup optimization with open-source polish.