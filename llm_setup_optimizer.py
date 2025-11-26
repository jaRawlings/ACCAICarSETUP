"""
LLM Setup Optimizer for ACC AI Project
--------------------------------------
Combines telemetry metrics + current setup into a prompt,
queries an LLM for optimized setup recommendations,
and saves the updated setup JSON.
"""

import json
from pathlib import Path
from typing import Dict, Any

# Example: using LangChain with OpenAI
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.output_parsers import JsonOutputParser


class LLMSetupOptimizer:
    def __init__(self, metrics_path: str, setup_path: str, output_path: str):
        self.metrics_path = Path(metrics_path)
        self.setup_path = Path(setup_path)
        self.output_path = Path(output_path)

        self.metrics = self._load_json(self.metrics_path)
        self.setup = self._load_json(self.setup_path)

        # Initialize LLM (replace with your provider: OpenAI, Anthropic, Mistral, etc.)
        self.llm = OpenAI(model="gpt-4", temperature=0)

    def _load_json(self, path: Path) -> Dict[str, Any]:
        with open(path, "r") as f:
            return json.load(f)

    def _save_json(self, data: Dict[str, Any], path: Path) -> None:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def build_prompt(self) -> str:
        return f"""
You are an expert race engineer for Assetto Corsa Competizione (ACC).
Analyze telemetry metrics and propose optimized car setup changes.

Telemetry Metrics:
{json.dumps(self.metrics, indent=4)}

Current Car Setup:
{json.dumps(self.setup, indent=4)}

Instructions:
- Recommend changes to tyre pressures, suspension, aero balance, dampers, and alignment if needed.
- Output ONLY a JSON object with the updated setup values.
- Include a short explanation for each change in a field called "rationale".
"""

    def run(self) -> None:
        # Build prompt
        prompt_text = self.build_prompt()

        # Define parser
        parser = JsonOutputParser()

        # Wrap in LangChain PromptTemplate
        prompt = PromptTemplate(
            template=prompt_text,
            input_variables=[],
            output_parser=parser,
        )

        # Query LLM
        response = self.llm(prompt.format())

        # Parse JSON output
        try:
            updated_setup = parser.parse(response)
        except Exception as e:
            raise RuntimeError(f"Failed to parse LLM output: {e}\nRaw output:\n{response}")

        # Save updated setup
        self._save_json(updated_setup, self.output_path)

        print("✅ Updated setup saved to", self.output_path)
        print("Changes rationale:")
        for k, v in updated_setup.get("rationale", {}).items():
            print(f" - {k}: {v}")


if __name__ == "__main__":
    optimizer = LLMSetupOptimizer(
        metrics_path="data/metrics.json",
        setup_path="configs/current_setup.json",
        output_path="configs/optimized_setup.json"
    )
    optimizer.run()
