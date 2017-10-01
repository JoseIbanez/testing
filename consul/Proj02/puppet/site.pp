node /^u1.\.lxd$/ {
    class { 'helloworld': }
    class { 'consul': }
}


class helloworld {
   notify { 'hello, world!': }
}
