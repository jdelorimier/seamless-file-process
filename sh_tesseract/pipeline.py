from more_itertools import bucket
from py import process
from ingestors.pdf import PDFIngestor
from ingestors.doc import DocIngestor
from ingestors.img import ImgIngestor
from ingestor import Ingestor
from pathlib import Path
import tempfile
import boto3
import os
import PIL
from urllib.parse import urlparse

from sh_tesseract.ingestors.img import ImgIngestor
import logging

PROFILE=None
if PROFILE==None:
    session = boto3.session.Session()
else:
    session = boto3.session.Session(profile_name=PROFILE)

def s3_key_gen(bucket_name, prefix='/', delimiter='/', start_after=''):
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    start_after = (start_after or prefix) if prefix.endswith(delimiter) else start_after
    s3_paginator = session.client('s3').get_paginator('list_objects_v2')
    for page in s3_paginator.paginate(Bucket=bucket_name, Prefix=prefix, StartAfter=start_after):
        for content in page.get('Contents', ()):
            full_path = f"s3://{bucket_name}/{content['Key']}"
            yield full_path

def local_key_gen(input_dir):
    for file in Path(input_dir).rglob('*'):
        yield file

def write_text(text, outtxtfile):
    with open(outtxtfile, 'w') as outfile:
        outfile.write(text)

def pipeline(input_dir, output_dir, language=None):
    if input_dir.startswith('s3'):
        s3_parse = urlparse(input_dir)
        prefix = s3_parse.path
        bucket = s3_parse.netloc
        paginator = s3_key_gen(bucket_name = bucket, prefix = prefix)
    else:
        paginator = local_key_gen(input_dir)
    for file in paginator:
        try:
            doc = Ingestor(input_path=file, output_path=None)
            process_path(doc, language=language)
        except Exception as e:
            logging.error(e)


def process_path(doc, language):
    logging.debug(f"processing {doc.input_path}")
    file = doc.input_path
    if doc.extension in [".pdf"]:
        try:
            pdf = PDFIngestor(file)
            pdf.ocr(language=language)
            text = pdf.textract_pdf(pdf.output_path)
        except Exception as e:
            logging.info(f"error ocring {file}")
            logging.error(e)
            raise e
    
    elif doc.extension in [".doc",".docx"]:
        docx = DocIngestor(file)
        text = docx.extract_text_textract(docx.input_path)
    
    elif doc.extension in [".png", ".jpg", ".jpeg", ".tif"]:
        img = ImgIngestor(file)
        
        try:
            with tempfile.TemporaryDirectory() as td:
                temp_output = f"{td}/{img.file_name}.pdf"
                img_to_pdf_output = img.img_to_pdf(
                    input_path=file,
                    output_path=temp_output)
                
                pdf = PDFIngestor(
                input_path=img_to_pdf_output
                )
                pdf.output_path = f"{img.output_path}.pdf"
                pdf.ocr(language=language)
        except Exception as e:
            logging.info(f"error on {file}")
            logging.error(e)
            raise e
        text = pdf.textract_pdf(pdf.output_path)
    
    else:
        logging.error(f"No Extension Found for {file}")
        text = None
    
    # print text
    if text:
        txt_file_path = f"output/txt/{doc.prefix_path}/{doc.file_name}.txt"
        print(txt_file_path)
        if not os.path.exists(f"output/txt/{doc.prefix_path}"):
            os.makedirs(f"output/txt/{doc.prefix_path}")
        with open(txt_file_path, 'w') as outfile:
            outfile.write(text)
        return text


if __name__ == "__main__":
    logging.basicConfig(
        filename='sh-tess.log',
        level=logging.ERROR,
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        filemode = "w+",
    )