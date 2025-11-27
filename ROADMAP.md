# Roadmap

This document outlines the planned development and future direction of the **MoTeC CSV Splitter & Corner Detection for ACC** project.  
The goal is to evolve from a simple corner-splitting utility into a robust telemetry analysis and AI-assisted car setup optimization tool.

---

## Current Capabilities
- Load and normalize MoTeC CSV telemetry exports.
- Detect corners using steering angle and lateral G-force thresholds.
- Adaptive mode: iteratively adjust thresholds until the number of detected corners matches the expected track layout.
- Export individual corner CSV files for deeper analysis.

---

## Short-Term Goals
- **Combined CSV Export**  
  Add a `SegmentType` column (`corner` / `straight`) to a single annotated CSV file.
- **Corner Summary Metrics**  
  Generate a summary file with start time, end time, duration, average steering angle, and entry/exit speed for each corner.
- **Improved Adaptive Algorithm**  
  Refine threshold iteration logic for faster convergence and more accurate corner counts.
- **Sample Data & Examples**  
  Provide example input/output files for users to test the tool immediately.

---

## Medium-Term Goals
- **Advanced Metrics**  
  - Oversteer angle replication (matching MoTeC i2 Pro math channels).  
  - Handling balance analysis (understeer/oversteer detection).  
  - Entry/exit speed deltas.
- **Visualization Tools**  
  Add optional plots (corner speeds, steering traces, G-force maps).
- **Testing Framework**  
  Unit tests with synthetic CSVs to validate detection logic.
- **Documentation Expansion**  
  Detailed explanation of MoTeC telemetry fields and how they are used.

---

## Long-Term Goals
- **AI Setup Optimizer Integration**  
  Connect telemetry outputs to an AI pipeline (e.g., LangChain) for automated car setup recommendations.
- **Track Profiles**  
  Predefined corner counts and detection profiles for major ACC circuits.
- **Community Contributions**  
  Encourage open-source collaboration, PRs for new features, and track-specific tuning.
- **Modular Repo Structure**  
  Package the tool as a Python library with clear APIs for integration into larger workflows.

---

## Vision
The long-term vision is to create a **modular, open-source telemetry analysis toolkit** that bridges motorsport data with AI-driven optimization.  
This project is designed to showcase both technical depth and professional polish, making it useful for sim racers, engineers, and recruiters evaluating data workflow skills.
