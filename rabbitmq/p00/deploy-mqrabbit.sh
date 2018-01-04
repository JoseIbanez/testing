
echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -


wget "http://packages.erlang-solutions.com/site/esl/esl-erlang/FLAVOUR_1_general/esl-erlang_20.1-1~ubuntu~xenial_amd64.deb"

sudo apt-get -y update

sudo apt-get install -y libwxbase3.0-0v5 libwxgtk3.0-0v5 libsctp1


sudo dpkg -i esl-erlang_20.1-1~ubuntu~xenial_amd64.deb 

sudo apt-get -y install rabbitmq-server


sudo apt-get install python-pip

sudo rabbitmq-plugins enable rabbitmq_management
