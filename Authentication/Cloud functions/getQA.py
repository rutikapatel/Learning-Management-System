from flask import jsonify
from google.cloud import firestore
import json

db = firestore.Client()

def getQuestion(request):

    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'id' in request_json:
        id = request_json['id']
    elif request_args and 'id' in request_args:
        id = request_args['id']

    ref=db.collection(u'qa').where(u'id', u'==', id).stream()
    for i in ref:
        data=i.to_dict()
    res={'question':data['question'],'answer':data['answer']}
    return json.dumps(res)
