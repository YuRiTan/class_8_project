docker build -t capstone .
if [ `docker ps | grep capstone | wc -l` -gt 0 ]; then docker stop capstone && docker container rm capstone; fi
docker run --rm -p 5555:5555 --name capstone -d capstone:latest
