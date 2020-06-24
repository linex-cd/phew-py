FROM ubuntu_textise:v2.1

ADD src /worker_service
WORKDIR /worker_service

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod +x /worker_service/startworker.sh

