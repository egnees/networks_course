FROM python:3.8-slim

RUN apt-get update 
RUN apt-get install -y iputils-ping

COPY mtu.py .

ENTRYPOINT [ "python3", "mtu.py" ]