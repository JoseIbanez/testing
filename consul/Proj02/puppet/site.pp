node /^u10\.lxd$/ {
    class { 'consul': }
    class { 'consul::bootstrap': }
}


class helloworld {
   notify { 'hello, world!': }
}
