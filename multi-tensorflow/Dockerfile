FROM gcr.io/tensorflow/tensorflow:0.8.0

# Replace 500 with your user / group id
#RUN export uid=340001 gid=40000 user=tensorflow group=tensorflow && groupadd $group -g $gid && useradd $user -u $uid -g $gid -d /home/$user -s /bin/bash
RUN export uid=500 gid=500 user=tensorflow group=tensorflow && groupadd $group -g $gid && useradd $user -u $uid -g $gid -d /home/$user -s /bin/bash
USER tensorflow
ENV HOME /home/tensorflow


RUN cp /usr/local/lib/python2.7/dist-packages/tensorflow/models/image/cifar10/cifar10_train.py /tmp/cifar10_download.py && sed -e "s/^  train()//g" -i /tmp/cifar10_download.py
RUN /usr/bin/python /tmp/cifar10_download.py
