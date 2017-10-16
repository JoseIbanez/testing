
openstack flavor list

openstack image list

openstack network list

openstack security group list

openstack keypair list


openstack server create \
    --flavor m1.tiny \
    --image CirrOS \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    cirros2

openstack server list


openstack server create \
    --flavor m1.mio \
    --image "Ubuntu 14.04" \
    --nic net-id=private1 \
    --security-group d0d95fd0-c2c5-408a-8c48-873a51712bf1 \
    --key-name openstack \
    u2

openstack server list


openstack console log show u2 


