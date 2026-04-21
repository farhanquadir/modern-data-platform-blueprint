with src as (

    select * from {{ source('raw', 'raw_transactions') }}

),

renamed as (

    select
        cast(InvoiceNo as varchar) as invoice_no,
        cast(StockCode as varchar) as stock_code,
        trim(cast(Description as varchar)) as product_description,
        cast(Quantity as integer) as quantity,
        try_strptime(cast(InvoiceDate as varchar), '%m/%d/%Y %H:%M') as invoice_ts,
        cast(UnitPrice as double) as unit_price,
        cast(CustomerID as varchar) as customer_id,
        trim(cast(Country as varchar)) as country
    from src

),

cleaned as (

    select
        invoice_no,
        stock_code,
        nullif(product_description, '') as product_description,
        quantity,
        invoice_ts,
        unit_price,
        nullif(customer_id, '') as customer_id,
        country,
        case when lower(invoice_no) like 'c%%' or quantity < 0 then true else false end as is_cancellation,
        abs(quantity) as abs_quantity,
        abs(quantity) * unit_price as gross_line_amount
    from renamed
    where invoice_no is not null
      and stock_code is not null
      and invoice_ts is not null
      and unit_price is not null
      and country is not null

)

select * from cleaned