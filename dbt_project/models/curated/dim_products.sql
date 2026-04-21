with base as (
    select
        stock_code as product_key,
        any_value(product_description) as product_description
    from {{ ref('stg_transactions') }}
    group by 1
)
select * from base