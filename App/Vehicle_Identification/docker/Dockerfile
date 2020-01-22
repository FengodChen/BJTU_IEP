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

# Install Python3 and Pip3
RUN apt install python3 python3-pip libsm6 libxrender-dev libxext-dev -y

RUN mkdir ~/.pip
RUN echo "[global]" >> ~/.pip/pip.conf
RUN echo "index-url = http://mirrors.aliyun.com/pypi/simple/" >> ~/.pip/pip.conf
RUN echo "trusted-host = mirrors.aliyun.com" >> ~/.pip/pip.conf

RUN pip3 install opencv-python==4.1.2.30 --user

# Set Time Zone
RUN apt install tzdata -y
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata

# Install SQLite
RUN apt install sqlite libsqlite3-dev -y

# Set Share File
RUN mkdir /Share
RUN mkdir /YOLOv3

WORKDIR /YOLOv3
