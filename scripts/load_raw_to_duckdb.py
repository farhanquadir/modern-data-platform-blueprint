from __future__ import annotations
from pathlib import Path
import duckdb
import pandas as pd


def load_dataframe_to_duckdb(
    df: pd.DataFrame,
    db_path: str,
    table_name: str = "raw_transactions",
) -> None:
    df = df.copy()

    for col in ["UnitPrice", "Quantity"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required_numeric = [c for c in ["UnitPrice", "Quantity"] if c in df.columns]
    if required_numeric:
        df = df.dropna(subset=required_numeric)

    if "UnitPrice" in df.columns:
        df = df[df["UnitPrice"] >= 0]

    if "Quantity" in df.columns:
        df = df[df["Quantity"] >= 0]

    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(db_file))
    con.register("tmp_df", df)
    con.execute(f"create or replace table {table_name} as select * from tmp_df")
    con.close()

    print(f"Loaded {len(df):,} rows into {db_file}:{table_name}")