Title: 墙内的Centos7 Linux安装K8S
Date: 2019-05-07 11:13
Category: Kubernetes
Tags: kubernetes, centos7, docker
Authors: r341h

1. 安装基础构建依赖

        $ yum -y install yum-utils device-mapper-persistent-data lvm2

2. 安装Docker

        $ yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
        $ yum -y install docker-ce
        $ systemctl start docker && systemctl enable docker 
        $ docker images   # 确定docker命令正常

3. 安装Kubernetes

    3.1 安装kubeadm, kubelet, kubectl

        $ vim kubernetes.repo

        [kubernetes]
        name=Kubernetes
        baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
        enabled=1
        gpgcheck=0
    

        $ yum -y install kubelet kubeadm kubectl kubernetes-cni
        $ systemctl enable kubelet && systemctl start kubelet

    3.2 pull下来kubernetes要要到的镜像，因为k8s.gcr.io这个域名被墙，需要从阿里云pull下来然后重新打tag，参考文档里的几篇版本都对不上，首先可以通过这个命令`列出`确定需要pull的镜像和版本：

        $ kubeadm config images list

    3.3 根据上一步列出的镜像和版本号，参考`https://github.com/cookcodeblog/k8s-deploy`的目录`kubeadm_v1.13.0/04_pull_kubernetes_images_from_aliyun.sh`编写一个脚本，注意替换成你需要的版本，然后执行。

    3.4 关闭swap，注释掉`/etc/fstab`里的swap一行，重启后生效，并关闭selinux

        $ swapoff -a
        $ setenforce 0
        $ sed -i 's/SELINUX=permissive/SELINUX=disabled/' /etc/sysconfig/selinux

    3.5 配置网络转发

        $ vim /etc/sysctl.d/k8s.conf

        net.bridge.bridge-nf-call-ip6tables = 1
        net.bridge.bridge-nf-call-iptables = 1
        net.ipv4.conf.all.forwarding = 1
        vm.swappiness = 0

        $ sysctl --system  # 确定配置生效

    3.6 初始化kubeadm，等待命令执行完成

        $ kubeadm init

    3.7 配置kubectl

        $ mkdir -p $HOME/.kube
        $ cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
        $ chown $(id -u):$(id -g) $HOME/.kube/config
        $ kubectl get nodes # 确认kubectl配置成功

4. 在Kubenetes里安装Flannel网络

    4.1 pull下Flannel镜像过程因为防火墙的原因依旧类似3.3操作，参考`https://github.com/cookcodeblog/k8s-deploy/tree/master/kubeadm_v1.13.0`里的`kubeadm_v1.13.0/pull_flannel_images_from_aliyun.sh`写一个脚本文件，这次的版本就用`v0.11.0`就好，便写完成执行脚本

    4.2 安装Flannel网络

        wget -O kube-flannel.yml https://raw.githubusercontent.com/coreos/flannel/a70459be0084506e4ec919aa1c114638878db11b/Documentation/kube-flannel.yml
        kubectl apply -f kube-flannel.yml
        
        # 过几十秒确认是否启动成功
        kubectl get pods --all-namespaces
        kubectl get cs

通过这四个步骤的成功执行，一个单机版本的Kubernetes已经安装完毕，接下去还可以做以下事情继续折腾，等之后有时间再折腾：
1. 添加一个worker节点加入到K8S集群
2. 可以根据参考文档，安装一个`K8S Dashboard`等或者部署应用
3. 尝试在自己实现Ingress的负载均衡


参考：

https://juejin.im/post/5c36fd906fb9a049f8197c9b

https://www.howtoforge.com/tutorial/centos-kubernetes-docker-cluster/

https://github.com/cookcodeblog/k8s-deploy