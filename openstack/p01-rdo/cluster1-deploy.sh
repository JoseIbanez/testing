




openstack server create \
    --flavor m1.mio \
    --image "Ubuntu 16.04" \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    d1

openstack server create \
    --flavor m1.mio \
    --image "Ubuntu 16.04" \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    d2

openstack server create \
    --flavor m1.mio \
    --image "Ubuntu 16.04" \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    d3

openstack server create \
    --flavor m1.mio \
    --image "Ubuntu 16.04" \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    d4



openstack floating ip list

openstack server add floating ip d2  192.168.1.202
