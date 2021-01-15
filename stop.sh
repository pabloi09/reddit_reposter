#bin/bash
docker exec -it reposter_app sqlite3 db.db "update post set closed=1;"
docker cp reposter_app:/reposter/db.db ./reposter/
docker cp reposter_app:/reposter/reposter.key ./reposter/
docker rm -f reposter_app
docker system prune -f
docker volume prune -f