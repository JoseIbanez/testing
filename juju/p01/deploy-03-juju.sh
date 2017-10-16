


add-apt-repository -y --update ppa:juju/stable
apt install -y juju



juju bootstrap localhost lxd-test

juju controllers

juju add-model model1
juju deploy ./model1.yaml

juju add-unit -n5 wordpress

juju deploy memcached
juju add-relation wordpress memcached

juju destroy-model model1


