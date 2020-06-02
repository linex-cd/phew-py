FROM ubuntu_textise:v3.0

ADD service /jobcenter
WORKDIR /jobcenter

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod +x /jobcenter/startjobcenter.sh

