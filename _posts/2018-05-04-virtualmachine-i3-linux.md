---
layout: post
title: "资源占用超级低的linux-自动登陆的i3桌面"
description: ""
category: 
tags: [虚拟机, vmware, i3, linux]
---
{% include JB/setup %}


现在的电脑是Surface，跑虚拟机很吃力了，但是不是不能跑，重点是优化后把linux的资源降下来，还是可以非常流畅。i3是个比xfce4更加轻量级的桌面管理器，而且不是像Windows那样悬浮窗口式的，而是tiling的桌面。随便网上找了个截图，大概就是这个意思：

![i3](https://i3wm.org/screenshots/i3-1.png)

##这边的例子以Vmware为例：

### 1. 首先要安装i3：

```
    $ sudo yum install i3   # centos
    $ sudo apt install i3   # debian & ubuntu
    $ sudo pacman -S i3     # archlinux
```

### 2. 备份并修改i3的配置文件，可以参考我的github，或者直接下载替换：

```
    cp ~/.config/i3/config ~/.config/i3/config.bak
    wget https://raw.githubusercontent.com/gccpacman/vm-i3wm-config/master/config
    cp config ~/.config/i3/config
```


### 3. 因为我的是高分屏，默认vmware不支持，但是可以修改i3的dpi让文字和界面看起来舒服：

```
    echo "Xft.dpi: 118" >> ~/.Xresources
```

### 4. 安装lightdm后，修改`/etc/lightdm/lightdm.conf`，设置session成i3，并且因为是虚拟机不想每次开机都输入用户名密码，可以设置自动登陆：

```
    [SeatDefaults]
    autologin-user= {{your username}}
    autologin-user-timeout=0
    user-session=i3
```


### 5. 根据你的系统安装open-vm-tools:

```    
    $ sudo yum install open-vm-tools   # centos
    $ sudo apt install open-vm-tools   # debian & ubuntu
    $ sudo pacman -S open-vm-tools     # archlinux

```
### 6. 如果你无法加载open-vm-tools, 则需要做如下配置：

```
    cp ~/.xsession ~/.xsession.bak
    echo "#!/bin/sh
    xrandr
    exec i3" > ~/.xsession
```
