import requests
import json
import os


def extract_currency():

    # Mata uang yang mau diambil, basis USD
    base_currency = "usd"

    # Folder penyimpanan
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(BASE_DIR, "data", "currency", "raw")
    os.makedirs(output_dir, exist_ok=True)

    # URL utama
    primary_url = (
        f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest"
        f"/v1/currencies/{base_currency}.json"
    )

    # URL cadangan
    fallback_url = (
        f"https://latest.currency-api.pages.dev"
        f"/v1/currencies/{base_currency}.json"
    )

    print("Mengambil data kurs mata uang...")

    try:
        response = requests.get(primary_url, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        print("URL utama gagal, mencoba URL cadangan...")
        response = requests.get(fallback_url, timeout=30)
        response.raise_for_status()

    data = response.json()

    # Ambil tanggal asli yang diberikan API
    api_date = data.get("date")

    if not api_date:
        raise ValueError("Tanggal data tidak ditemukan dari API.")

    # Nama file mengikuti tanggal data API
    output_file = os.path.join(
        output_dir,
        f"currency_{api_date}.json"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"Berhasil disimpan: {output_file}")
    print(f"Tanggal data: {api_date}")


if __name__ == "__main__":
    extract_currency()