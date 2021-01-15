#/bin/bash
./start.sh
sleep 10
docker exec -it reposter_app batch_processes/daily_scheduler.py
docker exec -it reposter_app tail -f batch.log