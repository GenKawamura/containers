FROM ubuntu:14.04

RUN apt-get update && apt-get install -y firefox Xvfb xdotool
# firefox.el6/firefox-38.6.1-1.el6_7.x86_64.rpm

# Replace 1000 with your user / group id
RUN export uid=1000 gid=1000 && \
    mkdir -p /home/madface && \
    echo "madface:x:${uid}:${gid}:MadFace,,,:/home/madface:/bin/bash" >> /etc/passwd && \
    echo "madface:x:${uid}:" >> /etc/group && \
    echo "madface ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/madface && \
    chmod 0440 /etc/sudoers.d/madface && \
    chown ${uid}:${gid} -R /home/madface

USER madface
ENV HOME /home/madface

