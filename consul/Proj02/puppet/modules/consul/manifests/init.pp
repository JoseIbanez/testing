class consul {
    notify { 'hello, consul!': }
}


class consul::server {

    notify { 'hello, consul server!': }

    file { '/etc/consul.d/server':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
    }

    file { '/var/consul':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
    }

    file { "/etc/consul.d/server/server.json":
        mode => "0644",
        owner => 'root',
        group => 'root',
        source => 'puppet:///modules/consul/server.json',
    }

    file { "/etc/systemd/system/consul.service":
        mode => "0644",
        owner => 'root',
        group => 'root',
        source => 'puppet:///modules/consul/consul.service',
    }

}