import json
import boto3
from datetime import datetime
import io
import gzip
import sys


s3 = boto3.client('s3')
def lambda_handler(event, context):
    t1 = datetime.now()
    client = boto3.client('dynamodb')

    items = client.scan(TableName='checkSumTable')
    
    if items['Count'] == 0:
        return 0
    else:
        for i in range(items['Count']):

            str_dt1 = items['Items'][i]['uploadedDateTime']['S']
            fileName = items['Items'][i]['fileName']['S']
            compressed = items['Items'][i]['compressed']['S']
            if compressed == 'No':
                dt2 = datetime.now()
                
                dt1 = datetime.strptime(str_dt1, "%Y-%m-%d %H:%M:%S.%f")
                # dt2 = datetime.strptime(str_dt2, "%Y-%m-%d %H:%M:%S.%f")
                
                hours = ((dt2 - dt1).seconds)/3600
                
                if hours > 720.00:
                    obj = s3.get_object(Bucket='myefficientbucket', Key= fileName)
                    buffer = obj['Body'].read()
                    compressed = gzip.compress(buffer)
                    index = fileName.find('.')
                    key =  'archive/' + fileName[:index] + '_compressed' + fileName[index:]
                    s3.put_object(Body=compressed, Bucket='myefficientbucket', Key=key)
                    s3.delete_object(Bucket='myefficientbucket', Key=fileName)
                    compressedSize = float(sys.getsizeof(compressed))
                    compressedSize = compressedSize/(1024*1024)
                    
                    client = boto3.resource('dynamodb')
                    table = client.Table('checkSumTable')
                    key = items['Items'][i]['checkSum']['S']
                    response = table.get_item( Key = { 'checkSum':key } )
                    print(response)
                    item = response['Item']
                    org = float(item['OriginalSize(MB)'])
                    ratio = str((org - compressedSize)/org)
                    t2 = datetime.now()
                    item['compressed'] = 'Yes'
                    item['CompressedSize(MB)'] = str(compressedSize)
                    item['CompressionRatio'] = str(ratio)
                    item['MemorySaved'] = str(org - compressedSize)
                    item['LambdaRunTime(ms)'] = str(((t2 -t1).total_seconds())*1000)
                    table.put_item(Item = item )
            else:
                continue
            
                # # obj = s3.copy_object(Bucket= 'myefficientbucket', Key='archive/img_e1.jpg', CopySource={'Bucket': 'myefficientbucket', 'Key': 'img_11.jpg'})
            

        return 0