### html handling

from sh_tesseract.ingestor import Ingestor
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class HtmlIngestor(Ingestor):

    def html_text(self, input_path):
        with open(input_path) as infile:
            raw_text = infile.read()

        soup = BeautifulSoup(raw_text, features="lxml")
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text