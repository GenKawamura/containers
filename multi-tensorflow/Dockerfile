FROM gcr.io/tensorflow/tensorflow:0.8.0

# Replace 500 with your user / group id
RUN export uid=340001 gid=40000 user=tensorflow group=tensorflow && groupadd $group -g $gid && useradd $user -u $uid -g $gid -d /home/$user -s /bin/bash
USER tensorflow
ENV HOME /home/tensorflow
