import json
import urllib.parse
import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

print('Loading function')

s3 = boto3.client('s3')


def lambda_handler(event, context):
    
    print("event=",  event)
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    # print("bucket=", bucket)
   
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    ind = key.find('archive/')
    if ind != -1:
        return 0
    response = s3.get_object(Bucket=bucket_name, Key=key)
   
    print("response", response)
    size = response['ContentLength']
    size = str(size/(1024*1024))
    
    etag = str(response['ETag'])
   
   

    client = boto3.resource('dynamodb')
    table = client.Table('checkSumTable')
    response = table.get_item( Key = { 'checkSum':str(response['ETag']) } )
    try:
        item = response['Item']
        if str(item['checkSum']) == etag:
            s3.delete_object(Bucket=bucket_name, Key=key)
            print("deleted succesfully", key)
    except:
        table.put_item(Item = { 'checkSum': etag, 'fileName': key, 'uploadedDateTime': str(datetime.now()), 'compressed': 'No', 'OriginalSize(MB)': size, 'CompressedSize(MB)': "NotUpdated", 'CompressionRatio': "NotUpdated"} )
        
    return 0