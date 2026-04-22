import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

JOB_STATE_TABLE = os.environ.get('JOB_STATE_TABLE')
table = dynamodb.Table(JOB_STATE_TABLE)

def lambda_handler(event, context):
    """
    GET /api/jobs/{id} - Poll job status
    """
    try:
        job_id = event['pathParameters']['id']
        
        response = table.get_item(Key={'jobId': job_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Job not found'})
            }
        
        item = response['Item']
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'jobId': item['jobId'],
                'status': item.get('status', 'PROCESSING'),
                'extractedText': item.get('extractedText', ''),
                'createdAt': item.get('createdAt')
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
