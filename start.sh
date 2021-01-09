#/bin/bash
sudo docker build -t "reposter" .
sudo docker run -d -v reposter:/reposter --net=host reposter