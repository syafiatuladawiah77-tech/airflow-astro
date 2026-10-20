import pandas as pd
import os
import glob


def transform_ihsg():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(BASE_DIR, "data", "ihsg", "raw")
    processed_dir = os.path.join(BASE_DIR, "data", "ihsg", "processed")
    os.makedirs(processed_dir, exist_ok=True)

    raw_files = sorted(glob.glob(os.path.join(raw_dir, "ihsg_*.csv")))

    if not raw_files:
        print("Belum ada file data mentah. Jalankan extract_ihsg dulu.")
        return

    latest_file = raw_files[-1]
    df = pd.read_csv(latest_file)

    df.columns = [c.lower() for c in df.columns]
    df = df[["date", "open", "high", "low", "close", "volume"]].copy()
    df["date"] = pd.to_datetime(df["date"])

    before_dup = len(df)
    df = df.drop_duplicates(subset=["date"])
    after_dup = len(df)
    print(f"Baris duplikat dihapus: {before_dup - after_dup}")

    df = df.sort_values("date").reset_index(drop=True)

    print("\n=== MISSING VALUE ===")
    print(df.isnull().sum())

    df = df.where(pd.notnull(df), None)

    print("\n=== DATA TERBARU ===")
    print(df.tail())

    output_file = os.path.join(processed_dir, "ihsg_merged.json")
    df.to_json(output_file, orient="records", indent=2, date_format="iso")

    print(f"\nData berhasil disimpan: {output_file}")
    print(f"Total baris: {len(df)}")


if __name__ == "__main__":
    transform_ihsg()