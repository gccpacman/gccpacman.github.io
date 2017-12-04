---
title: Surface Pro 3 安装Linux休眠唤醒后wifi和蓝牙无法正常使用的解决方法
date: 2017-12-04
---

`Manjaro Linux`从`17.02`版本开始匹配了Surface Pro 3， 这里必须非常感谢下Manjaro Team的工作，我现在可以再次在Surface上用畅快的用Linux了。

具体可以看reddit上的这篇文章： https://cd-rw.org/t/running-linux-on-the-surface-pro-3/175/37。

我实际安装的版本是`17.1pre3`，不管是蓝牙，触摸板，WIFI，touchpad，音量键，甚至触摸屏都可以正常使用，甚至都不用升级内核。

唯一的问题是启用休眠以后，wifi和蓝牙功能失灵了，即使通过重启`NetworkManager.service`也无法解决，因此基本上就是硬件驱动的问题，网上关于其他一些笔记本在休眠后无法解决的问题基本上就是用lsmod查到和wifi相关的模块，然后重新加载的方法，但是没有和surface pro有关的内容。

找了几篇stackoverflow文章做了多次尝试，然后通过`lsmod　| grep wifi`和`lsmod | grep bluetooth`查出来的模块，依次尝试，终于找到了正确的模块。

和wifi相关的模块是`mwifiex_pcie`， 和蓝牙相关的模块是`btusb`。

因此要做的操作就是`rmmod`和`modprobe`，休眠后执行下面的命令后，wifi和蓝牙就可以正常工作了。

     sudo rmmod -v btusb
     sudo rmbanbenmod -v mwifiex_pcie
     sudo modprobe -v btusb
     sudo modprobe -v mwifiex_pcie
 
但是这样就是每次都得再休眠后执行这些命令好像也略麻烦，最后看到又休眠后自动执行脚本的方法，`pm`和`systemctl`的休眠脚本位置不同，我对`pm`没印象，觉得arch的休眠几乎肯定是`systemctl`的，于是直接尝试了`systemctl`，`systemctl`的脚本位置在`/usr/lib/systemd/system-sleep`，这里的脚本会在sleep或者休眠时被调用。

我的脚本`/usr/lib/systemd/system-sleep/wakeup_suspend_dev.sh`的内容是：

```
    #!/bin/bash
    case $1 in
        pre)
          rmmod btusb
          rmmod mwifiex_pcie
        ;;
        post)
          modprobe btusb
                modprobe mwifiex_pcie
        ;;
    esac
```

`pre`是在休眠之前执行`rmmod`的操作，post是在休眠之后执行`modprobe`的操作。需要注意的是必须把这个脚本加可执行权限：

    sudo chmod +x wakeup_suspend_dev.sh

