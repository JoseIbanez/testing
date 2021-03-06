class consul {
    notify { 'hello, consul!': }

    file { '/var/consul':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
    }

    package { 'unzip':
	ensure => 'installed', 
    }


    archive { 'consul_0.9.3_linux_amd64.zip':
        path          => '/tmp/consul_0.9.3_linux_amd64.zip',
        source        => 'https://releases.hashicorp.com/consul/0.9.3/consul_0.9.3_linux_amd64.zip',
        #checksum      => 'f2aaf16f5e421b97513c502c03c117fab6569076',
        #checksum_type => 'sha1',
        extract       => true,
        extract_path  => '/tmp/',
        #creates       => $install_path,
        #cleanup       => 'true',
        cleanup       => 'false',        
        #require       => File[$install_path],
        require        => Package['unzip'],
    }

    file { '/usr/bin/consul':
        ensure    => 'file',
        source    => '/tmp/consul',
    }


}


class consul::server {

    notify { 'hello, consul server!': }

    file { '/etc/consul.d/server':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
        require => File['/etc/consul.d'],
    }

    file { '/etc/consul.d':
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
        source => 'puppet:///modules/consul/server.service',
    }

    service { 'consul':
        ensure => 'running',
        require => [ File['/etc/consul.d/bootstrap/bootstrap.json'],
                     File['/etc/systemd/system/consul.service'],
                     Class['consul'] ],
    }

}

class consul::bootstrap {

    notify { 'hello, consul bootstrap!': }

    file { '/etc/consul.d/bootstrap':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
        require => File['/etc/consul.d'],
    }

    file { '/etc/consul.d':
        ensure => directory,
        mode => '0755',
        owner => 'root',
        group => 'root',
    }


    file { "/etc/consul.d/bootstrap/bootstrap.json":
        mode => "0644",
        owner => 'root',
        group => 'root',
        source => 'puppet:///modules/consul/bootstrap.json',
    }

    file { "/etc/systemd/system/consul.service":
        mode => "0644",
        owner => 'root',
        group => 'root',
        source => 'puppet:///modules/consul/bootstrap.service',
    }

    service { 'consul':
        ensure => 'running',
        require => [ File['/etc/consul.d/bootstrap/bootstrap.json'],
                     File['/etc/systemd/system/consul.service'],
                     Class['consul'] ],
    }


}
