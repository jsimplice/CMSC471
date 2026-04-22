import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')

JOB_STATE_TABLE = os.environ.get('JOB_STATE_TABLE')
table = dynamodb.Table(JOB_STATE_TABLE)

# Aurora connection would go here (not implemented in this stub)
# rds = boto3.client('rds')

def lambda_handler(event, context):
    """
    Step Functions Step 3: Save results to DynamoDB and Aurora
    """
    try:
        job_id = event['jobId']
        extracted_text = event['extractedText']
        
        # Save to DynamoDB
        table.update_item(
            Key={'jobId': job_id},
            UpdateExpression='SET #status = :status, extractedText = :text, completedAt = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'SUCCEEDED',
                ':text': extracted_text,
                ':ts': datetime.utcnow().isoformat()
            }
        )
        
        # TODO: Save to Aurora RDS
        # This would require database connection setup
        
        return {
            'jobId': job_id,
            'status': 'SUCCEEDED',
            'extractedText': extracted_text
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
