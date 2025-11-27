import json
import zipfile
import csv
from collections import defaultdict, Counter

def load_setups_and_csv(zip_path):
    setups = []
    telemetry = {}

    with zipfile.ZipFile(zip_path, "r") as z:
        for file_name in z.namelist():
            if file_name.endswith(".json"):
                with z.open(file_name) as f:
                    setups.append(json.load(f))
            elif file_name.endswith(".csv"):
                with z.open(file_name) as f:
                    reader = csv.DictReader(line.decode("utf-8") for line in f)
                    # Expect columns like: corner_id, sector_time, lap_delta
                    for row in reader:
                        corner_id = row.get("corner_id")
                        if corner_id:
                            telemetry[corner_id] = {
                                "sector_time": float(row.get("sector_time", 0)),
                                "lap_delta": float(row.get("lap_delta", 0))
                            }
    return setups, telemetry

def derive_corner_weights(setups, telemetry):
    """
    Assign weights to each setup based on telemetry data.
    Example: slower corners (higher sector_time) get more weight.
    """
    weights = []
    for setup in setups:
        corner_id = setup.get("corner_id")
        if corner_id and corner_id in telemetry:
            sector_time = telemetry[corner_id]["sector_time"]
            # Weight = sector_time normalized (higher time = more important)
            weights.append(sector_time)
        else:
            weights.append(1.0)  # default if no telemetry match
    return weights

def aggregate_setups(setups, corner_weights):
    aggregated = defaultdict(list)

    for setup, weight in zip(setups, corner_weights):
        for key, value in setup.items():
            if key == "corner_id":  # skip metadata
                continue
            aggregated[key].append((value, weight))

    compromise = {}
    for key, values in aggregated.items():
        if all(isinstance(v[0], (int, float)) for v in values):
            total_weight = sum(w for _, w in values)
            compromise[key] = sum(v * w for v, w in values) / total_weight
        else:
            counter = Counter(v for v, _ in values)
            compromise[key] = counter.most_common(1)[0][0]

    return compromise

def save_master_setup(compromise, output_path="master_setup.json"):
    with open(output_path, "w") as f:
        json.dump(compromise, f, indent=4)

if __name__ == "__main__":
    zip_file = "corner_setups.zip"  # path to your zip archive
    setups, telemetry = load_setups_and_csv(zip_file)

    corner_weights = derive_corner_weights(setups, telemetry)
    master_setup = aggregate_setups(setups, corner_weights)

    save_master_setup(master_setup)
    print("Master compromise setup saved to master_setup.json")
