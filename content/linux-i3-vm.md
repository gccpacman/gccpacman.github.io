Title: 资源占用超级低的i3桌面
Date: 2018-05-04 10:20
Modified: 2018-05-04 19:30
Category: Vim
Tags: linux, vim, gtk, vitual machine
Authors: r341h

现在的电脑是Surface，跑虚拟机很吃力了，但是不是不能跑，重点是优化后把linux的资源降下来，还是可以非常流畅。i3是个比xfce4更加轻量级的桌面管理器，而且不是像Windows那样悬浮窗口式的，而是tiling的桌面。随便网上找了个截图，大概就是这个意思：

![i3](https://i3wm.org/screenshots/i3-1.png)

这边的例子以Vmware为例：


1. 首先要安装i3：
```
    $ sudo yum install i3   # centos
    $ sudo apt install i3   # debian & ubuntu
    $ sudo pacman -S i3     # archlinux
```
2. 备份并修改i3的配置文件，可以参考我的github，或者直接下载替换：
```
    cp ~/.config/i3/config ~/.config/i3/config.bak
    wget https://raw.githubusercontent.com/gccpacman/vm-i3wm-config/master/config
    cp config ~/.config/i3/config
```
3. 因为我的是高分屏，默认vmware不支持，但是可以修改i3的dpi让文字和界面看起来舒服：
```
    echo "Xft.dpi: 118" >> ~/.Xresources
```
4. 安装lightdm/gdm后，，设置session成i3，并且因为是虚拟机不想每次开机都输入用户名密码，可以设置自动登陆：

    4.1 `lightdm`修改`/etc/lightdm/lightdm.conf`:
    ```
        [SeatDefaults]
        autologin-user= {{your username}}
        autologin-user-timeout=0
        user-session=i3
    ```
    4.2 `gdm`修改`/etc/gdm3/daemon.conf`:
    ```
        [daemon]
        AutomaticLoginEnable=true
        AutomaticLogin=teotfw
    ```
    4.3 或者直接disable x-manager, 用startx方式启动
    ```
        sudo systemctl set-default multi-user.target
        echo "exec i3" > ~/.xinitrc
        startx # reboot并login后执行
    ```

5. 根据你的系统安装open-vm-tools
```
    $ sudo yum install open-vm-tools   # centos
    $ sudo apt install open-vm-tools   # debian & ubuntu
    $ sudo pacman -S open-vm-tools     # archlinux
```
6. 如果你无法加载open-vm-tools, 则需要做如下配置：
```
    cp ~/.xsession ~/.xsession.bak
    echo "#!/bin/sh
    xrandr
    exec i3" > ~/.xsession
```