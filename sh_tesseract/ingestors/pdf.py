from sh_tesseract.ingestor import Ingestor
import ocrmypdf
import logging
import textract

logger = logging.getLogger(__name__)

class PDFIngestor(Ingestor):

    def ocr(self, language=None):
        """
        run pdf ocr and deposit in outpath
        """
        result = self.pdf_process(
                input_path=self.input_path,
                output_path=self.output_path,
                language=language,
                )
        if result == ocrmypdf.ExitCode.already_done_ocr:
            logger.debug("Skipped document because it already contained text")
        elif result == ocrmypdf.ExitCode.ok:
            logger.debug("OCR complete")
        logging.info(result)

    def pdf_process(self, input_path, output_path, language=None):

        # ocrmypdf.configure_logging(ocrmypdf.Verbosity.default)
        try:
            result = ocrmypdf.ocr(input_file=input_path,
                output_file=output_path,
                language=language,
                tesseract_timeout=120,
                rotate_pages=True,
                skip_text=True,
                progress_bar=False,
                deskew=True)
        except ocrmypdf.exceptions.EncryptedPdfError:
            logging.error('encryption error')
            return None
            

        return result

    def textract_pdf(self, input_path):    
        text = textract.process(input_path)
        text = text.decode('utf-8')
        return text


