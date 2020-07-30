import boto3 
import string 
import json 
from stop_words import get_stop_words
import csv
    
def lambda_handler(event, context): 
     
    s3 = boto3.client("s3") 
     
    if event:         
        print("Event :", event)         
        file_obj = event["Records"][0]         
        filename = str(file_obj["s3"]["object"]['key'])         
        print("Filename: ", filename) 
        file_obj = s3.get_object(Bucket = "group10dataprocessing", Key = filename)         
        file_content = file_obj["Body"].read().decode('utf-8') 
        
        filtered_words = [word for word in file_content.split() if word not in get_stop_words('english')]
        
        named={}
        word_list=[]
        for i in filtered_words:
            if i[0].isupper():
                a=i.lstrip()
                a=i.replace('\n','')
                if a in named:
                    named[a] += 1
                else:
                    named[a] = 1
        #print (named)
        result = json.dumps(named)
        #print (result)
        json_name=filename[0]+filename[1]+filename[2]+"word_cloud.txt"
        lambda_path = "/tmp/" + json_name         
        s3_path = "/" + json_name 
        encoded_string = result.encode("utf-8")         
        with open(lambda_path, 'w+') as file: 
            file.write(result)             
        file.close() 
        s3 = boto3.resource("s3") 
        s3.Bucket('group10dataprocessing').put_object(Key=s3_path, Body=encoded_string) 

