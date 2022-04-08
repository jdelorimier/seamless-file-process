#!/bin/bash

source .env

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com
docker build -t batch-ocr .
docker tag batch-ocr:latest $AWS_ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/batch-ocr:latest
docker push $AWS_ACCOUNT_NUMBER.dkr.ecr.us-east-1.amazonaws.com/batch-ocr:latest