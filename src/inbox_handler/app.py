import json
import boto3
import os
import uuid

s3 = boto3.client('s3')

INBOX_BUCKET = os.environ.get('INBOX_BUCKET')

def lambda_handler(event, context):
    """
    POST /api/inbox - Upload image to S3 inbox
    GET /api/inbox - List images in inbox
    DELETE /api/inbox/{key} - Delete image from inbox
    """
    try:
        method = event.get('httpMethod', 'POST')
        
        if method == 'POST':
            # Handle multipart file upload
            # This is a simplified version; in production you'd handle multipart properly
            file_name = f"upload-{uuid.uuid4()}.jpg"
            
            # For now, just return the key that would be used
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'objectKey': file_name, 'bucket': INBOX_BUCKET})
            }
        
        elif method == 'GET':
            # List objects in inbox
            response = s3.list_objects_v2(Bucket=INBOX_BUCKET)
            files = [obj['Key'] for obj in response.get('Contents', [])]
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'files': files})
            }
        
        elif method == 'DELETE':
            # Delete specific file
            key = event['pathParameters']['key']
            s3.delete_object(Bucket=INBOX_BUCKET, Key=key)
            
            return {
                'statusCode': 204,
                'body': json.dumps({})
            }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
