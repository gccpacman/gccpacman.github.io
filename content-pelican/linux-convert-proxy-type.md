Title: Linux将Socks代理转换成Http代理
Date: 2015-05-14 10:20
Modified: 2015-05-14 19:30
Category: Linux
Tags: linux, proxy
Authors: r341h


安装polipo：

	sudo apt-get update
	sudo apt-get install polipo

编辑polipo配置文件 `/etc/polipo/config` ：

		### Basic configuration

		# Add your proxy's address
		proxyAddress = 192.168.0.1

		# Allow from anyone in the 192.168.0.* range to connect to your proxy
		allowedClients = 192.168.0.0/24

重启服务：

	sudo /etc/init.d/polipo restart

参考：

[Polipo - Community Help Wiki](https://help.ubuntu.com/community/Polipo)