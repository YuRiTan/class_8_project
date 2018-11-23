docker build -t capstone
if [ `docker ps | grep capstone | wc -l` -gt 0 ]; then docker stop capstone; fi
docker run capstone -p 5555:5555 --name capstone -d
