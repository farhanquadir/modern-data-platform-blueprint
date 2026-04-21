
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select unit_price
from "warehouse"."main"."stg_transactions"
where unit_price is null



  
  
      
    ) dbt_internal_test