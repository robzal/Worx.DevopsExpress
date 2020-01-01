import json
import boto3
import os
import logging
from awslogger import logger
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from botocore.session import Session
import ptvsd

USER_TABLE_NAME = os.environ["USER_TABLE_NAME"]
DEBUG_PORT = 5890

#ptvsd.enable_attach(address=('0.0.0.0', DEBUG_PORT), redirect_output=True)
#ptvsd.wait_for_attach()

class UserDDB(Model):
    class Meta:
        table_name = USER_TABLE_NAME
        region = Session().get_config_variable("region")

    userid = UnicodeAttribute(hash_key=True)
    surname = UnicodeAttribute()
    firstname = UnicodeAttribute()


def getUser(userId):

    try:
        msg = "Reading {0} Table for Key {1}".format(USER_TABLE_NAME,userId)
        logger.info(msg)
        u = UserDDB.get(userId)
        return [
            u.firstname
        ]
    except Exception as e:
        emsg = "Error reading {0} Table for Key {1}".format(USER_TABLE_NAME,userId)
        logger.error(emsg)
        logger.error(print(e))
        return [
            emsg
        ]

def postUser(event):

    u = UserDDB()
    userId = "unknown"
    try:
        data = json.loads(event["body"])
        userId = data["userid"]
        surname = data["surname"]
        firstname = data["firstname"]
        try:
            u = UserDDB.get(userId)
        except Exception as e:
            u = UserDDB()
            u.userid = userId
        u.surname = surname
        u.firstname = firstname
        u.save()

        return [
            data
        ]
    except Exception as e:
        emsg = "Error saving data in {0} Table for Key {1}".format(USER_TABLE_NAME,userId)
        logger.error(emsg)
        logger.error(print(e))
        return [
            emsg
        ]

def lambda_handler(event, context):
 
    if event['resource'] == "/user/{id}" and event['httpMethod'] == 'GET':
        response = getUser(event['pathParameters']['id'])
    elif event['resource'] == "/user/{id}" and event['httpMethod'] == 'POST':
        response = postUser(event)
    else:
        response = os.getenv('ACCT_PREFIX')

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
