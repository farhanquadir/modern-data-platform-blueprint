select
    country,
    sum(case when not is_cancellation then gross_line_amount else 0 end) as total_revenue,
    count(distinct invoice_no) as invoice_count,
    count(distinct customer_key) as customer_count
from {{ ref('fct_order_lines') }}
group by 1
order by total_revenue desc