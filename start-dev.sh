#/bin/bash
./start.sh
docker exec -it reposter_app batch_processes/daily_scheduler.py