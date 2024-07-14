FROM amazonlinux:latest
RUN yum update -y
RUN yum install -y \
    python3 \
    python3-pip \
    zip
RUN yum -y clean all
RUN python3 -m pip install --upgrade --ignore-installed pip