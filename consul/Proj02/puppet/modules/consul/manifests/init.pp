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
        source => 'puppet:///modules/consul/server.service',
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
    }

    exec { 'consul bin':
        command   => "cp /tmp/consul /usr/bin/consul",
        path      => $::path,
        subscribe => Archive['consul_0.9.3_linux_amd64.zip'],
    }

}