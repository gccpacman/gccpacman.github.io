---
title: 用Calibre Server创建个人在线电子书阅读网站 
date: 2017-12-20
---



DigitalOcean上有在ubuntu 14.04上安装calibre server的教程, 但是已经过时了。[How To Create a Calibre Ebook Server on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-create-a-calibre-ebook-server-on-ubuntu-14-04)，一是calibre-server的参数已经改变，而且创建系统服务的方式已经不适用之后的Ubuntu版本，我的服务器是16.04，因此需要把/etc/init/里的脚本改写成systemctl脚本

改写的方法参考了：https://wiki.ubuntu.com/SystemdForUpstartUsers

用户名和密码也不再支持digitalocean里的明文的形式, [官方文档](https://manual.calibre-ebook.com/server.html#managing-user-accounts-from-the-command-line-only)里看到有`enable-auth`和`userdb`, 看来是出于安全性进行了改进, userdb指定最简单的sqlite数据库，并按照提示添加用户。
最终的版本是：
```
  [Unit]
  Description=Job that runs the calibre daemon

  [Service]
  Environment=LIBRARY_PATH=/home/huyunyan_cn/calibre-library
  Environment=PORT=8080
  Environment=USERDB=/home/huyunyan_cn/calibre-library/users.sqlite
  ExecStart=/usr/bin/calibre-server $LIBRARY_PATH \
                                   --port $PORT --enable-auth --userdb $USERDB
  [Install]
  WantedBy=multi-user.target
```

用户名和密码需要通过另一个参数`--manage-users`启动server后手动配置：

`sudo  calibre-server /home/huyunyan_cn/calibre-library/ --port 8080 --manage-users --userdb /home/huyunyan_cn/calibre-library/users.sqlite`

这样就完成了，访问域名后会提示输入用户名和密码，这样你自己可以在任何设备上访问，又不用担心别人来访问你的电子书。

TODO:
1. 自动刷新书库（--auto-reload这个参数已经不能用，需要通过restart service来实现）
2. 远程同步书籍，可以从本地直接上传书到server



