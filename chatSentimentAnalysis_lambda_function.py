import json
import boto3

def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    name = event['Records'][0]['s3']['object']['key']
    file = s3.Object("group10chatdata", name)
    filename = name.split(".")
    content = json.load(file.get()['Body'])
    lines = []
    for i in content:
        lines.append(i['message'])
    
    comprehend = boto3.client("comprehend")
    FinalData = []
    
    for i in range(0,len(lines)):
        ans = comprehend.detect_sentiment(Text = lines[i], LanguageCode = "en")
        dict = {
            "message" : lines[i],
            "sentiment" : ans["Sentiment"]
        }
        FinalData.append(dict)
    print("filename" + filename[0])
    with open("/tmp/"+filename[0]+"Sentiment.json","w") as file:
        json.dump(FinalData,file)
    print("file created")
    
    s3_client = boto3.client("s3")
    s3_client.upload_file("/tmp/"+filename[0]+"Sentiment.json","group10chatsentiment",filename[0]+"Sentiment.json")   
    
     
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
