node /^u10\.lxd$/ {
    class { 'consul::server': }
}


class helloworld {
   notify { 'hello, world!': }
}
