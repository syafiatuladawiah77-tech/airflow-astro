import pandas as pd
import os

from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_currency():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    file_path = os.path.join(
        BASE_DIR,
        "data",
        "currency",
        "processed",
        "currency_merged.json"
    )

    df = pd.read_json(file_path, orient="records")

    hook = PostgresHook(
        postgres_conn_id="worldbank_postgres"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS currency;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS currency.daily_rates (
            date DATE PRIMARY KEY,
            idr DOUBLE PRECISION,
            myr DOUBLE PRECISION,
            sgd DOUBLE PRECISION,
            thb DOUBLE PRECISION,
            php DOUBLE PRECISION
        );
    """)

    insert_query = """
        INSERT INTO currency.daily_rates (
            date,
            idr,
            myr,
            sgd,
            thb,
            php
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
            idr = EXCLUDED.idr,
            myr = EXCLUDED.myr,
            sgd = EXCLUDED.sgd,
            thb = EXCLUDED.thb,
            php = EXCLUDED.php;
    """

    rows = []

    for _, row in df.iterrows():
        rows.append((
            row["date"],
            row["idr"],
            row["myr"],
            row["sgd"],
            row["thb"],
            row["php"],
        ))

    cursor.executemany(insert_query, rows)

    conn.commit()
    cursor.close()
    conn.close()

    print("===================================")
    print("Data currency berhasil dimuat ke PostgreSQL")
    print("Total baris:", len(rows))
    print("===================================")


if __name__ == "__main__":
    load_currency()