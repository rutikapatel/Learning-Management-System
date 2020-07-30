from flask import jsonify
from google.cloud import firestore

db = firestore.Client()

def storeQA(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'question' in request_json:
        question = request_json['question']
    elif request_args and 'question' in request_args:
        question = request_args['question']

    if request_json and 'answer' in request_json:
        answer = request_json['answer']
    elif request_args and 'answer' in request_args:
        answer = request_args['answer']

    if request_json and 'id' in request_json:
        id = request_json['id']
    elif request_args and 'id' in request_args:
        id = request_args['id']

    data = {'question':question,'answer':answer,'id':id}
    print(data)
    db.collection(u'qa').add(data)

    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('True', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return ('True', 200, headers)

