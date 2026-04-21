select
    customer_key,
    any_value(country) as country,
    count(distinct invoice_no) as invoice_count,
    sum(case when not is_cancellation then gross_line_amount else 0 end) as total_revenue,
    max(invoice_ts) as last_order_ts
from {{ ref('fct_order_lines') }}
where customer_key <> 'UNKNOWN'
group by 1
order by total_revenue desc
limit 25