# SSHH
SSH utility which provides easy access to your servers using `yaml` configuration file.
Utility support passwordless and passwordl login, logins to certain location and more.

Given configuration file:
```yaml
- server:   myserver.org
  user:     my-username
  tags:     ['work', 'university']
```

You can simple connect to server using tags or any part of the server's name:
```sh
sshh work
sshh uni
sshh myser
```
---

*Note:*

SSHH is useful when combining with `password` field (which points to a file) and **Cerberos** tickets (since you can't use keys), This requires [`sshpass`](https://packages.ubuntu.com/trusty/sshpass) to be installed
