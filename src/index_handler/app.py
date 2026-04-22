import json
import boto3
import os

s3 = boto3.client('s3')

STATIC_SITE_BUCKET = os.environ.get('STATIC_SITE_BUCKET')

def lambda_handler(event, context):
    """
    GET / - Returns the index.html page
    """
    try:
        if not STATIC_SITE_BUCKET:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Static site bucket not configured'})
            }
        
        response = s3.get_object(Bucket=STATIC_SITE_BUCKET, Key='index.html')
        html_content = response['Body'].read().decode('utf-8')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': html_content
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
