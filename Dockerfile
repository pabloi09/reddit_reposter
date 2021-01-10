FROM python

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install ffmpeg cron nano -y
COPY ./reposter/ /reposter
WORKDIR /reposter
ENV VIRTUAL_ENV=/reposter/venv 
RUN python -m venv $VIRTUAL_ENV
RUN PATH="$VIRTUAL_ENV/bin:$PATH"
RUN . /venv/bin/activate
RUN pip install -e .
RUN pip install -r requirements.txt
RUN echo "Batch processes log file" >> /reposter/batch.log

CMD python /reposter/batch_processes/daily_scheduler.py & cron &  service cron force-reload & tail -f /reposter/batch.log
