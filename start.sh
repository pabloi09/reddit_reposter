#/bin/bash
docker build -t "reposter" .
docker run -d -v reposter:/reposter --net=host --name=reposter_app reposter 