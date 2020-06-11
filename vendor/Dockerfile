FROM ubuntu_textise:v2.1

ADD src /vendor_service
WORKDIR /vendor_service

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

RUN chmod +x /vendor_service/startvendor.sh

