Title:编译Linux From Scrach（LFS） --（2）下载LFS相关的源码并从创建目录和用户
Date: 2022-04-06 17:20
Modified: 2022-04-06 17:20
Category: Linux
Tags: linux, lfs
Authors: r341h


按照文档里的链接，每行一个链接的方法，创建wget-list-sysv和needed-patches-list，源码我放在我的github仓库： https://github.com/gccpacman/LFS-ubuntu2204


### 0） 假设已经完成了LFS（1）的步骤 -- 宿主机分区，设置LFS环境变量等



### 1） 在$LFS/sources/目录下，创建wget-list-sysv，执行以下命令批量下载源代码tar包

```

# wget-list-sysv
wget --input-file=wget-list-sysv --continue --directory-prefix=$LFS/sources

```

<!-- ![lfs source code]({static}/images/lfs2.png) -->

### 2）在$LFS/sources/patches目录下，创建needed-patches-list，执行以下命令批量下载源代码tar包

```

# needed-patches-list
wget --input-file=needed-patches-list --continue --directory-prefix=$LFS/sources/patches

```

<!-- ![lfs  source code]({static}/images/lfs2-2.png) -->

### 3） 创建基本LFS Linux目录结构

```

mkdir -pv $LFS/{etc,var} $LFS/usr/{bin,lib,sbin}
for i in bin lib sbin; do
  ln -sv usr/$i $LFS/$i
done
case $(uname -m) in
  x86_64) mkdir -pv $LFS/lib64 ;;
esac

mkdir -pv $LFS/tools

```

<!-- ![lfs  source code]({static}/images/lfs2-3.png) -->

### 4） 创建LFS宿主机用户, 并且将$LFS下的目录chown给lfs用户

```

groupadd lfs
useradd -s /bin/bash -g lfs -m -k /dev/null lfs
passwd lfs
# enter passwords for lfs user

# grant lfs $LFS directory permission
chown -v lfs $LFS/{usr{,/*},lib,var,etc,bin,sbin,tools}
case $(uname -m) in
  x86_64) chown -v lfs $LFS/lib64 ;;
esac

```

### 5) 初始化lfs用户的bashrc和bash_profile, 添加LFS, LFS_TGT等环境变量

```

cat > ~/.bash_profile << "EOF"
exec env -i HOME=$HOME TERM=$TERM PS1='\u:\w\$ ' /bin/bash
EOF

cat > ~/.bashrc << "EOF"
set +h
umask 022
LFS=/mnt/lfs
LC_ALL=POSIX
LFS_TGT=$(uname -m)-lfs-linux-gnu 
PATH=/usr/bin
if [ ! -L /bin ]; then PATH=/bin:$PATH; fi 
PATH=$LFS/tools/bin:$PATH 
CONFIG_SITE=$LFS/usr/share/config.site 
export LFS LC_ALL LFS_TGT PATH CONFIG_SITE 
EOF

```