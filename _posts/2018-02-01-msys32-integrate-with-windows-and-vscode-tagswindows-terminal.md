---
layout: post
title: "MSys32 integrate with Windows and VSCode"
description: ""
category: 
tags: [windows, terminal]
---
{% include JB/setup %}

在不久之前发现了Msys2，基于Cygwin但是却又有一个让我觉得无比美好的包管理器Pacman(和Arch Linux的一样)，于是决定试试。但是真的用于Windows的终端还有很多麻烦的地方要解决，主要是以下几点：
1. Git的ssh_keygen配置，你和windows自己的CMD里的ssh_keygen能否共用
2. Msys用的换行符是和Linux一样的LF，而Windows的是CRLF
3. Python能不能直接用Windows的Python而不用模拟Unix环境的Python（有很多的bug）
4. 能否和我目前用的最多的VSCode编辑器无缝集成


经过一段时间的研究，每个问题都得到了很好的解决，目前来讲非常的完美，在这里分享一下：

1. 下载并安装 [Msys2](http://www.msys2.org/)

2. 安装和配置 `git`, 配置在windows上check出crlf格式文本，提交lf格式:

>>>
    安装git：
        $ pacman --needed -S bash pacman msys2-runtime  git 

    修改git处理回车的方式：
        $ git config --global core.autocrlf true  
	
3. 修改Home目录路径, Msys2默认的Home目录是Mingw64的/home/username, 但是我希望使用windows的Home目录/c/Users/username. 方法是编辑`/etc/nsswitch.conf`, 并修改

    db_home: windows
    
4.~~Install Python & Pip~~ (直接用windows的Python就好，用Mingw64的Python反而可能会有很多问题)

~~$ Pacman -S mingw-w64-x86_64-python2  mingw-w64-x86_64-python3 mingw-w64-x86_64-python2-pip mingw-w64-x86_64-python3-pip ~~



5. 让VSCode里的继承终端（VSCode Integrated Terminal）使用Msys2，在VSCode的settings里加入以下内容:
```
	{
	    "terminal.integrated.shell.windows": "C:\\msys64\\usr\\bin\\bash.exe",
	    "terminal.integrated.shellArgs.windows": [
		"--login",
	    ],
	    "terminal.integrated.env.windows": {
		"CHERE_INVOKING": "1",
		"MSYSTEM": "MINGW64",
	"MSYS2_PATH_TYPE": "inherit",
	    },
	} 
```


参考：

https://getpocket.com/a/read/1169705865

https://help.github.com/articles/dealing-with-line-endings

https://stackoverflow.com/questions/33942924/how-to-change-home-directory-and-start-directory-on-msys2

https://stackoverflow.com/questions/45836650/how-do-i-integrate-msys2-shell-into-visual-studio-code-on-window/48016561#comment84105772_48016561
