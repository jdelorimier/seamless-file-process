FROM python:3.8-slim-buster

# Install poetry
RUN python3 -m pip install -U pip \
 && python3 -c "import urllib.request; print(urllib.request.urlopen('https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py').read().decode('utf-8'))" | python3
ENV PATH="${PATH}:/root/.poetry/bin"

# Install tesseract dependencies
RUN apt-get update && apt-get -y install \
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

# Install language pack
RUN apt-get install tesseract-ocr-rus

# Install textract dependencies
RUN apt-get -y install \
    python-dev \
    libxml2-dev \
    libxslt1-dev \
    antiword \
    unrtf \
    poppler-utils \
    # pstotext \
    tesseract-ocr \
    flac \
    ffmpeg \
    lame \
    libmad0 \
    libsox-fmt-mp3 \
    sox \
    libjpeg-dev \
    swig

# Install libreoffice
RUN apt install libreoffice -y 

WORKDIR /app
ENV PYTHONPATH /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY sh_tesseract sh_tesseract/
ENTRYPOINT ["python","sh_tesseract/main.py"]