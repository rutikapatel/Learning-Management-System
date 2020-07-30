import json

def lambda_handler(event, context): 
    
    print(event['response']['autoConfirmUser'])
    event['response']['autoConfirmUser']=True
    print(event['response']['autoConfirmUser'])
    print(event['response']['autoVerifyEmail'])
    event['response']['autoVerifyEmail']=True
    print(event['response']['autoVerifyEmail'])
    
    return event
