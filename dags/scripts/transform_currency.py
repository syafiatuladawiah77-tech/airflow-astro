import json
import pandas as pd
import os
import glob


def transform_currency():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(BASE_DIR, "data", "currency", "raw")
    processed_dir = os.path.join(BASE_DIR, "data", "currency", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    # Mata uang yang mau difokuskan (sesuaikan sama negara di project World Bank kamu)
    target_currencies = ["idr", "myr", "sgd", "thb", "php"]

    # Ambil semua file mentah yang sudah terkumpul
    raw_files = sorted(glob.glob(os.path.join(raw_dir, "currency_*.json")))

    if not raw_files:
        print("Belum ada file data mentah. Jalankan extract dulu.")
        return

    rows = []

    for file_path in raw_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        date = data.get("date")
        rates = data.get("usd", {})

        row = {"date": date}
        for currency in target_currencies:
            row[currency] = rates.get(currency)

        rows.append(row)

    df = pd.DataFrame(rows)

    # Hapus duplikat tanggal (kalau ada extract dobel di hari yang sama)
    before_dup = len(df)
    df = df.drop_duplicates(subset=["date"])
    after_dup = len(df)
    print(f"Baris duplikat dihapus: {before_dup - after_dup}")

    # Urutkan berdasarkan tanggal
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    print("\n=== MISSING VALUE ===")
    print(df.isnull().sum())

    # Ganti NaN jadi None, aman untuk PostgreSQL
    df = df.where(pd.notnull(df), None)

    print("\n=== DATA TERBARU ===")
    print(df.tail())

    output_file = os.path.join(processed_dir, "currency_merged.json")
    df.to_json(output_file, orient="records", indent=2, date_format="iso")

    print(f"\nData berhasil disimpan: {output_file}")
    print(f"Total baris (hari): {len(df)}")


if __name__ == "__main__":
    transform_currency()