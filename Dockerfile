FROM python:3.7-alpine

ENV PG_HOST '192.168.86.89'
ENV PG_DB 'airquality'
ENV PG_PORT '5432'
ENV PG_USER 'postgres'
ENV PG_PASS 'postgres'
ENV USB_DEVICE '/dev/ttyUSB0'
ENV USE_HUE 'False'

WORKDIR /usr/local/bin
COPY requirements.txt .
COPY main.py .

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

CMD ["python3", "main.py"]
