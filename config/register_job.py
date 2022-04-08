import boto3
import os
from dotenv import load_dotenv

load_dotenv()
AWS_ACCOUNT_NUMBER = os.getenv('AWS_ACCOUNT_NUMBER')

iam = boto3.client('iam')
client = boto3.client('batch')

ImportRole = iam.get_role(RoleName='batch-ocr-task-role')

response = client.register_job_definition(
    jobDefinitionName='batch-ocr-job',
    type='container',
    containerProperties={
        'image': f'{AWS_ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com/batch-ocr:latest',
        'jobRoleArn': ImportRole['Role']['Arn'],
        'executionRoleArn': ImportRole['Role']['Arn'],
        'environment': [
            {
                'name': 'S3_PATH',
                'value': '',
            },
            {
                'name': 'AWS_DEFAULT_REGION',
                'value': 'use-east-1',
            },
        ],
        'resourceRequirements': [
            {
                'value':"1",
                'type':"VCPU",
            },
            {
                'value':"2048",
                'type':"MEMORY",   
            }
        ],
        'networkConfiguration': {'assignPublicIp': 'ENABLED'},
    },
    platformCapabilities=["FARGATE"],

)

print(response)