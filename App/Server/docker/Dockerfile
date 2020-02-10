FROM fengodchen_seed_image:1.0
MAINTAINER LiaoChen <17211401@bjtu.edu.cn>

# Set Share Python Lib
RUN echo "export PYTHONPATH=/Share/PythonLib" >> /root/.bashrc

# Install Django and Websocket
# RUN pip3 install websockets==8.1 django==3.0.2 --user

# Install Flask and Pyecharts
RUN pip3 install pyecharts==1.6.2 flask==1.1.1

# Set Pyhton import Path
RUN echo 'export PYTHONPATH=${PYTHONPATH}:/Share/App/Socket_Operator' >> /root/.bashrc

# Install and Configure Apache2
RUN apt install apache2 libapache2-mod-wsgi-py3 -y
RUN echo "ServerName localhost:80" >> /etc/apache2/apache2.conf
#RUN echo "service apache2 start" >> /root/.bashrc
RUN echo 'WSGIPythonHome "/usr"' >> /etc/apache2/apache2.conf
RUN echo 'WSGIScriptAlias / /var/www/html/main.wsgi' >> /etc/apache2/apache2.conf



# Install MySQL
#RUN apt install mysql-client mysql-server -y

# Set Share File
RUN mkdir /App
WORKDIR /App