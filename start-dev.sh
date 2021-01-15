#/bin/bash
./start.sh
docker exec -it reposter_app python batch_processes/daily_scheduler.py
docker exec -it reposter_app tail -f batch.log