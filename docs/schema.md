# Schema design

## Raw
- `raw_transactions`
  - one row per invoice line from source

## Staging
- `stg_transactions`
  - standardized names and types
  - cancellation flag
  - gross line amount

## Curated
- `dim_customers`
- `dim_products`
- `dim_dates`
- `fct_order_lines`

## Analytics
- `mart_monthly_revenue`
- `mart_top_customers`
- `mart_country_sales`
- `ai_customer_context`
