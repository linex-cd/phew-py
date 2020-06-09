FROM ubuntu_textise:v2.1

ADD src /textise_service
WORKDIR /textise_service

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod +x /textise_service/startworker.sh

