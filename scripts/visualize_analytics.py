from __future__ import annotations

from pathlib import Path
import duckdb
import pandas as pd
import matplotlib.pyplot as plt


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_monthly_revenue(con: duckdb.DuckDBPyConnection, output_dir: Path) -> None:
    query = """
    select year_month, revenue, invoices, order_lines
    from mart_monthly_revenue
    order by year_month
    """
    df = con.execute(query).fetchdf()

    if df.empty:
        print("mart_monthly_revenue is empty. Skipping monthly revenue plot.")
        return

    df["year_month"] = pd.to_datetime(df["year_month"])

    plt.figure(figsize=(10, 5))
    plt.plot(df["year_month"], df["revenue"], marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    out = output_dir / "monthly_revenue_trend.png"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


def plot_top_customers(con: duckdb.DuckDBPyConnection, output_dir: Path, top_n: int = 10) -> None:
    query = f"""
    select *
    from mart_top_customers
    order by total_revenue desc
    limit {top_n}
    """
    df = con.execute(query).fetchdf()

    if df.empty:
        print("mart_top_customers is empty. Skipping top customers plot.")
        return

    df = df.sort_values("total_revenue", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["customer_key"].astype(str), df["total_revenue"])
    plt.title(f"Top {top_n} Customers by Revenue")
    plt.xlabel("Total Revenue")
    plt.ylabel("Customer")
    plt.tight_layout()
    out = output_dir / "top_customers.png"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


def plot_country_sales(con: duckdb.DuckDBPyConnection, output_dir: Path, top_n: int = 10) -> None:
    query = f"""
    select *
    from mart_country_sales
    order by total_revenue desc
    limit {top_n}
    """
    df = con.execute(query).fetchdf()

    if df.empty:
        print("mart_country_sales is empty. Skipping country sales plot.")
        return

    df = df.sort_values("total_revenue", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(df["country"], df["total_revenue"])
    plt.title(f"Top {top_n} Countries by Revenue")
    plt.xlabel("Total Revenue")
    plt.ylabel("Country")
    plt.tight_layout()
    out = output_dir / "country_sales.png"
    plt.savefig(out, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved {out}")


def main() -> None:
    base = Path(__file__).resolve().parents[1]
    db_path = base / "data" / "warehouse" / "warehouse.db"
    output_dir = base / "exports" / "figures"

    _ensure_dir(output_dir)

    if not db_path.exists():
        raise FileNotFoundError(f"DuckDB file not found: {db_path}")

    con = duckdb.connect(str(db_path), read_only=True)
    try:
        plot_monthly_revenue(con, output_dir)
        plot_top_customers(con, output_dir, top_n=10)
        plot_country_sales(con, output_dir, top_n=10)
    finally:
        con.close()


if __name__ == "__main__":
    main()