import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
ACCESS_KEY_ID = 'AKIAXTA4CVO3RZJ5QV7N'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'group10dataprocessing'
FILE_NAME = '003.txt';
s3_file = '003.txt'


def upload_to_aws(FILE_NAME, BUCKET_NAME, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY)

    try:
        s3.upload_file(FILE_NAME, BUCKET_NAME, s3_file)
        print("Upload Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


upload_to_aws(FILE_NAME, BUCKET_NAME, s3_file)