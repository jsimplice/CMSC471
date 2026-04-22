import json
import boto3
import os
import uuid

stepfunctions = boto3.client('stepfunctions')

STATE_MACHINE_ARN = os.environ.get('STATE_MACHINE_ARN')

def lambda_handler(event, context):
    """
    POST /api/jobs - Start a new transcription job
    """
    try:
        body = json.loads(event.get('body', '{}'))
        image_key = body.get('imageKey')
        
        if not image_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'imageKey is required'})
            }
        
        job_id = str(uuid.uuid4())
        
        # Start Step Functions execution
        response = stepfunctions.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            name=job_id,
            input=json.dumps({
                'jobId': job_id,
                'imageKey': image_key
            })
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'jobId': job_id,
                'executionArn': response['executionArn']
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
