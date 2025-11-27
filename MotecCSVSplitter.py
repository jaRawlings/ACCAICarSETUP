import csv

def load_motec_rows(input_csv):
    with open(input_csv, newline='') as f:
        raw = list(csv.reader(f))

    header_idx = None
    for i, row in enumerate(raw):
        if not row:
            continue
        first = row[0].strip().strip('"').upper()
        if first == "TIME":
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find header row starting with 'Time'.")

    header = [h.strip().strip('"').lstrip("\ufeff").upper() for h in raw[header_idx]]
    data_rows = raw[header_idx + 1:]

    rows = []
    for r in data_rows:
        if len(r) < len(header):
            r = r + [""] * (len(header) - len(r))
        elif len(r) > len(header):
            r = r[:len(header)]
        row_dict = {header[j]: r[j].strip().strip('"') for j in range(len(header))}
        rows.append(row_dict)

    return header, rows


def detect_corners(rows, steer_threshold, g_lat_threshold, min_duration):
    corners = []
    current_corner = []
    corner_index = 1

    for row in rows:
        try:
            steer = float(row.get("STEERANGLE", "0") or "0")
            g_lat = float(row.get("G_LAT", "0") or "0")
        except (ValueError, TypeError):
            continue

        if abs(steer) > steer_threshold and abs(g_lat) > g_lat_threshold:
            current_corner.append(row)
        else:
            if current_corner:
                try:
                    duration = float(current_corner[-1]["TIME"]) - float(current_corner[0]["TIME"])
                except (ValueError, TypeError, KeyError):
                    duration = 0.0
                if duration >= min_duration:
                    corners.append((corner_index, current_corner))
                    corner_index += 1
                current_corner = []

    if current_corner:
        try:
            duration = float(current_corner[-1]["TIME"]) - float(current_corner[0]["TIME"])
        except (ValueError, TypeError, KeyError):
            duration = 0.0
        if duration >= min_duration:
            corners.append((corner_index, current_corner))

    return corners


def export_corners(corners, header, output_prefix):
    for idx, corner_rows in corners:
        out_file = f"{output_prefix}_corner{idx}.csv"
        with open(out_file, "w", newline='') as f_out:
            writer = csv.DictWriter(f_out, fieldnames=header)
            writer.writeheader()
            writer.writerows(corner_rows)
        print(f"Exported corner {idx} with {len(corner_rows)} rows to {out_file}")


def adaptive_corner_split(input_csv, output_prefix, target_turns):
    header, rows = load_motec_rows(input_csv)

    steer_threshold = 0.5
    g_lat_threshold = 0.2
    min_duration = 0.05
    count = 0  # initialize

    for iteration in range(50):
        corners = detect_corners(rows, steer_threshold, g_lat_threshold, min_duration)
        count = len(corners)
        print(f"Iteration {iteration}: steer={steer_threshold:.3f}, g_lat={g_lat_threshold:.3f}, min_dur={min_duration:.3f} -> {count} corners")

        if count == target_turns:
            export_corners(corners, header, output_prefix)
            print(f"✅ Matched target of {target_turns} turns.")
            return

        if count < target_turns:
            steer_threshold *= 0.8
            g_lat_threshold *= 0.8
            min_duration *= 0.8
        else:
            steer_threshold *= 1.2
            g_lat_threshold *= 1.2
            min_duration *= 1.2

    print(f"⚠️ Could not converge to {target_turns} turns after 50 iterations. Last count={count}")


# ---------------- MAIN ----------------
if __name__ == "__main__":
    adaptive_corner_split(
        input_csv="C:\\Users\\john\\Documents\\MoTeC\\Valencia-ferrari_296_gt3-0-2025.11.27-10.58.07.csv",
        output_prefix="C:\\Users\\john\\Documents\\MoTeC\\Valencia1",
        target_turns=13
    )
