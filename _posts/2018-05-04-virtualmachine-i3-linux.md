现在的电脑是Surface，跑虚拟机很吃力了，但是不是不能跑，重点是优化后把linux的资源降下来，还是可以非常流畅。i3是个比xfce4更加轻量级的桌面管理器，而且不是像Windows那样悬浮窗口式的，而是tiling的桌面。随便网上找了个截图如下：

![i3](https://i3wm.org/screenshots/i3-1.png)

vmware, virtualbox都可以，不过这边的例子以Vmware为例：

首先要安装i3：

    $ sudo yum install i3   # centos
    $ sudo apt install i3   # debian & ubuntu
    $ sudo pacman -S i3     # archlinux

备份并修改i3的配置文件：

    cp ~/.config/i3/config ~/.config/i3/config.bak
    cp config ~/.config/i3/

因为我的是高分屏，默认vmware不支持，但是可以修改i3的dpi让文字和界面看起来舒服：

    echo "Xft.dpi: 118" >> ~/.Xresources

安装lightdm后，设置session成i3，并且因为是虚拟机不想每次开机都输入用户名密码，可以设置自动登陆：

    [SeatDefaults]
    autologin-user= {{your username}}
    autologin-user-timeout=0
    user-session=i3
