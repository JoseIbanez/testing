node default {
    class { 'helloworld': }
    class { 'helloworld::motd': }
}

node /^u1.\.lxd$/ {
    class { 'helloworld::packages': }
}

class helloworld {
   notify { 'hello, world!': }
}

class helloworld::motd {

   file { '/etc/motd':
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => "hello, world!\n",
    }

}

class helloworld::packages {

  # you can use a global package parameter
  Package { ensure => 'installed' }

  package { 'screen': }
  package { 'nmap': }
  package { 'sudo': }

}
