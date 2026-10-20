import yfinance as yf
import pandas as pd
import os
from datetime import datetime


def extract_ihsg():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "data", "ihsg", "raw")
    os.makedirs(output_dir, exist_ok=True)

    ticker = "^JKSE"  # Ticker IHSG di Yahoo Finance

    print("Mengambil data IHSG dari Yahoo Finance...")

    data = yf.download(ticker, period="1y", interval="1d")

    if data.empty:
        print("Data kosong, cek koneksi atau ticker.")
        return

    data = data.reset_index()
    data.columns = [c[0] if isinstance(c, tuple) else c for c in data.columns]

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(output_dir, f"ihsg_{today}.csv")

    data.to_csv(output_file, index=False)

    print(f"Jumlah baris: {len(data)}")
    print(f"Berhasil disimpan: {output_file}")
    print(data.tail())


if __name__ == "__main__":
    extract_ihsg()