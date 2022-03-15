#!/bin/bash

# Install Poetry
# python3 -c "import urllib.request; print(urllib.request.urlopen('https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py').read().decode('utf-8'))" | python3
# PATH="${PATH}:$HOME/.poetry/bin"

# Install tesseract
sudo apt-get -y install \
    ghostscript \
    icc-profiles-free \
    libxml2 \
    pngquant \
    python3-distutils \
    python3-pkg-resources \
    python3-reportlab \
    qpdf \
    tesseract-ocr \
    zlib1g \
    unpaper

# languages
sudo apt-get install install tesseract-ocr-rus \
    tesseract-ocr-bel

# Textract
sudo apt-get -y install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr \
flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig

# libre office
sudo apt install libreoffice -y 



