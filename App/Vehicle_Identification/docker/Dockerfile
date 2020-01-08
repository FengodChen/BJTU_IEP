FROM ubuntu:18.04
MAINTAINER LiaoChen <17211401@bjtu.edu.cn>

# Change apt source
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get clean
ENV DEBIAN_FRONTEND noninteractive

# Update apt
RUN apt update -y

# Install GCC and Make
RUN apt install gcc g++ make -y

# Set Time Zone
RUN apt install tzdata -y
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Install SQLite
RUN apt install sqlite -y

# Set Share File
RUN mkdir /Share
RUN mkdir /YOLOv3

WORKDIR /YOLOv3
