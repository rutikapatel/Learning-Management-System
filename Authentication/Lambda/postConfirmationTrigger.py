
import pymysql
import boto3
import json


rds_host  = 'serverlesslmsystem.cogjula0tv9b.us-east-1.rds.amazonaws.com'
name = 'admin'
password = 'serverlesslmsystem'
db_name = 'project'

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    print('abc')
    print("Connection Error")
    print(e)
    
def lambda_handler(event, context):
    print('aaa')
    cur = conn.cursor()
    id=event['request']['userAttributes']['sub']
    email=event['request']['userAttributes']['email']
    name=event['request']['userAttributes']['name']
    print(event)
    organization=event['request']['userAttributes']['custom:organization']

    query_select='insert into users(id,name,email,organization) values(%s,%s,%s,%s)'
    values=(id,name,email,organization)
    cur.execute(query_select,values)
    conn.commit()
    
    return event
        
