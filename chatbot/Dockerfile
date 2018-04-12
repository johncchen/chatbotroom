FROM centos:7

MAINTAINER NUWA Inc. <chen.john@nuwarobotics.com>

RUN yum -y update && \
    yum -y install epel-release && \
    yum -y install python34 python34-setuptools iputils && \ 
    easy_install-3.4 pip

COPY . /opt/chatbotroom

WORKDIR /opt/chatbotroom

EXPOSE 80

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/bin/sh","-c","/usr/bin/python3 manage.py runserver 0.0.0.0:80"]
#CMD ["/bin/bash", "ping localhost"]
