with ranked as (

    select
        coalesce(customer_id, 'UNKNOWN') as customer_key,
        country,
        invoice_ts,
        row_number() over (
            partition by coalesce(customer_id, 'UNKNOWN')
            order by invoice_ts desc, country
        ) as rn
    from {{ ref('stg_transactions') }}

)

select
    customer_key,
    country
from ranked
where rn = 1