docker network create grid

docker run -d -p 4442-4444:4442-4444 --net grid --name selenium-hub selenium/hub:latest

docker run -d --net grid -e SE_EVENT_BUS_HOST=selenium-hub \
 --shm-size="2g" \
 -e SE_EVENT_BUS_PUBLISH_PORT=4442 \
 -e SE_EVENT_BUS_SUBSCRIBE_PORT=4443 \
 selenium/node-chrome:latest
