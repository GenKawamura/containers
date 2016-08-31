FROM centos:6.7

RUN yum --nogpgcheck -y install Xvfb xclock ImageMagick

# Replace 374 with your user / group id
RUN export uid=374 gid=374 && groupadd madface -g $gid && useradd madface -u $uid -g $gid

USER madface
ENV HOME /home/madface

