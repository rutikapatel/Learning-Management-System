import sys
import logging
import pymysql
import json

rds_host  = "serverlesslmsystem.cogjula0tv9b.us-east-1.rds.amazonaws.com"
name = "admin"
password = "serverlesslmsystem"
db_name = "project"

SELECT_USERS_COUNT_QUERY = "SELECT COUNT(username) FROM User"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }

def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def help_user_navigate(ifProcessorAnalyze, helping_user):
    process = "process"
    analyze = "analyze"
    upload = "upload"
    print(ifProcessorAnalyze,helping_user)
    if helping_user is not None and ifProcessorAnalyze is not None:
        print("in helping user and if result")
        if ((process in helping_user) or (analyze in helping_user) or (upload in helping_user)):
            return build_validation_result(False, 'ProcessorAnalyzeResult', "Would you like to process or analyze dada?")
        elif (helping_user.lower() == "yes"):
            return build_validation_result(False, 'ProcessorAnalyzeResult', "Please navigate to top left corder and select process to upload files")
        elif (helping_user.lower() == "ok"):
            return build_validation_result(False, 'ProcessorAnalyzeResult', "Thank you")
        return build_validation_result(False, 'ProcessorAnalyzeResult', "I don't understand what you are saying, can you please repeat?")
    
    if ifProcessorAnalyze is not None:
        print("if process analyze")
        if ((process in ifProcessorAnalyze) or (analyze in ifProcessorAnalyze) or (upload in ifProcessorAnalyze)):
            return build_validation_result(False, 'ProcessorAnalyzeResult', "Would you like to process or analyze data?")
        return build_validation_result(False, 'ProcessorAnalyzeResult', "I don't understand what you are saying, can you please repeat?")
        if (helping_user.lower() == "yes"):
            return build_validation_result(False, 'ProcessorAnalyzeResult', "Please navigate to top and select files to upload files")
        return build_validation_result(False, 'ProcessorAnalyzeResult', "I don't understand what you are saying, can you please repeat?")
    return build_validation_result(True, None, None)


def navigate_user_help(intent_request):
    ifProcessorAnalyze = get_slots(intent_request)["ifProcessorAnalyze"]
    helping_user = get_slots(intent_request)["ProcessorAnalyzeResult"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = help_user_navigate(ifProcessorAnalyze, helping_user)

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))

    return close(intent_request['sessionAttributes'], 'Fulfilled', {'contentType': 'PlainText', 'content': 'I hope that helps, thank you!'})


def Dynamic_user_help(userid):
    db = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5);
    cursor = db.cursor()
    SELECT_ONLINE_USERS_QUERY = "SELECT name FROM users where email = '" + str(userid) + "';"
    cursor.execute(SELECT_ONLINE_USERS_QUERY)
    result = cursor.fetchall()
    SELECT_USERS_ONLINE = "SELECT name from users  where status = 1";
    cursor.execute(SELECT_USERS_ONLINE)
    user_result = cursor.fetchall()
    users_all = ""
    for names in user_result:
        users_all = users_all + str(names)
    print(users_all)
    if userid is not None :
        if (len(result) == 0):
            if userid.lower() == "ok":
                return build_validation_result(False, 'usersloggedin',  "Thank you visit again")
            return build_validation_result(False, 'usersloggedin', "there are no users online or email is incorrect")
        elif (len(result) > 0):
            return build_validation_result(False, 'usersloggedin',  " Users online are" +users_all)
    return build_validation_result(True, None, None)


def DynamicHelp(intent_request):
    userid = get_slots(intent_request)["usersloggedin"]
    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        slots = get_slots(intent_request)
        validation_result = Dynamic_user_help(userid)

        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return delegate(output_session_attributes, get_slots(intent_request))

    return close(intent_request['sessionAttributes'], 'Fulfilled', {'contentType': 'PlainText', 'content': 'I hope that helps, thank you!'})



def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'DynamicHelp':
        return DynamicHelp(intent_request)
    elif intent_name == 'NavigationHelp':
        return navigate_user_help(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    return dispatch(event)
