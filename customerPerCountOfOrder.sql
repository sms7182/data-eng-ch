select c.customer_name,count(o.order_id)  number_of_order from customers c  
join orders o on o.customer_id=c.customer_id
group by c.customer_id,c.customer_name

