import json
import boto3
import os
import logging
from awslogger import logger
from botocore.session import Session
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from json import JSONEncoder
import ptvsd

#DEBUG_PORT = 5890
#ptvsd.enable_attach(address=('0.0.0.0', DEBUG_PORT), redirect_output=True)
#ptvsd.wait_for_attach()

class UserDDB(Model):

    name = UnicodeAttribute()


def getUser(userId):

    u = UserDDB()
    u.name="Bart Simpson"
    return u.name

def postUser(event):

    u = UserDDB()
    u.name="Homer Simpson"
    return u.name

def lambda_handler(event, context):
 
    if event['resource'] == "/user/{id}" and event['httpMethod'] == 'GET':
        response = getUser(event['pathParameters']['id'])
    elif event['resource'] == "/user/{id}" and event['httpMethod'] == 'POST':
        response = postUser(event)
    else:
        response = "Cant read the data in the {0} environment".format(os.getenv('ACCT_PREFIX'))

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }
