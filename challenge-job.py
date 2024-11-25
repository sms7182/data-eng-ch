import schedule
import time
import psycopg2
import redis
import json
import datetime

connection=psycopg2.connect(database="challenge-db",user="postgres",password="postgres",host="host.docker.internal",port=5432)
cursor=connection.cursor()
rc=redis.Redis("host.docker.internal")

def task():
    sql="select rs.number_of_country,rs.country,rs.sum_of_amount_per_country from (select count(c.customer_id) over(partition by c.country) number_of_country,c.country,sum(o.amount) over(partition by c.country) sum_of_amount_per_country,row_number() over(partition by c.country) r from customers c  join orders o on o.customer_id=c.customer_id) rs where rs.r=1"

    cursor.execute(sql)
        
    orders=cursor.fetchall()
    jo=json.dumps(orders)
    tm=datetime.datetime.now()
    rc.hset("orders_per_country",str(tm),jo)



    

schedule.every().minute.do(task)

while True:
    schedule.run_pending()
    time.sleep(1)