FROM python:3.10.2-alpine

WORKDIR /app

RUN  \
    apk update && \
    apk upgrade && \
    pip install --upgrade pip

COPY ./requirements.txt .

# install dependencies with additional dependencies for psycopg2
RUN python3 -m pip install -r /app/requirements.txt --no-cache-dir

COPY ./app /app

CMD python3 main.py