Title: windows的包管理Chocolate和vim.Vundle
Date: 2017-10-22 10:20
Modified: 2010-12-05 19:30
Category: Vim
Tags: windows, vim
Authors: r341h


Windows的开发环境一直都会让人比较头疼，一般解决方法有用Cygwin等模拟Linux的环境，Windows 10又自带了Ubuntu On Windows 10的环境。但是都或多或少有点问题，例如Cygwin的文件目录和windows分离，Ubuntu On Windows 10不能用Nodejs，打开X应用比较麻烦，只能用终端等。

经过很多尝试，我认为最友好的环境还是windows原生的环境，只是你需要偶尔告别命令行搜索某些应用需要的依赖，依次安装，这样其实绝大多数的开发环境都是可以部署的。不过还是有工具可以帮助我们，例如Windows其实也有一个类似apt-get或者[Homebrew](https://brew.sh/)的包管理工具，叫做[Chocolate](https://chocolatey.org/).

[安装Chocolate](https://chocolatey.org/install)只要在Powershell里写这行代码即可：

    Set-ExecutionPolicy Bypass; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

安装包的方法是`choco install <package_name>` 但是这个命令必须用admin权限的powershell来执行。于是想是不是有个windows的`sudo`，结果一查还真的有，而且可以用chocolate安装。于是admin执行powershell并运行了`choco install sudo`就安装好了。以后只要在普通用户的powershell执行`sudo choco install <package_name>`即可了。

我用choco安装了`git`, `vim`, `python`，`curl`，`wget`等工具，安装后powershell可以执行不少的类似linux的命令了。
但vim是裸奔状态，如果我直接把以前配置的.vimrc文件拿过来，显然用不来，甚至连Vundle包管理都用不来。Vundle的官方文档有[windows上配置的方法](https://github.com/VundleVim/Vundle.vim/wiki/Vundle-for-Windows)就是把:

    set rtp+=~/.vim/bundle/Vundle.vim
    call vundle#begin()

改成

    set rtp+=$HOME/.vim/bundle/Vundle.vim/
    call vundle#begin('$HOME/.vim/bundle/')

然后再执行`vim +BundleInstall +qall`就好了。