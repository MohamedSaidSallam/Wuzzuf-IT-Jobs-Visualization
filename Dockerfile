FROM python:3.9.0-alpine3.12

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev libxml2-dev && \
    apk add --no-cache libxslt
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps

COPY . .

CMD [ "python", "-m", "Wuzzuf_DataCollection" ]