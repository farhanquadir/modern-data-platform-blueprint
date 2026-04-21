with base as (
    select distinct
        cast(invoice_ts as date) as date_key,
        extract(year from invoice_ts) as year_num,
        extract(month from invoice_ts) as month_num,
        strftime(cast(invoice_ts as date), '%Y-%m') as year_month
    from "warehouse"."main"."stg_transactions"
)
select * from base