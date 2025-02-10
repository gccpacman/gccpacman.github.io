---
title: "WSL无缝使用windows的Vagrant"
date: 2019-09-25T10:23:00
categories:
  - "WSL"
tags:
  - "windows"
  - "vagrant"
  - "linux"
draft: false
---
同时安装windows和wsl下的linux版本的vagrant，配置环境变量就可以使用。linux下vagrant的好处很多，首先文件的换行和权限的烦恼没有了，然后可以使用一些revision工具，例如ansible，在vagrantfile初始化的时候带来很多好处

下载地址：https://www.vagrantup.com/downloads.html

1. Windows下安装就直接exe了
2. Linux我的是Ubuntu，因此就下官网的deb包

    dpkg -i vagrant_amd64.deb

3. 需要在Linux的Home目录下的`.bashrc`或者`.zshrc`添加以下行，这样可以把windows的路径转换成WSL里的Linux路径：

export VAGRANT_WSL_ENABLE_WINDOWS_ACCESS="1"

4. 大功告成，在`wsl`输入`vagrant`，如果出现帮助信息就说明配置成功了

PS： 需要注意的是，wsl里的vagrant，不能读取Linux下的`Vagrantfile`，需要Vagrantfile存在于windows文件系统，因为本质上vagrant还是在windows上执行，调用Virtualbox等虚拟机的SDK，也就是说你的Vagrantfile，必须位于类似于`\mnt\c\`这样的windows挂载盘符目录下。

Also see：
https://www.vagrantup.com/docs/other/wsl.html