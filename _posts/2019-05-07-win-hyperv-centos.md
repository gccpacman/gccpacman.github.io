---
title: Windows在Hyperv安装Centos7并配置网络
date: 2019-05-07 11:13:00 
categories: Windows
tags: [windows, hyper-v, centos, vitual machine]
---
Hyper-V安装Centos，网卡选择Hyper-V的Default Switch。
Default Switch默认是可以连接外网的，如果是windows机器不用配置直接可以联网，但是Linux不行，原因是网卡eth0默认没有配置dhcp：

可以通过以下几部配置：

1. 编辑`/etc/sysconfig/network-scripts/ifcfg-eth0`,修改以下三项:

        DEVICE=eth0
        BOOTPROTO=dhcp
        ONBOOT=yes

2. 编辑`/etc/sysconfig/network`, 替换server-name.company.lan为你的主机名：

        NETWORKING=yes
        HOSTNAME=server-name.company.lan

3. 重启network服务：

        $ systemctl restart network

4. 确认网络是否网络正常，正常的话重启，再次确认：

        $ nslookup bing.com


参考：
https://unix.stackexchange.com/questions/17436/centos-on-hyperv-eth0-not-in-ifconfig

https://www.krizna.com/centos/setup-network-centos-7/