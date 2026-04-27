import json
import boto3
import uuid
import os
import time

s3_client     = boto3.client('s3')
dynamo_client = boto3.client('dynamodb')

INPUT_BUCKET = os.environ['INPUT_BUCKET']
JOBS_TABLE   = os.environ['JOBS_TABLE']
URL_EXPIRY   = 300

def handler(event, context):
    body = json.loads(event['body'])
    
    filename     = body.get('filename')
    content_type = body.get('contentType')
    
    if not filename or not content_type:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'filename and contentType required'})
        }
    
    job_id  = str(uuid.uuid4())
    s3_key  = f'uploads/{job_id}/{filename}'
    
    # Generate presigned URL
    upload_url = s3_client.generate_presigned_url(
        'put_object',
        Params={
            'Bucket':      INPUT_BUCKET,
            'Key':         s3_key,
            'ContentType': content_type
        },
        ExpiresIn=URL_EXPIRY
    )
    
    # Create job record in DynamoDB
    dynamo_client.put_item(
        TableName=JOBS_TABLE,
        Item={
            'jobId':     { 'S': job_id },
            'status':    { 'S': 'PENDING' },
            'filename':  { 'S': filename },
            's3Key':     { 'S': s3_key },
            'createdAt': { 'S': str(time.time()) },
            'expiresAt': { 'N': str(int(time.time()) + 604800) }
        }
    )
    
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps({
            'jobId':     job_id,
            'uploadUrl': upload_url,
            's3Key':     s3_key
        })
    }