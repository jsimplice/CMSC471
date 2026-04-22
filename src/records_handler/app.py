import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

JOB_STATE_TABLE = os.environ.get('JOB_STATE_TABLE')
table = dynamodb.Table(JOB_STATE_TABLE)

def lambda_handler(event, context):
    """
    GET /api/records - Get all records
    DELETE /api/records/{id} - Delete specific record
    """
    try:
        method = event.get('httpMethod', 'GET')
        
        if method == 'GET':
            # Scan all items (in production, use pagination)
            response = table.scan()
            items = response.get('Items', [])
            
            records = []
            for item in items:
                if item.get('extractedText'):
                    records.append({
                        'jobId': item['jobId'],
                        'extractedText': item['extractedText'],
                        'createdAt': item.get('createdAt')
                    })
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(records)
            }
        
        elif method == 'DELETE':
            job_id = event['pathParameters']['id']
            table.delete_item(Key={'jobId': job_id})
            
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
