
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select invoice_ts
from "warehouse"."main"."stg_transactions"
where invoice_ts is null



  
  
      
    ) dbt_internal_test