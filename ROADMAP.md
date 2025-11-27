# Roadmap

This document outlines the planned development and future direction of the **MoTeC CSV Splitter & Corner Detection for ACC** project.  
The goal is to evolve from a simple corner-splitting utility into a robust telemetry analysis and AI-assisted car setup optimization toolkit.

---

## Current Capabilities
- Load and normalize MoTeC CSV telemetry exports.
- Detect corners using steering angle and lateral G-force thresholds.
- Adaptive mode: iteratively adjust thresholds until the number of detected corners matches the expected track layout.
- Export individual corner CSV files for deeper analysis.
- Ingest setup JSON files and MoTeC CSV data directly from `.zip` archives.
- Aggregate multiple corner-specific setups into a single compromise setup using telemetry-derived weights.

---

## Short-Term Goals
- **Unified CSV Export**  
  Add a `SegmentType` column (`corner` / `straight`) to a single annotated CSV file.
- **Corner Summary Metrics**  
  Generate a summary file with start time, end time, duration, average steering angle, entry/exit speed, and lap-time delta.
- **Telemetry-Driven Weighting**  
  Use sector times and lap deltas from MoTeC CSVs to quantify the importance of each corner in setup aggregation.
- **Improved Adaptive Algorithm**  
  Refine threshold iteration logic for faster convergence and more accurate corner counts.
- **Sample Data & Examples**  
  Provide example input/output files and annotated setups for immediate user testing.

---

## Medium-Term Goals
- **Advanced Metrics**  
  - Oversteer angle replication (matching MoTeC i2 Pro math channels).  
  - Handling balance analysis (understeer/oversteer detection).  
  - Entry/exit speed deltas and braking efficiency.  
  - Sector-weighted compromise setups.
- **Visualization Tools**  
  Optional plots for corner speeds, steering traces, G-force maps, and setup parameter influence.
- **Testing Framework**  
  Unit tests with synthetic CSVs and JSON setups to validate detection and aggregation logic.
- **Documentation Expansion**  
  Detailed explanation of MoTeC telemetry fields, setup parameters, and how they interact in compromise generation.

---

## Long-Term Goals
- **AI Setup Optimizer Integration**  
  Connect telemetry outputs and aggregated setups to an AI pipeline (e.g., LangChain) for automated car setup recommendations.
- **Track Profiles**  
  Predefined corner counts, detection profiles, and weighting schemes for major ACC circuits.
- **Community Contributions**  
  Encourage open-source collaboration, PRs for new features, and track-specific tuning.
- **Modular Repo Structure**  
  Package the tool as a Python library with clear APIs for integration into larger workflows and AI agents.

---

## Vision
The long-term vision is to create a **modular, open-source telemetry and setup optimization toolkit** that bridges motorsport data with AI-driven workflows.  
This project is designed to showcase both technical depth and professional polish, making it useful for sim racers, engineers, and recruiters evaluating data workflow and AI integration skills.
