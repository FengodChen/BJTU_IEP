FROM fengodchen_seed_image:1.0
MAINTAINER LiaoChen <17211401@bjtu.edu.cn>

# Install and Configure Apache2
RUN apt install apache2 php7.2 libapache2-mod-php7.2 -y
RUN echo "ServerName localhost:80" >> /etc/apache2/apache2.conf
RUN echo "service apache2 start" >> /root/.bashrc

# Set Pyhton import Path
RUN echo "export PYTHONPATH=/App/Data_Operator" >> /root/.bashrc
RUN echo "export PYTHONPATH=${PYTHONPATH}:/Share/App/Socket_Operator" >> /root/.bashrc

# Install MySQL
#RUN apt install mysql-client mysql-server -y

# Set Share File
RUN mkdir /App
WORKDIR /App