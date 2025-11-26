"""
MoTeC Data Pipeline for ACC AI Setup Optimizer
----------------------------------------------
Parses MoTeC i2 Pro telemetry exports (CSV/LOG) and extracts
relevant metrics for AI-driven setup optimization.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, Any, List


class MoTeCDataPipeline:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.data = None

    def load_data(self) -> pd.DataFrame:
        """Load MoTeC CSV/LOG export into a DataFrame."""
        if self.filepath.suffix.lower() == ".csv":
            self.data = pd.read_csv(self.filepath)
        elif self.filepath.suffix.lower() == ".log":
            # LOG files may need custom parsing; placeholder
            self.data = pd.read_csv(self.filepath, delimiter="\t")
        else:
            raise ValueError("Unsupported file format. Use CSV or LOG.")
        return self.data

    def extract_metrics(self) -> Dict[str, Any]:
        """Extract relevant telemetry metrics."""
        if self.data is None:
            raise RuntimeError("Data not loaded. Call load_data() first.")

        metrics = {}

        # Tyre pressures & temps
        metrics["tyres"] = {
            "pressure_FL": self.data["Tyre Pressure FL"].mean(),
            "pressure_FR": self.data["Tyre Pressure FR"].mean(),
            "pressure_RL": self.data["Tyre Pressure RL"].mean(),
            "pressure_RR": self.data["Tyre Pressure RR"].mean(),
            "temp_FL": self.data["Tyre Temp FL"].mean(),
            "temp_FR": self.data["Tyre Temp FR"].mean(),
            "temp_RL": self.data["Tyre Temp RL"].mean(),
            "temp_RR": self.data["Tyre Temp RR"].mean(),
        }

        # Suspension travel
        metrics["suspension"] = {
            "travel_FL": self.data["Susp Travel FL"].mean(),
            "travel_FR": self.data["Susp Travel FR"].mean(),
            "travel_RL": self.data["Susp Travel RL"].mean(),
            "travel_RR": self.data["Susp Travel RR"].mean(),
        }

        # Aero balance & ride height
        metrics["aero"] = {
            "ride_height_FL": self.data["Ride Height FL"].mean(),
            "ride_height_FR": self.data["Ride Height FR"].mean(),
            "ride_height_RL": self.data["Ride Height RL"].mean(),
            "ride_height_RR": self.data["Ride Height RR"].mean(),
            "aero_balance": self.data["Aero Balance"].mean()
            if "Aero Balance" in self.data.columns else None,
        }

        # Damper histograms (simplified: average damper velocity)
        metrics["dampers"] = {
            "damper_FL": self.data["Damper Vel FL"].mean(),
            "damper_FR": self.data["Damper Vel FR"].mean(),
            "damper_RL": self.data["Damper Vel RL"].mean(),
            "damper_RR": self.data["Damper Vel RR"].mean(),
        }

        return metrics

    def to_json(self, metrics: Dict[str, Any], output_path: str) -> None:
        """Save extracted metrics to JSON for downstream AI agent."""
        with open(output_path, "w") as f:
            json.dump(metrics, f, indent=4)


if __name__ == "__main__":
    # Example usage
    pipeline = MoTeCDataPipeline("data/session_export.csv")
    df = pipeline.load_data()
    metrics = pipeline.extract_metrics()
    pipeline.to_json(metrics, "data/metrics.json")
    print("Extracted metrics saved to data/metrics.json")
