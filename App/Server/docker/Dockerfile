FROM ubuntu:18.04
MAINTAINER LiaoChen <17211401@bjtu.edu.cn>

# Change apt source
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean

# Install and Configure Apache2
RUN apt update -y \
	&& apt install apache2 -y
RUN echo "ServerName localhost:80" >> /etc/apache2/apache2.conf
RUN echo "service apache2 start" >> /root/.bashrc
RUN mkdir /Share

#RUN service apache2 start