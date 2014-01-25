base:
  '*':
    - server

  'u4':
    - match: list
    - users

  '* not G@roles:ntp-master':
    - match: compound
    - ntp

  'roles:ntp-master':
    - match: grain
    - ntp-master

  'G@roles:dns-priv and G@roles:dns-slave':
    - match: compound
    - dns-priv

  g_mta:
    - match: nodegroup
    - mta
 