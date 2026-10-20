import os
import pandas as pd

from airflow.providers.postgres.hooks.postgres import PostgresHook


def load_ihsg():

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(BASE_DIR, "data", "ihsg", "processed", "ihsg_merged.json")

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
        CREATE TABLE IF NOT EXISTS market.ihsg (
            date DATE PRIMARY KEY,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            volume BIGINT
        );
    """)

    insert_query = """
        INSERT INTO market.ihsg (date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (date) DO UPDATE SET
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
    """

    rows = []
    for _, row in df.iterrows():
        rows.append((
            row["date"], row["open"], row["high"],
            row["low"], row["close"], row["volume"]
        ))

    cursor.executemany(insert_query, rows)

    conn.commit()
    cursor.close()
    conn.close()

    print("===================================")
    print("Data IHSG berhasil dimuat ke PostgreSQL")
    print("Total baris:", len(rows))
    print("===================================")


if __name__ == "__main__":
    load_ihsg()