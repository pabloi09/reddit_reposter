FROM python

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg cron -y
COPY ./reposter/ /reposter
WORKDIR /reposter
RUN pip install -e .
RUN pip install -r requirements.txt
RUN crontab -l | { cat; echo "@daily python /reposter/batch_processes/daily_scheduler.py >> /reposter/batch.log"; } | crontab -


CMD touch /reposter/batch.log & cron & tail -f /reposter/batch.log
