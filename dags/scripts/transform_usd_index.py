import json
import os


def transform_usd_index():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.path.join(BASE_DIR, "data", "usd_index", "raw", "usd_index_raw.json")

    output_dir = os.path.join(BASE_DIR, "data", "usd_index", "processed")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(
        output_dir,
        "usd_index_processed.json"
    )

    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    transformed_data = []

    for item in raw_data.get("data", []):
        date = item.get("date")
        value = item.get("value")

        if date is None or value is None:
            continue

        transformed_data.append({
            "date": date,
            "usd_index": float(value)
        })

    transformed_data.sort(key=lambda x: x["date"])

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(transformed_data, file, indent=4)

    print(f"Data Dollar Index hasil transformasi disimpan: {output_file}")
    print(f"Jumlah data hasil transformasi: {len(transformed_data)}")

    return output_file


if __name__ == "__main__":
    transform_usd_index()