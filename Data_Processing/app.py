from flask import Flask, render_template, request
import os
import boto3
from botocore.client import Config
from werkzeug.utils import secure_filename
from botocore.exceptions import NoCredentialsError

ACCESS_KEY_ID = 'AKIAXTA4CVO3RZJ5QV7N'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'group10dataprocessing'
FILE_NAME = '001.txt';
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET','POST'])
def data():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        print (f.save(secure_filename(f.filename)))
        file_name =os.path.join("",f.filename)
        s3_name = os.path.join("",f.filename)
        data = open(FILE_NAME, 'rb')

        upload_to_aws(file_name,BUCKET_NAME,s3_name)
        print ("Done")

        data = []
        return render_template('data.html',data=data)

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
if __name__ == '__main__':
    app.run(debug=True,port=8080)
