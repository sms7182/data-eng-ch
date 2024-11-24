select rs.samount,rs.customer_name from (
select sum(o.amount) over(partition by o.customer_id) samount,c.customer_name,row_number() over(partition by o.customer_id) r from customers c  
join orders o on o.customer_id=c.customer_id) rs where rs.r=1 order by  rs.samount desc limit 3


