
import pymysql
import boto3
import json


rds_host  = 'serverlesslmsystem.cogjula0tv9b.us-east-1.rds.amazonaws.com'
name = 'admin'
password = 'serverlesslmsystem'
db_name = 'project'

print('ssss')
try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    print("Connection Error")
    print(e)
    
def lambda_handler(event, context):

    cur = conn.cursor()
    id=event['request']['userAttributes']['sub']
    query_update='update users set status=1 where id=(%s)'
    values=(id,)
    cur.execute(query_update,values)
    conn.commit()
    response={}
    
    return event

    
        
        

