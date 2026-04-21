from __future__ import annotations
from pathlib import Path
import duckdb

EXPORT_TABLES = [
    "mart_monthly_revenue",
    "mart_top_customers",
    "mart_country_sales",
    "ai_customer_context",
]

def export_tables(db_path: str, export_dir: str) -> None:
    export_path = Path(export_dir)
    export_path.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(db_path)
    for table in EXPORT_TABLES:
        df = con.execute(f"select * from {table}").df()
        outfile = export_path / f"{table}.csv"
        df.to_csv(outfile, index=False)
        print(f"Exported {outfile}")
    con.close()