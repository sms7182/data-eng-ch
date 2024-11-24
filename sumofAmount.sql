select sum(o.amount) sumOfAmount,c.customer_name from customers c  
join orders o on o.customer_id=c.customer_id
where c.country='USA'
group by c.customer_id,c.customer_name

