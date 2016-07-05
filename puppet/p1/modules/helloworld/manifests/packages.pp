class helloworld::packages {

  # you can use a global package parameter
  Package { ensure => 'installed' }

  package { 'screen': }
  package { 'nmap': }
  package { 'sudo': }

}
