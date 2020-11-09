FROM ubuntu_textise:v2.1

ADD service /textise_web
WORKDIR /textise_web

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod +x /textise_web/startweb.sh

