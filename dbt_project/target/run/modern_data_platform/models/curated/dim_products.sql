
  
    
    

    create  table
      "warehouse"."main"."dim_products__dbt_tmp"
  
    as (
      with base as (
    select
        stock_code as product_key,
        any_value(product_description) as product_description
    from "warehouse"."main"."stg_transactions"
    group by 1
)
select * from base
    );
  
  