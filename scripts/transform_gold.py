import json
import pandas as pd
import os
import glob


def transform_gold():
    # Folder utama project di dalam Airflow
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    raw_dir = os.path.join(BASE_DIR, "data", "currency", "raw")
    processed_dir = os.path.join(BASE_DIR, "data", "gold", "processed")

    os.makedirs(processed_dir, exist_ok=True)

    # Ambil semua file raw currency
    raw_files = sorted(
        glob.glob(os.path.join(raw_dir, "currency_*.json"))
    )

    if not raw_files:
        print("Belum ada file data mentah.")
        return

    records = []

    for file_path in raw_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        date = data.get("date")
        rates = data.get("usd", {})

        xau = rates.get("xau")

        # Simpan hanya jika tanggal dan XAU tersedia
        if date is not None and xau is not None:
            records.append({
                "date": date,
                "xau_per_usd": xau
            })

    df = pd.DataFrame(records)

    if df.empty:
        print("Tidak ada data XAU yang ditemukan.")
        return

    # =========================
    # CLEANING / PREPROCESSING
    # =========================

    # Cek missing value
    print("\n=== MISSING VALUE ===")
    print(df.isnull().sum())

    # Hapus baris yang tidak memiliki data penting
    df = df.dropna(subset=["date", "xau_per_usd"])

    # Hapus duplikat berdasarkan tanggal
    before_dup = len(df)

    df = df.drop_duplicates(
        subset=["date"],
        keep="last"
    )

    after_dup = len(df)

    print(f"\nBaris duplikat dihapus: {before_dup - after_dup}")

    # Ubah date menjadi datetime
    df["date"] = pd.to_datetime(df["date"])

    # Pastikan XAU numerik
    df["xau_per_usd"] = pd.to_numeric(
        df["xau_per_usd"],
        errors="coerce"
    )

    # Hindari pembagian dengan nol
    df.loc[df["xau_per_usd"] <= 0, "xau_per_usd"] = None
    df = df.dropna(subset=["xau_per_usd"])

    # Konversi:
    # API memberikan XAU per 1 USD
    # Dibalik menjadi USD per gold ounce
    df["gold_usd_per_ounce"] = 1 / df["xau_per_usd"]

    # Urutkan berdasarkan tanggal
    df = df.sort_values("date").reset_index(drop=True)

    # =========================
    # HASIL
    # =========================

    print("\n=== DATA EMAS TERBARU ===")
    print(df.tail())

    output_file = os.path.join(
        processed_dir,
        "gold_merged.json"
    )

    df.to_json(
        output_file,
        orient="records",
        indent=2,
        date_format="iso"
    )

    print("\n===================================")
    print("Transformasi data emas berhasil")
    print(f"Total baris: {len(df)}")
    print(f"File: {output_file}")
    print("===================================")


if __name__ == "__main__":
    transform_gold()