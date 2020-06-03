
ARG version

FROM jobcenter_image:${version}

ADD ../src /jobcenter
WORKDIR /jobcenter

RUN chmod +x /jobcenter/startjobcenter.sh

