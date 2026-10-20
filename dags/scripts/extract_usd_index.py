import json
import os
import requests
from datetime import datetime, timedelta


def extract_usd_index():

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    url = f"https://convextrade.com/api/public/data/DTWEXBGS?start={start_date}&end={end_date}"

    print(f"Mengambil data USD Index dari {start_date} sampai {end_date}...")

    response = requests.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()

    # Path absolut, selalu ke root project (bukan tergantung folder jalan)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "data", "usd_index", "raw")
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "usd_index_raw.json")

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Data Dollar Index berhasil disimpan: {output_file}")
    print(f"Jumlah data: {len(data.get('data', []))}")

    return output_file


if __name__ == "__main__":
    extract_usd_index()