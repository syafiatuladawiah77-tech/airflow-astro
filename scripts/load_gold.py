import json
import os
from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_gold():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    input_file = os.path.join(
        BASE_DIR,
        "data",
        "gold",
        "processed",
        "gold_merged.json"
    )

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"File processed gold tidak ditemukan: {input_file}"
        )

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not data:
        raise ValueError("Data gold kosong.")

    postgres_hook = PostgresHook(
        postgres_conn_id="worldbank_postgres"
    )

    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    # Buat schema
    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS commodity;
    """)

    # Buat tabel gold
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS commodity.gold_price (
            date DATE PRIMARY KEY,
            xau_per_usd DOUBLE PRECISION,
            gold_usd_per_ounce DOUBLE PRECISION
        );
    """)

    # Insert / update data
    for row in data:
        cursor.execute("""
            INSERT INTO commodity.gold_price (
                date,
                xau_per_usd,
                gold_usd_per_ounce
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (date)
            DO UPDATE SET
                xau_per_usd = EXCLUDED.xau_per_usd,
                gold_usd_per_ounce = EXCLUDED.gold_usd_per_ounce;
        """, (
            row["date"][:10],
            row["xau_per_usd"],
            row["gold_usd_per_ounce"]
        ))

    conn.commit()

    cursor.close()
    conn.close()

    print("===================================")
    print("Load data emas berhasil")
    print(f"Total data diproses: {len(data)}")
    print("Tabel: commodity.gold_price")
    print("===================================")


if __name__ == "__main__":
    load_gold()