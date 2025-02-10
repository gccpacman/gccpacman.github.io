---
layout: post
title: Linux搭建PPTP VPN Server
date: 2015-04-19 10:20:00 
categories: Linux
tags: [linux, vpn]
---

1.  安装server

        # On CentOS 6 x64:
        rpm -i http://poptop.sourceforge.net/yum/stable/rhel6/pptp-release-current.noarch.rpm
        yum -y install pptpd
        # On Ubuntu 12.10 x64:
        apt-get install pptpd
  
2. 编辑 **/etc/pptpd.conf** 添加以下行:

        localip 10.0.0.1
        remoteip 10.0.0.100-200
  
localip本机ip(vpn的服务器ip), remoteip-分配给客户端的ip, 应该处于同一网段

3. 添加pptp用户名和密码到 **/etc/ppp/chap-secrets** :

        #client server secret IP
        user1 pptpd 24odfjafdi34 *
        user2 pptpd 3f3faf3fsdfI *
        #Where client is the username, server is type of service – pptpd for our example, secret is the password, and IP addresses specifies which IP address may authenticate. By setting ‘*’ in IP addresses field, you specify that you would accept username/password pair for any IP.  

4. 添加DNS服务器地址到 **/etc/ppp/pptpd-options**:

        ms-dns 8.8.8.8
        ms-dns 8.8.4.4

5. 启动 PPTP 守护进程daemon:

        service pptpd restart

6. 验证是否启动成功并接受连接

        netstat -alpn | grep :1723

7. 设置ipv4转发. 编辑 **/etc/sysctl.conf** 添加：
        
        #It is important to enable IP forwarding on your PPTP server. This will allow you to forward packets between public IP and private IPs that you setup with PPTP. )
        
        net.ipv4.ip_forward = 1

        # To make changes active, run 
        sysctl -p

8. 添加iptables规则

        #The following iptables firewall rules allow port 1723, GRE and perform NAT:

        iptables -I INPUT -p tcp --dport 1723 -m state --state NEW -j ACCEPT
        iptables -I INPUT -p gre -j ACCEPT
        iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE

        # In the last rule replace “eth0″ with the interface connecting to the internet on your VPN server. Finally the following rule is required to ensure websites load properly

        iptables -I FORWARD -p tcp --tcp-flags SYN,RST SYN -s 172.20.1.0/24 -j TCPMSS  --clamp-mss-to-pmtu
  
        # ReReplace **172.20.1.0/24** with the IP address range used in the “remoteip” option in the **/etc/pptpd.conf** this firewall rule is used to ensure a proper MTU value is used to prevent fragmentation.


参考:
[How To Setup Your Own VPN With PPTP](https://www.digitalocean.com/community/tutorials/how-to-setup-your-own-vpn-with-pptp)

[pptpd VPN: No internet access after connecting](http://askubuntu.com/questions/492923/pptpd-vpn-no-internet-access-after-connecting)
