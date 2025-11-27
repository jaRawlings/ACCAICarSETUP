import json
import pandas as pd
import argparse
import glob
import zipfile
from pathlib import Path
from openai import OpenAI



# --- LOAD CORNER FILES ---
def load_corner_files(output_prefix: str) -> list[tuple[str, pd.DataFrame]]:
    """
    Load all corner CSV files exported by adaptive_corner_split.
    Returns list of (filename, DataFrame).
    """
    files = sorted(glob.glob(f"{output_prefix}_corner*.csv"))
    if not files:
        raise FileNotFoundError(f"No corner CSV files found with prefix '{output_prefix}_corner'")
    return [(f, pd.read_csv(f)) for f in files]


# --- LLM QUERY ---
def query_llm_for_corner(corner_df: pd.DataFrame, base_setup: dict) -> dict:
    """
    Send telemetry for one corner + base setup to LLM, get recommended changes.

    Parameters
    ----------
    corner_df : pd.DataFrame
        Telemetry data for a single corner.
    base_setup : dict
        The current ACC setup JSON loaded from file, used as the baseline.

    Returns
    -------
    dict
        A dictionary of recommended setup changes for this corner, following ACC setup.json schema.
    """
    client = OpenAI()

    # Defensive summary generation
    try:
        from typing import cast

        desc = cast(pd.DataFrame, cast(object, corner_df.describe(include="all")))
        telemetry_summary = desc.to_string()
    except Exception as e:
        telemetry_summary = f"Could not generate summary: {e}"

    prompt = f"""
    You are an expert race engineer for ACC.
    Analyze the following telemetry data and the current setup.
    Suggest specific setup changes (e.g., camber, toe, dampers, ride height, tyre pressures, wing, splitter, mechanical Balance, drivetrain preload, caster) 
    that would improve performance.

    IMPORTANT:
    - Output ONLY a JSON object containing all parameters.
    - Keep the schema consistent with ACC setup.json format.

    Telemetry summary:
    {telemetry_summary}

    Current setup:
    {json.dumps(base_setup, indent=2)}
    """

    messages = [
        {"role": "system", "content": "You are an expert race engineer for ACC."},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages, # type: ignore
        temperature=0.2
    )

    msg_content = response.choices[0].message.content

    try:
        changes = json.loads(msg_content)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON returned:\n{msg_content}")

    return changes


# --- MAIN PIPELINE ---
def main():
    parser = argparse.ArgumentParser(description="ACC Telemetry → LLM → Corner-by-Corner Setup Optimizer")
    parser.add_argument("--setup", required=True, help="Path to initial setup JSON file")
    parser.add_argument("--prefix", required=True, help="Output prefix used by corner splitter (e.g. Valencia1)")
    parser.add_argument("--zip", default="corner_setups.zip", help="Zip file to save all per-corner JSONs")
    args = parser.parse_args()

    # Load base setup
    with open(args.setup, "r") as f:
        base_setup = json.load(f)

    # Load corner files
    corner_files = load_corner_files(args.prefix)

    # Create zip archive and write each corner JSON directly
    with zipfile.ZipFile(args.zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f, df in corner_files:
            print(f"🔍 Processing {Path(f).name}...")
            changes = query_llm_for_corner(df, base_setup)

            corner_name = Path(f).stem
            json_bytes = json.dumps(changes, indent=2).encode("utf-8")
            zipf.writestr(f"{corner_name}.json", json_bytes)

    print(f"✅ All per-corner setup files saved into {args.zip}")


if __name__ == "__main__":
    main()
