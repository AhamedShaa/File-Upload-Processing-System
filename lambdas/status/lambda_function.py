import json
import boto3
import os

dynamo_client = boto3.client('dynamodb')
JOBS_TABLE    = os.environ['JOBS_TABLE']

def handler(event, context):
    job_id = event['pathParameters']['jobId']
    
    response = dynamo_client.get_item(
        TableName=JOBS_TABLE,
        Key={ 'jobId': { 'S': job_id } }
    )
    
    item = response.get('Item')
    
    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'job not found'})
        }
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'jobId':       item['jobId']['S'],
            'status':      item['status']['S'],
            'filename':    item['filename']['S'],
            'createdAt':   item['createdAt']['S'],
            'processedAt': item.get('processedAt', {}).get('S', None),
            'outputKeys':  json.loads(item['outputKeys']['S']) if 'outputKeys' in item else None,
            'errorMsg':    item.get('errorMsg', {}).get('S', None)
        })
    }