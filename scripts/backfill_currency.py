import requests
import json
import os
from datetime import datetime, timedelta


def backfill_currency(days=180):

    base_currency = "usd"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(BASE_DIR, "..", "data", "currency", "raw")
    output_dir = os.path.abspath(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    today = datetime.now()

    success_count = 0
    skip_count = 0
    fail_count = 0

    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")

        output_file = os.path.join(output_dir, f"currency_{date_str}.json")

        if os.path.exists(output_file):
            skip_count += 1
            continue

        url = (
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date_str}"
            f"/v1/currencies/{base_currency}.json"
        )

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()

            with open(output_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

            print(f"Berhasil: {date_str}")
            success_count += 1
        except requests.exceptions.RequestException:
            print(f"Gagal (mungkin belum ada data): {date_str}")
            fail_count += 1

    print("\n===================================")
    print(f"Berhasil: {success_count}")
    print(f"Dilewati (sudah ada): {skip_count}")
    print(f"Gagal: {fail_count}")
    print("===================================")


if __name__ == "__main__":
    backfill_currency(days=180)