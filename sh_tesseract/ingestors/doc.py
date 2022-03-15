
from sh_tesseract.ingestor import Ingestor
from subprocess import  Popen, check_output
import docx2txt
import textract
import logging
logger = logging.getLogger(__name__)


class DocIngestor(Ingestor):

    # LIBRE_OFFICE = r"/usr/local/bin/soffice" MAC
    LIBRE_OFFICE= "/usr/bin/soffice"

    def doc_to_pdf(self, input_doc_path, tmp_dir):
        """
        download libre office https://www.libreoffice.org/download/download/
        """
        p = Popen([self.LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', '--outdir',
            tmp_dir, input_doc_path])
        print([self.LIBRE_OFFICE, '--convert-to', 'pdf', input_doc_path, tmp_dir])
        p.communicate()
    
    def extract_text_docx(self, input_doc_path):
        """
        https://github.com/ankushshah89/python-docx2txt
        apparently this function can take images out of documents too
        """
        text = docx2txt.process(input_doc_path)
        logger.debug(f"Extacted text on {self.file_name}")
        return text
    
    def extract_text_soffice(self, input_doc_path):
        """
        soffice --headless --convert-to txt:Text /path_to/document_to_convert.doc
        """
        command = [self.LIBRE_OFFICE, '--headless', '--convert-to', 'txt:Text', input_doc_path]
        out = check_output(command)
        return out
    
    def extract_text_textract(self, input_doc_path):
        """
        Mac:
        brew install caskroom/cask/brew-cask
        brew cask install xquartz
        brew install poppler antiword unrtf tesseract swig
        pip install textract
        """
        try:
            text = textract.process(str(input_doc_path))
            text = text.decode('utf-8') # utf-8 is default of above, but it is configurable
            return text
        except Exception as e:
            logging.error(f'docx extraction error for {input_doc_path}')
            return None
