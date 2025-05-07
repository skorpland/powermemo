FROM python:3.11-slim-buster AS build


WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN python3.11 -m pip install -r requirements.txt --no-cache-dir

COPY ./powermemo_server /app/powermemo_server
COPY ./api.py /app
COPY ./api_docs.py /app


CMD ["python3.11", "-m", "fastapi", "run", "api.py"]
