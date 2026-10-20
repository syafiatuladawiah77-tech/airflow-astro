import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@postgres:5432/postgres")

query = """
SELECT
    c.date, c.idr,
    u.usd_index,
    i.close AS ihsg_close
FROM currency.daily_rates c
INNER JOIN market.usd_index u ON c.date = u.date
INNER JOIN market.ihsg i ON c.date = i.date
ORDER BY c.date;
"""

df = pd.read_sql(query, engine)
df["date"] = pd.to_datetime(df["date"])

df["idr_change"] = df["idr"].pct_change() * 100
df["usd_index_change"] = df["usd_index"].pct_change() * 100
df["ihsg_change"] = df["ihsg_close"].pct_change() * 100

df["idr_change_next"] = df["idr_change"].shift(-1)
df_clean = df.dropna()

print("Jumlah baris:", len(df_clean))
print("\nKORELASI LAG: Fitur(t) -> IDR_change(t+1)")
for fitur in ["usd_index_change", "ihsg_change"]:
    korelasi = df_clean[fitur].corr(df_clean["idr_change_next"])
    print(f"{fitur:20s} : {korelasi:.4f}")