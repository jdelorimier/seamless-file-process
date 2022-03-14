### image handling

from sh_tesseract.ingestor import Ingestor
from io import BytesIO
import img2pdf
import tempfile
import logging

logger = logging.getLogger(__name__)

class ImgIngestor(Ingestor):

    def img_to_pdf(self, input_path, output_path):
        input_path = str(input_path)
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(input_path))
        logger.info(f"converted {self.file_name} to pdf")
        return output_path
    
    def img_to_binary(self, input_path):
        with open(input_path, 'rb') as infile:
            img = img2pdf.convert(infile)
            # bytes_reader = BytesIO(img)
        return img
    
    