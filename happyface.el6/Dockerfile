FROM centos:6.7

## Generating basis
RUN yum --nogpgcheck -y install epel-release
RUN yum --nogpgcheck -y install git unzip wget rpm-build


## Generating UI
RUN yum --nogpgcheck -y install http://download1.rpmfusion.org/free/el/updates/6/x86_64/rpmfusion-free-release-6-1.noarch.rpm
RUN UMD_VERSION=http://repository.egi.eu/sw/production/umd/3/sl6/x86_64/base/umd-release-3.0.0-1.el6.noarch.rpm; yum --nogpgcheck -y install $UMD_VERSION
RUN repofile=http://cvmrepo.web.cern.ch/cvmrepo/yum/cvmfs/EL/6/x86_64/cvmfs-release-2-4.el6.noarch.rpm; yum -y --nogpgcheck install $repofile && yum clean all && yum --nogpgcheck --disablerepo=UMD* --enablerepo=cernvm -y install cvmfs cvmfs-auto-setup cvmfs-init-scripts

#RUN /etc/init.d/autofs restart

## Installing HappyFace
RUN hostname
RUN cd /var/lib && git clone https://github.com/HappyFaceGoettingen/HappyFace-Integration-Server -b MadUpdate
RUN cd /var/lib/HappyFace-Integration-Server && ./nightly-build.sh -r

USER happyface3
ENV HOME /var/lib/HappyFace

