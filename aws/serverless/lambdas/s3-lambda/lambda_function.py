import json
import boto3
import os
import sys
import uuid
# import requests


def lambda_handler(event, context):

    # Create an S3 client
    s3 = boto3.client('s3')

    # # Call S3 to list current buckets
    # response = s3.list_buckets()

    # # Get a list of all bucket names from the response
    # buckets = [bucket['Name'] for bucket in response['Buckets']]

    # # Print out the bucket list
    # print("Bucket List: %s" % buckets)

    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        s3.download_file(bucket, key, download_path)
   
    f = open(download_path, "r")
    print(f.read())

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f.read(),
            # "location": ip.text.replace("\n", "")
        }),
    }
