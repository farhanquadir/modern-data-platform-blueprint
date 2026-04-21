select
    d.year_month,
    sum(case when not f.is_cancellation then f.gross_line_amount else 0 end) as revenue,
    count(distinct f.invoice_no) as invoices,
    count(*) as order_lines
from "warehouse"."main"."fct_order_lines" f
left join "warehouse"."main"."dim_dates" d
  on f.date_key = d.date_key
group by 1
order by 1