"""
Setup Optimizer for ACC AI Setup Project
----------------------------------------
Reads telemetry metrics (from motec_data_pipeline JSON output),
compares them to the current car setup JSON, and applies changes.
"""

import json
from pathlib import Path
from typing import Dict, Any


class SetupOptimizer:
    def __init__(self, metrics_path: str, setup_path: str):
        self.metrics_path = Path(metrics_path)
        self.setup_path = Path(setup_path)

        self.metrics = self._load_json(self.metrics_path)
        self.setup = self._load_json(self.setup_path)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with open(path, "r") as f:
            return json.load(f)

    def _save_json(self, data: Dict[str, Any], path: Path) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def compare_and_adjust(self) -> Dict[str, Any]:
        """
        Apply simple rule-based adjustments based on telemetry metrics.
        Extendable with LangChain agent reasoning later.
        """
        adjustments = {}

        # --- Tyre pressures ---
        target_pressure = 27.5  # Example target PSI for ACC tyres
        for corner in ["FL", "FR", "RL", "RR"]:
            current = self.metrics["tyres"][f"pressure_{corner}"]
            setup_val = self.setup["tyres"][f"pressure_{corner}"]

            if current < target_pressure - 0.5:
                self.setup["tyres"][f"pressure_{corner}"] = setup_val + 0.2
                adjustments[f"pressure_{corner}"] = "increase +0.2"
            elif current > target_pressure + 0.5:
                self.setup["tyres"][f"pressure_{corner}"] = setup_val - 0.2
                adjustments[f"pressure_{corner}"] = "decrease -0.2"

        # --- Suspension travel (too much travel → stiffen suspension) ---
        for corner in ["FL", "FR", "RL", "RR"]:
            travel = self.metrics["suspension"][f"travel_{corner}"]
            if travel > 60:  # mm threshold example
                self.setup["suspension"][f"spring_{corner}"] += 5
                adjustments[f"spring_{corner}"] = "increase stiffness +5"

        # --- Aero balance (rear instability → increase rear wing) ---
        aero_balance = self.metrics["aero"].get("aero_balance")
        if aero_balance and aero_balance < 45:  # too front-biased
            self.setup["aero"]["rear_wing"] += 1
            adjustments["rear_wing"] = "increase +1"

        # --- Damper histograms (simplified: average velocity too high → add damping) ---
        for corner in ["FL", "FR", "RL", "RR"]:
            damper = self.metrics["dampers"][f"damper_{corner}"]
            if damper > 0.8:  # arbitrary threshold
                self.setup["dampers"][f"bump_{corner}"] += 2
                adjustments[f"bump_{corner}"] = "increase damping +2"

        return adjustments

    def run(self, output_path: str = "configs/optimized_setup.json") -> None:
        adjustments = self.compare_and_adjust()
        self._save_json(self.setup, Path(output_path))

        print("✅ Setup optimized and saved to", output_path)
        print("Applied adjustments:")
        for k, v in adjustments.items():
            print(f" - {k}: {v}")


if __name__ == "__main__":
    optimizer = SetupOptimizer(
        metrics_path="data/metrics.json",
        setup_path="configs/current_setup.json"
    )
    optimizer.run()
