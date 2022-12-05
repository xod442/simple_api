FROM python:3.8
RUN apt-get update -y
RUN apt-get install -y nano

COPY requirements.txt /opt/
RUN pip3 install -r /opt/requirements.txt

WORKDIR /simple_api
#COPY . .

ENV FLASK_APP=app
ENV FLASK_DEBUG=1
CMD  ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
