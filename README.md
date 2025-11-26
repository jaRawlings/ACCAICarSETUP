# ACC AI Setup Optimizer (MoTeC + LangChain)

## Overview
**ACC AI Setup Optimizer** applies **large language models (LLMs)** to **motorsport telemetry analysis**.  
It ingests **MoTeC telemetry data** from Assetto Corsa Competizione (ACC), compares it with the current car setup, and recommends optimized parameters.

The workflow showcases **LangChain prompt orchestration** and **AI reasoning** for **iterative optimization**.

---

## Features
- **Telemetry parsing:** Extracts tyre pressures/temps, suspension travel, aero balance, ride height, and damper histograms from MoTeC CSV/LOG.
- **Rule‑based optimizer:** Compares metrics against thresholds and updates the car setup JSON.
- **LLM integration:** Generates prompts, queries an LLM, and writes back updated setup JSON with rationales.
- **Iterative loop:** Test → Analyze → Adjust → Repeat.
- **Structured outputs:** Consistent JSON schema for telemetry, setup, and recommendations.

---

## Tech stack
- **Python** for data parsing and orchestration  
- **LangChain** for prompt workflows and agent integration  
- **LLMs** (OpenAI / Claude / Mistral) for reasoning  
- **MoTeC i2 Pro** telemetry exports (CSV/LOG)  
- **JSON setup files** for ACC configuration

---

## How it works
1. Export session telemetry from ACC via **MoTeC i2 Pro**.
2. Run `motec_data_pipeline.py` to parse telemetry → outputs `data/metrics.json`.
3. Run `setup_optimizer.py` to apply rule-based changes → outputs `configs/optimized_setup.json`.
4. Run `llm_setup_optimizer.py` to generate an LLM prompt, query the model, and update the setup with rationales.
5. Apply changes in ACC and repeat testing.

---

## Repository structure

---

## Quick start
- **Install dependencies:** `pip install -r requirements.txt`
- **Parse telemetry:** `python src/motec_data_pipeline.py`
- **Rule-based optimize:** `python src/setup_optimizer.py`
- **LLM optimize:** `python src/llm_setup_optimizer.py`

---

## Roadmap
- Add **memory** for cross‑session learning
- Integrate a **vector database** for trend storage
- Build a **UI dashboard** for visualization
- Extend to other sims (iRacing, rFactor 2)

---

## Contributing
- **Fork** the repo
- **Create** a feature branch
- **Submit** a pull request

---

## License
MIT License – free to use, modify, and distribute.