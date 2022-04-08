from distutils.sysconfig import PREFIX
from urllib import response
import boto3
import itertools
import os
from dotenv import load_dotenv

load_dotenv()
AWS_ACCOUNT_NUMBER = os.getenv('AWS_ACCOUNT_NUMBER')
BUCKET_TARGET = os.getenv('BUCKET_TARGET')
PREFIX_TARGET = os.getenv('PREFIX_TARGET')


client = boto3.client('batch')

def submit_job(job_name, s3_path):
    response = client.submit_job(
        jobDefinition='batch-ocr-job',
        jobName=job_name,
        jobQueue='batch-ocr-queue',
        containerOverrides={
            'environment': [
                {
                    'name': 'S3_PATH',
                    'value': s3_path,
                },
                {
                    'name':'AWS_DEFAULT_REGION',
                    'value':'us-east-1'
                }
            
            ]
        },
    )

    return response

if __name__ == "__main__":

    COUNT = 100

    s3 = boto3.resource('s3')
    bucket_name = BUCKET_TARGET
    my_bucket = s3.Bucket(bucket_name)
    file_gen = my_bucket.objects.filter(Prefix=f"{PREFIX_TARGET}/")
    i = 1
    for object_summary in file_gen:
        key = object_summary.key
        s3_path = f"s3://{bucket_name}/{key}"
        print(s3_path)
        response = submit_job(job_name=f"full{i}", s3_path = s3_path)
        print(response)
        i +=1
