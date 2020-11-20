FROM python:3.8

EXPOSE 5000

WORKDIR /webservice

COPY requirements.txt .

COPY webservice .

RUN pip install -r requirements.txt

CMD [ "python", "./server.py" ]