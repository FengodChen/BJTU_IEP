FROM ubuntu:18.04
MAINTAINER LiaoChen <17211401@bjtu.edu.cn>

# Change apt source
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
ENV DEBIAN_FRONTEND noninteractive

# Update apt
RUN apt update -y

# Set Time Zone
RUN apt install tzdata -y
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Install and Configure Apache2
RUN apt install apache2 php7.2 libapache2-mod-php7.2 -y
RUN echo "ServerName localhost:80" >> /etc/apache2/apache2.conf
RUN echo "service apache2 start" >> /root/.bashrc

# Install MySQL
#RUN apt install mysql-client mysql-server -y

# Set Share File
RUN mkdir /Share
