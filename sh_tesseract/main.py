#### RUN BATCH

import boto3
import os
import tempfile
from urllib.parse import urlparse
import smart_open
from sh_tesseract.ingestor import Ingestor
from sh_tesseract.pipeline import process_path
import pathlib

def parse_s3_path(s3_path):
    parse = urlparse(s3_path, allow_fragments=False)
    bucket = parse.netloc
    key = parse.path.strip('/')
    return bucket, key

def download_file(s3_path, local_file_path):
    s3 = boto3.client('s3')
    bucket, key = parse_s3_path(s3_path)
    pathlib.Path(local_file_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        s3.download_file(bucket,key,local_file_path)
        return {
            "msg":"Success",
            "loc":local_file_path,
            "origin":f"{s3_path}"
        }
    except Exception as e:
        return {
            "msg":"Error",
            "error": str(e)
        }

def upload(local_path, s3_path):
    s3 = boto3.resource('s3')
    bucket, key = parse_s3_path(s3_path)
    try:
        s3.Bucket(bucket).upload_file(local_path,key)
        return {
            "msg":"Successful local file upload",
            "loc":s3_path,
            "origin":local_path
        }
    
    except Exception as e:
        return {
            "msg":f"Errorfile on file upload from {local_path}",
            "error": str(e)
        }

def stream_text(s3_path, text):
    session = boto3.Session()
    try:
        with smart_open.open(s3_path, 'w', transport_params={'client': session.client('s3')}) as outfile:
            outfile.write(text)
        return {
            "msg":"Successful text stream",
            "loc":s3_path,
        }
    except Exception as e:
        return {
            "msg":f"Error on text stream to {s3_path}",
            "error": str(e)
        }

def main():
    if os.environ.get('S3_PATH'):
        s3_path = os.environ['S3_PATH']
        TEST = False
    else:
        TEST = True
    with tempfile.TemporaryDirectory() as tmpdir:
        bucket, key = parse_s3_path(s3_path)
        local_file_path = f"{tmpdir}/{key}"
        processed_file_path=f"{tmpdir}/ocr/{key}"
        doc = Ingestor(local_file_path, output_path=processed_file_path)
        download = download_file(s3_path=s3_path, local_file_path = local_file_path)
        print(download)
        if download.get('loc'):
            loc = download.get('loc')
            text, output_path = process_path(doc, language = "rus")

            if text:
                s3_txt=f"s3://{bucket}/txt/{key}.txt"
                text_status = stream_text(s3_txt, text)
                print(text_status)
            
            print(output_path)
            if os.path.exists(output_path):
                filename, file_extension = os.path.splitext(output_path)
                keyname, key_extension = os.path.splitext(key)
                if file_extension == key_extension:
                    s3_proccessed_path=f"s3://{bucket}/ocr/{key}"
                else:
                    s3_proccessed_path=f"s3://{bucket}/ocr/{key}{file_extension}"

                upload_status = upload(local_path=output_path, s3_path=s3_proccessed_path)
                print(upload_status)
            


if __name__ == "__main__":
    main()


