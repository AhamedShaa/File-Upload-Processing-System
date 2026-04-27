import json
import boto3
import os
import time
from PIL import Image
import io

s3_client     = boto3.client('s3')
dynamo_client = boto3.client('dynamodb')

INPUT_BUCKET  = os.environ['INPUT_BUCKET']
OUTPUT_BUCKET = os.environ['OUTPUT_BUCKET']
JOBS_TABLE    = os.environ['JOBS_TABLE']

SIZES = [
    ('large',     1200),
    ('thumbnail', 200),
]

def handler(event, context):
    for sqs_record in event['Records']:
        s3_event = json.loads(sqs_record['body'])
        
        for s3_record in s3_event['Records']:
            src_key = s3_record['s3']['object']['key']
            job_id  = src_key.split('/')[1]
            
            print(f"Processing: {src_key}")
            
            try:
                # Download original image from S3
                response   = s3_client.get_object(
                    Bucket=INPUT_BUCKET,
                    Key=src_key
                )
                image_data = response['Body'].read()
                
                # Open image with Pillow
                image = Image.open(io.BytesIO(image_data))
                
                if image.mode in ('RGBA', 'P'):
                    image = image.convert('RGB')
                
                output_keys = {}
                
                for size_name, width in SIZES:
                    resized = resize_image(image, width)
                    
                    out_key = src_key.replace(
                        'uploads/', 
                        f'processed/{size_name}/'
                    )
                    
                    buffer = io.BytesIO()
                    resized.save(buffer, format='JPEG', quality=85)
                    buffer.seek(0)
                    
                    s3_client.put_object(
                        Bucket=OUTPUT_BUCKET,
                        Key=out_key,
                        Body=buffer,
                        ContentType='image/jpeg'
                    )
                    
                    output_keys[size_name] = out_key
                    print(f"Saved {size_name}: {out_key}")
                
                # Update job status to DONE
                dynamo_client.update_item(
                    TableName=JOBS_TABLE,
                    Key={ 'jobId': { 'S': job_id } },
                    UpdateExpression='SET #s = :done, outputKeys = :keys, processedAt = :ts',
                    ExpressionAttributeNames={ '#s': 'status' },
                    ExpressionAttributeValues={
                        ':done': { 'S': 'DONE' },
                        ':keys': { 'S': json.dumps(output_keys) },
                        ':ts':   { 'S': str(time.time()) }
                    }
                )

            except Exception as e:
                print(f"Failed processing {src_key}: {str(e)}")
                
                # Update job status to FAILED
                dynamo_client.update_item(
                    TableName=JOBS_TABLE,
                    Key={ 'jobId': { 'S': job_id } },
                    UpdateExpression='SET #s = :failed, errorMsg = :e',
                    ExpressionAttributeNames={ '#s': 'status' },
                    ExpressionAttributeValues={
                        ':failed': { 'S': 'FAILED' },
                        ':e':      { 'S': str(e) }
                    }
                )
                raise

def resize_image(image, target_width):
    width, height = image.size
    ratio         = target_width / width
    target_height = int(height * ratio)
    
    return image.resize(
        (target_width, target_height),
        Image.LANCZOS
    )