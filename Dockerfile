FROM python

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg cron -y
COPY ./reposter/ /reposter
WORKDIR /reposter
RUN pip install -e .
RUN pip install -r requirements.txt
RUN crontab -l | { cat; echo "@daily python /reposter/batch_processes/daily_scheduler.py >> /reposter/batch.log 2>&1"; } | crontab -
RUN echo "Batch processes log file" >> /reposter/batch.log

CMD cron &  service cron force-reload & tail -f /reposter/batch.log
