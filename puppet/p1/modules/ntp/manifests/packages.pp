class ntp::packages {

  notify { 'ntp::packages, hello': }


  # you can use a global package parameter
  Package { ensure => 'installed' }

  package { 'ntp': }
  package { 'screen': }
}
