FROM python:3.7-alpine

WORKDIR /usr/local/bin
COPY requirements.txt .
COPY main.py .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD ["python3", "main.py"]
