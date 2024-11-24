import schedule
import time
import psycopg2
import redis
import json


connection=psycopg2.connect(database="challenge-db",user="postgres",password="postgres",host="127.0.0.1",port=5432)
cursor=connection.cursor()
rc=redis.Redis("host.docker.internal")

def task():
    sql="select rs.number_of_country,rs.country,rs.sum_of_amount_per_country from (select count(c.customer_id) over(partition by c.country) number_of_country,c.country,sum(o.amount) over(partition by c.country) sum_of_amount_per_country,row_number() over(partition by c.country) r from customers c  join orders o on o.customer_id=c.customer_id) rs where rs.r=1"
    lso=rc.get("last_order")
    last_order_id=0
    if lso is None:
        cursor.execute(sql,[-1])
    else:
        lso_str=json.loads(lso)
        last_order_id=int(lso_str)
        cursor.execute(sql,[int(last_order_id)])
        
    orders=cursor.fetchall()
    rc.set()

    for row in orders:
        order={"order_id":row[0],"customer_id":row[1],"order_date":row[2],"amount":row[3]}
        jo=json.dumps(order)
        rc.hset("orders",row[0],jo)
        last_order_id=row[0]
    rc.set("last_order",last_order_id)    

    sqlCustomer="select * from customers  where customer_id> %s"
    lsc=rc.get("last_customer")
    last_customer_id=0
    if lsc is None:
        cursor.execute(sqlCustomer,[-1])
    else:
        lastCs_str=json.loads(lsc)
        last_customer_id=int(lastCs_str)
        cursor.execute(sqlCustomer,[int(last_customer_id)])
    customers=cursor.fetchall()
    

    for row in customers:
        customer={"customer_id":row[0],"customer_name":row[1],"country":row[2]}
        jo=json.dumps(customer)
        rc.hset("customers",row[0],jo)
        last_customer_id=row[0]

    rc.set("last_customer",last_customer_id)    


    

schedule.every().minute.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)