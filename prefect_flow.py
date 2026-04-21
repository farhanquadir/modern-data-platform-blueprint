from __future__ import annotations
import os
import subprocess
from pathlib import Path

import pandas as pd
from prefect import flow, task
from ucimlrepo import fetch_ucirepo

from scripts.validate_contracts import validate_dataframe
from scripts.load_raw_to_duckdb import load_dataframe_to_duckdb
from scripts.export_analytics import export_tables

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = str(BASE_DIR / "data" / "warehouse" / "retail.duckdb")
CONTRACT_PATH = str(BASE_DIR / "contracts" / "transactions_contract.yaml")
DBT_DIR = str(BASE_DIR / "dbt_project")
EXPORT_DIR = str(BASE_DIR / "exports")

@task
def fetch_dataset() -> pd.DataFrame:
    ds = fetch_ucirepo(id=352)
    df = ds.data.original.copy()
    print(df.head())
    return df

@task
def validate_raw(df: pd.DataFrame) -> None:
    validate_dataframe(df, CONTRACT_PATH)

@task
def persist_raw_csv(df: pd.DataFrame) -> str:
    out = BASE_DIR / "data" / "raw" / "online_retail.csv"
    df.to_csv(out, index=False)
    print(f"Saved raw CSV to {out}")
    return str(out)

@task
def load_raw(df: pd.DataFrame) -> None:
    load_dataframe_to_duckdb(df, DB_PATH, "raw_transactions")

@task
def run_dbt() -> None:
    env = os.environ.copy()
    env["DBT_PROFILES_DIR"] = DBT_DIR
    subprocess.run(["dbt", "deps"], cwd=DBT_DIR, check=False, env=env)
    subprocess.run(["dbt", "build"], cwd=DBT_DIR, check=True, env=env)

@task
def export_outputs() -> None:
    export_tables(DB_PATH, EXPORT_DIR)

@flow(name="modern-data-platform-blueprint")
def retail_platform_flow() -> None:
    df = fetch_dataset()
    validate_raw(df)
    persist_raw_csv(df)
    load_raw(df)
    run_dbt()
    export_outputs()

if __name__ == "__main__":
    retail_platform_flow()