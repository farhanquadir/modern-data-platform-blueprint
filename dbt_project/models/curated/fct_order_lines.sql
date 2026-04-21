with base as (

    select
        invoice_no,
        stock_code,
        coalesce(customer_id, 'UNKNOWN') as customer_key,
        invoice_ts,
        cast(invoice_ts as date) as date_key,
        country,
        is_cancellation,
        quantity,
        abs_quantity,
        unit_price,
        gross_line_amount,
        row_number() over (
            order by
                invoice_no,
                stock_code,
                invoice_ts,
                coalesce(customer_id, 'UNKNOWN'),
                country,
                quantity,
                unit_price,
                gross_line_amount
        ) as order_line_id
    from {{ ref('stg_transactions') }}

)

select
    cast(order_line_id as varchar) as order_line_id,
    invoice_no,
    stock_code as product_key,
    customer_key,
    date_key,
    invoice_ts,
    country,
    is_cancellation,
    quantity,
    abs_quantity,
    unit_price,
    gross_line_amount
from base