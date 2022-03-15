
# we get an infile an input: a path
# A file has certain attributes
import os
from pathlib import Path
import logging
import boto3
from  urllib.parse import urlparse

logger = logging.getLogger(__name__)

PROFILE=None
if PROFILE==None:
    session = boto3.session.Session()
else:
    session = boto3.session.Session(profile_name=PROFILE)

class Ingestor(object):

    def __init__(self, input_path, output_path=None):
        '''
        Example: /a/path/to/file.pdf
        '''
        # self.input_path = self.process_s3(input_path=input_path)
        self.input_path = input_path
        self.extension = self.get_extenstion(self.input_path) # .pdf
        self.stem = self.get_stem(self.input_path) # file
        self.prefix_path = self.get_prefix(self.input_path)[0] # a/path/to
        self.file_name = self.get_prefix(self.input_path)[1] # file.pdf
        self.output_path = self.get_output_path(output_path)

    def get_extenstion(self, input_path):
        ext = os.path.splitext(input_path)[1]
        ext = ext.lower()
        return ext

    def get_stem(self, input_path):
        stem = Path(input_path).stem
        stem = stem.lower()
        return stem
    
    def get_prefix(self, input_path):
        prefix_path, file_name =  os.path.split(input_path)
        prefix_path = prefix_path
        return prefix_path, file_name
    
    def get_output_path(self, output_path):
        if output_path:
            output_prefix = self.get_filepath(output_path)[1]
            output_path = output_path
        else:
            output_prefix=f"output/files/{self.prefix_path}"
            output_path = f"output/files/{self.input_path}"
        
        if not os.path.exists(output_prefix):
            os.makedirs(output_prefix)

        return output_path
    
    def process_s3(self, input_path):
        if input_path.startswith('s3'):
            s3_parse = urlparse(input_path, allow_fragments=False)
            bucket = s3_parse.netloc
            file_path = s3_parse.path.strip('/')
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            output_path = file_path
            try:
                session.client('s3').download_file(bucket, file_path, output_path)
            except Exception as e:
                logging.error(f's3 download error on {input_path}')
                logging.error(e)

            return output_path
        
        else:
            return input_path