FROM python:alpine

WORKDIR /app
COPY requirements.txt .

RUN apk update \
    && apk upgrade \
    && apk add tzdata \
    && ln -s /usr/share/zoneinfo/Europe/Stockholm /etc/localtime

RUN pip install --upgrade pip \
    && pip install -r requirements.txt
COPY . .

CMD [ "/usr/local/bin/flask", "run", "-h", "0.0.0.0" ]
