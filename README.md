# Modern Data Platform Blueprint

A compact end-to-end data platform project demonstrating how raw business data can be transformed into analytics-ready datasets using a layered warehouse design, data contracts, orchestration, and reproducible transformations.

This project was designed as a portfolio-ready architecture demo for AI and data platform roles. It shows how to move from raw ingestion to governed analytics outputs in a lightweight but realistic stack.

## Why this project

Many portfolio projects focus only on machine learning models. This project instead demonstrates the data foundation that supports analytics, BI, and future AI applications.

It is built to showcase:
- layered data architecture
- ETL/ELT pipeline design
- schema validation and data contracts
- warehouse-style modeling
- orchestration and reproducibility
- analytics delivery for downstream BI and AI use cases

## Architecture

The project follows a medallion-style flow:

**Raw -> Staging -> Curated -> Analytics**

### Raw
Source data is ingested into DuckDB as `raw_transactions`.

### Staging
Data is standardized and cleaned in dbt models:
- column renaming
- timestamp parsing
- null handling
- cancellation flags
- business-friendly derived fields

### Curated
Reusable business entities are created:
- `dim_customers`
- `dim_products`
- `dim_dates`
- `fct_order_lines`

### Analytics
Reporting-ready marts are built:
- `mart_monthly_revenue`
- `mart_top_customers`
- `mart_country_sales`
- `ai_customer_context`

The `ai_customer_context` table is intentionally included as an AI-ready layer that can later support RAG or LLM applications.

## Tech stack

- **Python** for ingestion, validation, export, and visualization
- **DuckDB** as the lightweight warehouse
- **dbt-duckdb** for transformations and testing
- **Prefect** for orchestration
- **YAML data contracts** for schema and quality expectations
- **Matplotlib** for analytics visualizations
- **Google Colab** for fast execution and demo portability

## Dataset

This project uses the **UCI Online Retail** dataset, a public transactional dataset containing invoices, products, quantities, timestamps, prices, customer IDs, and countries.

It is a good fit for demonstrating a business-oriented warehouse pipeline because it resembles retail sales data commonly used in reporting and analytics scenarios.

## Repository structure

```text
modern-data-platform-blueprint/
├── contracts/
│   └── transactions_contract.yaml
├── data/
│   └── warehouse/
│       └── warehouse.db
├── dbt_project/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   └── models/
│       ├── staging/
│       ├── curated/
│       └── analytics/
├── exports/
│   ├── *.csv
│   └── figures/
├── scripts/
│   ├── load_raw_to_duckdb.py
│   ├── validate_contracts.py
│   ├── export_analytics.py
│   └── visualize_analytics.py
├── prefect_flow.py
└── Modern_Data_Platform_Blueprint_Colab.ipynb


## Core pipeline steps
1. Load raw data into DuckDB

The raw UCI dataset is loaded into the warehouse as raw_transactions.

2. Validate against a data contract

A YAML contract checks expected fields, numeric constraints, and core schema assumptions.

3. Run dbt models

dbt transforms the raw table into staging, curated, and analytics layers.

4. Export marts

Analytics-ready tables are exported as CSV files.

5. Visualize outputs

A plotting script produces summary charts for portfolio presentation.