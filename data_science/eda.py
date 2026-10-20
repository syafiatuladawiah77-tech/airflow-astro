import pandas as pd
from sqlalchemy import create_engine


# ==========================================
# 1. KONEKSI KE POSTGRESQL
# ==========================================

engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgres:5432/postgres"
)


# ==========================================
# 2. JOIN 3 TABEL
# ==========================================

query = """
SELECT
    c.date,
    c.idr,
    c.myr,
    c.sgd,
    c.thb,
    c.php,
    g.gold_usd_per_ounce,
    u.usd_index
FROM currency.daily_rates c
INNER JOIN commodity.gold_price g
    ON c.date = g.date
INNER JOIN market.usd_index u
    ON c.date = u.date
ORDER BY c.date;
"""


# ==========================================
# 3. AMBIL DATA KE DATAFRAME
# ==========================================

df = pd.read_sql(query, engine)

df["date"] = pd.to_datetime(df["date"])


# ==========================================
# 4. CEK DATA AWAL
# ==========================================

print("\n====================================")
print("DATASET HASIL JOIN 3 TABEL")
print("====================================")

print("\nJumlah baris dan kolom:")
print(df.shape)

print("\n5 data pertama:")
print(df.head())

print("\nTipe data:")
print(df.dtypes)

print("\nMissing value:")
print(df.isnull().sum())

print("\nJumlah duplikat:")
print(df.duplicated().sum())

print("\nRentang tanggal:")
print(df["date"].min(), "sampai", df["date"].max())

# ==========================================
# 5. STATISTIK DESKRIPTIF
# ==========================================

print("\n====================================")
print("STATISTIK DESKRIPTIF")
print("====================================")

kolom_numerik = [
    "idr",
    "myr",
    "sgd",
    "thb",
    "php",
    "gold_usd_per_ounce",
    "usd_index"
]

statistik = df[kolom_numerik].describe().T

print(statistik.round(4))