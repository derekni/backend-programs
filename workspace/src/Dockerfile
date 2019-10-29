FROM python:3.7

RUN MKDIR /usr/app/src
WORKDIR /usr/app/src

COPY . .

RUN pip install -r requirements.txt

CMD python app.py