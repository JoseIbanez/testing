FROM ubuntu:13.10
MAINTAINER Jose Ibanez <jose.ibanez@fibratel.com>
ADD ./88apt-proxy /etc/apt/apt.conf.d/88apt-proxy
RUN apt-get update 
RUN apt-get -y upgrade
RUN DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install mysql-client mysql-server apache2 libapache2-mod-php5 php5-gd php5-ldap pwgen python-setuptools vim-tiny php5-mysql 
RUN apt-get -y install openssh-server sudo php5-json 
RUN easy_install supervisor
ADD ./start.sh /start.sh
ADD ./foreground.sh /etc/apache2/foreground.sh
ADD ./supervisord.conf /etc/supervisord.conf
RUN echo %sudo	ALL=NOPASSWD: ALL >> /etc/sudoers
#RUN rm -rf /var/www/
#ADD http://www.limesurvey.org/en/stable-release/finish/25-latest-stable-release/1078-limesurvey205plus-build140302-tar-gz /lime.tar.gz
ADD http://192.168.1.104/1078-limesurvey205plus-build140302-tar-gz /lime.tar.gz
RUN tar xvz -f /lime.tar.gz 
RUN mv /limesurvey/ /var/www/ls/
RUN chmod 777 -R /var/www/ls/tmp/
RUN chmod 777 -R /var/www/ls/upload/
RUN chmod 777 -R /var/www/ls/application/config/
RUN chmod 755 /start.sh
RUN chmod 755 /etc/apache2/foreground.sh
RUN mkdir /var/log/supervisor/
EXPOSE 80
EXPOSE 22
CMD ["/bin/bash", "/start.sh"]
