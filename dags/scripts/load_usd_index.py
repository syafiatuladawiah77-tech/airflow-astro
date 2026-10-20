import os
import pandas as pd

from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_usd_index():

    file_path = "/usr/local/airflow/dags/data/usd_index/processed/usd_index_processed.json"

    df = pd.read_json(file_path, orient="records")

    hook = PostgresHook(
        postgres_conn_id="worldbank_postgres"
    )

    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS market;
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS market.usd_index (
            date DATE PRIMARY KEY,
            usd_index DOUBLE PRECISION
        );
    """)

    insert_query = """
        INSERT INTO market.usd_index (date, usd_index)
        VALUES (%s, %s)
        ON CONFLICT (date) DO UPDATE SET
            usd_index = EXCLUDED.usd_index;
    """

    rows = []

    for _, row in df.iterrows():
        rows.append((
            row["date"],
            row["usd_index"],
        ))

    cursor.executemany(insert_query, rows)

    conn.commit()
    cursor.close()
    conn.close()

    print("===================================")
    print("Data Dollar Index berhasil dimuat ke PostgreSQL")
    print("Total baris:", len(rows))
    print("===================================")


if __name__ == "__main__":
    load_usd_index()
