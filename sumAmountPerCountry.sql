select rs.number_of_country,rs.country,rs.sum_of_amount_per_country
 from (select count(c.customer_id) over(partition by c.country) number_of_country,c.country,sum(o.amount) over(partition by c.country) sum_of_amount_per_country,row_number() over(partition by c.country) r 
																		  from customers c  join orders o on o.customer_id=c.customer_id) rs where rs.r=1