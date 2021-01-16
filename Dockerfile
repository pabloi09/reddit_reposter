FROM python

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg cron nano sqlite3 -y
COPY ./reposter/ /reposter
WORKDIR /reposter

ENV VIRTUAL_ENV=/reposter/venv 
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --upgrade pip
RUN pip install -e .
RUN pip install -r requirements.txt
RUN pip install -U urllib3
RUN crontab -l | { cat; echo "@daily /reposter/venv/bin/python /reposter/batch_processes/daily_scheduler.py >> /reposter/batch.log 2>&1"; } | crontab -
RUN echo "Batch processes log file" >> /reposter/batch.log

CMD /reposter/venv/bin/python /reposter/daemons/insta_daemon.py & cron & service cron force-reload & tail -f /reposter/batch.log
