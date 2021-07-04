FROM python:3.8.3-alpine

WORKDIR /app
ADD ./nflrushing/requirements.txt /app/nflrushing/


RUN pip install --upgrade pip
RUN pip install gunicorn
RUN pip install -r nflrushing/requirements.txt

ADD ./docker /app/docker
ADD ./nflrushing /app/nflrushing