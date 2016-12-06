node default {

file { '/root/example_file.txt':
    ensure => "file",
    owner  => "root",
    group  => "root",
    mode   => "700",
    content => "Congratulations!
Puppet has created this file.
",}

augeas { "eth0":
    context => "/files/etc/sysconfig/network-scripts/ifcfg-eth0",
    changes => [
        "set DEVICE eth0",
        "set BOOTPROTO none",
        "set HOSTNAME tropo01",
        "set ONBOOT yes",
        "set NETMASK 255.255.255.0",
        "set IPADDR 10.12.0.10",
        "rm DHCP_HOSTNAME",
    ],
    require => Augeas['hostname'],
    notify => Service['network']
}

augeas { "hostname":
    context => "/files/etc/sysconfig/network",
    changes => [
        "set HOSTNAME tropo01",
    ],
}

service { "network":
  ensure    => running,
  enable    => true
}

}
