---
layout: post
title: Ubuntu Notes
updated: 2020-07-25
category: posts
---

**[声明]: 实验环境为 UEFI+GPT 的 Win10 笔记本电脑, 分区格式为 Ext2. 仅供参考.**

200125开坑Ubuntu, 被其简单的系统占用所折服, 开始使用ubuntu, 一直到现在. 这个记录其实是一以贯之的, 但里面的教程不保证一直有效, 加上我也只能阶段性的记录一下, 更多即时的记录请看 [Github - -nix](//github.com/dandelionfs/-nix)

<font size=1>~~多说一句: 在用完 Win10 后有感, **在没有深入了解意见科技产品前, 永远不要过分相信他带来的便利**, 你的电脑, 在你真正摸清楚他的操作原理和操作逻辑之前, 不要过分依赖他, 在他面前, 你可能就是赤裸的, 而我所真正担心的是我没有足够的时间和精力去见证世间的一切, 害怕的是自己不能静下心来慢慢的学习起来, 对那些Fast Learner肃然起敬, 但同时我始终都不了解真正的自己, 永远在以伤害自己的方式来逼迫自己努力, 而不是全身心的投入到自己的学习生涯中, 这又是多么的可悲……~~</font>

## INSTALL UBUNTU 

下载官方的镜像 (国内有大量的开源镜像网站) , 然后用 `Ultralso` 烧录到一个**8G** (4G) 大小的U盘. 重启电脑到 **BIOS** 中将 BOOT 里的 `BOOT Security` 关掉 (HP: F10), 重启进入系统**UEFI**的U盘启动的模式 (HP: F11), 之后进入U盘的 Ubuntu里面体验一下.准备安装.

不要直接安装. 需要**换源**, 去找系统的安装源list文件, 在`/etc/apt/sources.list`里, 用管理员的权限修改下载源地址 (提前查到自己对应版本的源地址) . 

```shell
sudo cp /etc/apt/sources.list /etc/apt/sources.list_backup #backup your old sourse 
sudo gedit /etc/apt/sources.list # open sources.list 
sudo apt update
```
**国内换源**:

- 高校镜像源有:
  - [Tinghua Mirror / 清华大学](https://mirrors.tuna.tsinghua.edu.cn)
  - [USTC  Mirror / 中国科学技术大学](https://mirrors.ustc.edu.cn)
  - [SJTU Mirror / 上海交通大学](https://ftp.sjtu.edu.cn)
  - [SHU Mirror / 上海大学](https://mirrors.shu.edu.cn)
- 企业镜像源: 
  - [Alibaba Mirror / 阿里](http://mirrors.aliyun.com) 
  - [Netease Mirror / 网易](http://mirrors.163.com)
  - [Huawei Mirrors / 华为](https://mirrors.huaweicloud.com)
  - [Tencent Mirror / 腾讯](https://mirrors.cloud.tencent.com)
  - [Yun-Idc / 首都在线](https://mirrors.yun-idc.com)

**国外换源**:<sup>[6](#j6)</sup>

- 高校开源镜像站：
  - [The Chinese University of Hong Kong](https://ftp.cuhk.edu.hk)
  - [元智大學](https://ftp.yzu.edu.tw)
  - [Massachusetts Institute of Technology](https://mirrors.mit.edu)
- 云服务商开源镜像站：
  - [Digital Ocean](https://mirrors.digitalocean.com)
  - [Linode](https://mirrors.linode.com)
  - [Cat Networks](https://mirrors.cat.net)
- 公益开源镜像站：
  - [Kernel ORG](https://mirrors.kernel.org)
  - [Yandex](https://mirror.yandex.ru)

分盘的时候还请参考最下面的地址, 但是值得注意一下`boot`不要太小气, 就我的话, 我给他2G有点多了, 1G刚刚好, 主分区32G, 交换空间8G( 貌似和Win10虚存类似, 太大也不必), 家目录 60G, 共100G, 分区也仅供参考. 

更详细的可以参考更详细的教程: [Ubuntu 换源, 安装&卸载软件](https://zhuanlan.zhihu.com/p/27187622).

## SYS UPDATE
```shell
sudo update-manager -c -d
```

## APT MANAGE
一般来说, 安装命令有<sup>[10](#j10)</sup>: 

```shell
sudo apt install xxx
sudo apt reinstall xxx
sudo apt reinstall -d xxx  
sudo apt install tree -y # 使用apt安装软件,譬如安装tree,这里的 -y 参数是为了在安装的时候默认选择yes
sudo dpkg -i xxx.deb # deb包安装
sudo apt install gdebi
sudo gdebi netease-cloud-music_1.2.1_amd64_ubuntu_20190428.deb
sudo apt install -f #安装依赖 (如果提示需要的话)
sudo apt install ./xxxx.deb  #另一种deb包安装方式
#安装filename.tar.gz软件,然后在解压目录或者bin文件夹中执行setup.sh文件
```
**源码安装**: 有些软件没有被收录进软件镜像源, 或者说开发者需要去使用他们最新的版本, 这时候就要自己去他们的官网或者是代码托管平台下载最新的Linux源码, 自己来build. 这种方式安装需要解决很多的依赖, 安装前多Google. 此处还是以tree为例: 

- 先下载最新的源码包

```shell
  tar zxf tree-1.7.0.tgz #解压
  cd  tree-1.7.0/
  
  sudo make # make and install
  sudo make instal l# 如果没有配置环境, 先用apt安装build-essential
```
+ [忽略某些依赖安装(Wechat Failure)](https://qastack.cn/server/250224/how-do-i-get-apt-to-ignore-some-dependencies)

```shell
# Check Depend
dpkg --info XXX.deb | grep Depends
# Apt-get
sudo apt install XXX.deb-
# dpkg
sudo dpkg -i --ignore-depends=<--->  XXX.deb
```

### Uninstall

```shell
sudo apt remove --purge XXX
sudo apt autoremove --purge XXX

dpkg --get-selections | grep XXX
sudo apt purge XXX  #一个带core的package, 如果没有带core的package, 则是情况而定. 
```

### Clean
```shell
sudo apt autoclean # 只删除过时的软件包, 例如最近更新所取代的软件包, 就完全不需要它们. 
sudo apt autoremove

dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P 

# 清理日志问题.
sudo echo > /var/log/syslog
sudo echo > /var/log/kern.log
```
如果出现zsh/shell权限不足的情况, 使用`sudo -i`临时切换到`Root`用户的模式下进行操作. 操作完`exit`退出即可.

**清理SNAP**

执行脚本:

```shell
#!/bin/shell
# Removes old revisions of snaps
# CLOSE ALL SNAPS BEFORE RUNNING THIS
set -eu
snap list --all | awk '/disabled/{print $1, $3}' |
    while read snapname revision; do
        snap remove "$snapname" --revision="$revision"
    done
```

### Run AppImage

> AppImage 是一种把应用打包成单一文件的格式, 允许在各种不同的目标系统 (基础系统(Debian、RHEL等), 发行版(Ubuntu、Deepin等)) 上运行, 无需进一步修改. 

简而言之就是绿色通用版本.

下载好程序的时候选择[属性]-> 可执行文件. 点击即可, 一般我习惯放在 `/home/usrname/opt/`下, 也可以节省下根目录的空间内存......

```
cd /usr/share/applications
```

创建一个`.desktop`文件. 然后编辑以下内容即可创建图标, 值得注意的是程序运行的图标的是包自带的, 这里定义的只能是应用菜单的.[^14][^15]

```shell
[Desktop Entry]
Version=1.0	
Encoding=UTF-8			# 字符编码  
Name= XXX 
Comment= XXX			# 鼠标经上提示名称 也可国际化
Exec=XXX 				# 菜单执行的命令或程序路径
Terminal=false
Icon=XXX 				# 图标路径
Type=Application
Categories=Development
StartupNotify=false;	#设置软件启动是不通知
Hidden=false			#菜单是否隐藏, 类似NoDisplay属性
```

### BINARY FILE

直接编译好的包可以`./x`运行即可, 方便的话就打包一个`desktop`文件.

### Knowledge For APT & APT-GET

**APT**的其它命令选项可以实现与使用 apt-get 时相同的操作. 虽然 apt 与 apt-get 有一些类似的命令选项, 但它并不能完全向下兼容 apt-get 命令. 也就是说, 可以用 apt 替换部分 apt-get 系列命令, 但不是全部. 

|     apt 命令     |      取代的命令      |           命令的功能           |
| :--------------: | :------------------: | :----------------------------: |
|   apt install    |   apt-get install    |           安装软件包           |
|    apt remove    |    apt-get remove    |           移除软件包           |
|    apt purge     |    apt-get purge     |      移除软件包及配置文件      |
|    apt update    |    apt-get update    |         刷新存储库索引         |
|   apt upgrade    |   apt-get upgrade    |     升级所有可升级的软件包     |
|  apt autoremove  |  apt-get autoremove  |       自动删除不需要的包       |
| apt full-upgrade | apt-get dist-upgrade | 在升级软件包时自动处理依赖关系 |
|    apt search    |   apt-cache search   |          搜索应用程序          |
|     apt show     |    apt-cache show    |           显示装细节           |

当然, apt 还有一些自己的命令: 

|   新的apt命令    |             命令的功能              |
| :--------------: | :---------------------------------: |
|     apt list     | 列出包含条件的包 (已安装, 可升级等) |
| apt edit-sources |             编辑源列表              |

**APT-GET**

对于低级操作, 仍然需要 apt-get. 

### Deb Manage

- 打包DEB实践参考<supf>[4](#j4)[5](#j5)</supf>

## SHORTCUT

### Desktop Shortcut

| Operation  |                   Effects                    | Operation |             Effects             |
| :--------: | :------------------------------------------: | :-------: | :-----------------------------: |
|  Alt + F1  | 聚焦到桌面左侧任务导航栏, 可按上下键进行导航 | Alt + F2  |            运行命令             |
|  Alt + F4  |                 关闭当前窗口                 | Alt + Tab |          切换程序窗口           |
| Alt + 空格 |                 打开窗口菜单                 |   PrtSc   |            桌面截图             |
|  Win + A   |                搜索/浏览程序                 |    Win    | 搜索/浏览程序、文件、音乐文件等 |
|  Win + F   |                搜索/浏览文件                 |  Win + M  |        搜索/浏览音乐文件        |



### Terminal Shortcut

|       Operation       |                 Effects                  |        Operation        |                       Effects                        |
| :-------------------: | :--------------------------------------: | :---------------------: | :--------------------------------------------------: |
|    Ctrl + Alt + T     |                 打开终端                 |           Tab           |                 命令或文件名自动补全                 |
|   Ctrl + Shift + C    |                   复制                   |    Ctrl + Shift + V     |                         粘贴                         |
|   Ctrl + Shift + T    |        在同一个窗口新建终端标签页        |    Ctrl + Shift + W     |                      关闭标签页                      |
|   Ctrl + Shift + N    |               新建终端窗口               |    Ctrl + Shift + Q     |                     关闭终端窗口                     |
| Ctrl + Shift + PageUp |                标签页左移                | Ctrl + Shift + PageDown |                      标签页右移                      |
|       Ctrl + D        |                关闭标签页                |        Ctrl + C         |                     终止当前任务                     |
|       Ctrl + L        |                 清除屏幕                 |        Ctrl + P         |                  显示上一条历史命令                  |
|       Ctrl + N        |            显示下一条历史命令            |        Ctrl + R         |                   反向搜索历史命令                   |
|      Ctrl + J/M       |           回车 (同enter键功能)           |        Ctrl + A         |                    光标移动到行首                    |
|       Ctrl + E        |              光标移动到行尾              |        Ctrl + B         |           关闭想后移动一个位置 (backward)            |
|       Ctrl + Z        |          把当前任务放到后台运行          |      Ctrl + PageUp      |                   前一个终端标签页                   |
|    Ctrl + PageDown    |             下一个终端标签页             |           F1            |                     打开帮助指南                     |
|        Win + W        |               展示所有窗口               |         Win + T         |                      打开回收站                      |
|    Ctrl + Win + ↓     |           还原/最小化当前窗口            |     Ctrl + Win + D      |                    最小化所有窗口                    |
|       Ctrl + &        |        恢复Ctrl + H/D/W删除的内容        |     Ctrl + Win + ↑      |                    最大化当前窗口                    |
|       Ctrl + D        |  删除光标位置的一个字符 (delete键功能)   |        Ctrl + W         | 删除光标位置的前一个单词 (Alt + Backspace组合键功能) |
|       Ctrl + K        |      剪切从光标位置到行末的所有字符      |        Ctrl + Y         |           粘贴Ctrl + U/Ctrl + K剪切的内容            |
|       Ctrl + U        | 剪切从行的开头到光标前一个位置的所有字符 |       Ctrl + H/\*       |      删除光标位置的前一个字符 (backspace键功能)      |
|       Ctrl + ←        |        光标移动到下一个单词的词尾        |        Ctrl + →         |              光标移动到上一个单词的词首              |
|        Alt + H        |          打开“帮助”菜单 (help)           |        Ctrl + T         |       将光标位置的字符和前一个字符进行位置交换       |
|        Alt + V        |          打开“查看“菜单 (view)           |         Alt + T         |              打开“终端”菜单 (terminal)               |
|        Alt + E        |          打开“编辑”菜单 (edit)           |         Alt + S         |               打开“搜索”菜单 (search)                |
|          F11          |                 全屏切换                 |         Alt + F         |                打开“文件”菜单 (file)                 |

补充: 

2次连续Tab/4次连续Esc/2次连续Ctrl + I|将显示所有命令和工具名称



### Gedit Shortcut

| Operation |  Effects   |    Operation     |  Effects   |
| :-------: | :--------: | :--------------: | :--------: |
| Ctrl + N  |  新建文档  |     Ctrl + W     |  关闭文档  |
| Ctrl + S  |  保存文档  | Ctrl + Shift + S |   另存为   |
| Ctrl + F  |    搜索    |     Ctrl + H     | 搜索并替换 |
| Ctrl + I  | 跳到某一行 |     Ctrl + C     |    复制    |
| Ctrl + V  |    粘贴    |     Ctrl + X     |    剪切    |
| Ctrl + Q  |    退出    |                  |            |

使用 `ctrl + ;` (此为 fcitx 自带剪贴板插件)  : 查看粘贴板的内容, 此时显示的就不只有一条内容, 一般而言是最近的五次复制的内容. 使用数字键进行选择. 



## BUGS

![](https://dandelionfs.oss-cn-beijing.aliyuncs.com/fix-ubuntu-bug-tieba.webp)

### Boot 无法进去系统(花屏)

由于 Ubuntu(Linux) 并不是内置N卡驱动, 所以如果有 N卡独显 笔记本会发生在 Ufi模式 下启动U盘进入系统的时候卡死. 应该先用 `e` 进去 Boot 设置, 在末尾 quiet splash 的后面先空一格再加上`acpi_osi=linux nomodeset`, F10保存退出, 

[Tip] : 如果quiet splash后面发现有- - -这串符号, 直接删了就是, 只要保证上述添加的参数在splash后面即可

### N卡驱动

进去之后要换aliyun的源, 进去发现分辨率是锁死的(反正不是1080P), ~~是Ubuntu自带的显卡驱动背的锅~~(好像Ubuntu20.04LTS 已经自带 N卡 驱动了......), 更新N卡驱动: 

```shell
sudo ubuntu-drivers autoinstall # 自动安装

sudo gedit /etc/modprobe.d/blacklist.conf # 黑名单
blacklist vga16fb # for nvidia display device install
blacklist nouveau
blacklist rivafb
blacklist rivatv
blacklist nvidiafb

sudo update-initramfs -u &&  reboot # 刷新重启
```


### Touchpad

下面是一段脚本<sup>[1](#j1)</sup>, 保存`sh`文件后运行.

```shell
#!/bin/shell
#
# Gestures install 
# version 1.3
# 
# by The Fan Club 2020
#
# NOTE: run as sudo
#
#
# Remove if selected 
if [ "$1" = "--remove" ]; then 
	echo "[Gestures] Gestures uninstall started..."
	python3 -m pip uninstall gestures
	rm /usr/local/bin/gestures
	rm /usr/share/applications/org.cunidev.gestures.desktop
	rm /usr/share/metainfo/org.cunidev.gestures.appdata.xml
	rm /usr/share/icons/hicolor/scalable/apps/org.cunidev.gestures.svg
	# remove libinput-gestures
	su $SUDO_USER libinput-gestures-setup stop
	su $SUDO_USER libinput-gestures-setup autostop
	libinput-gestures-setup uninstall	
	echo "[Gestures] Gestures removal complete."
	exit 
fi
#
# Install libinput-gestures - https://github.com/bulletmark/libinput-gestures
echo "[Gestures] Gestures install started..."
#
# Add user to input group
gpasswd -a $SUDO_USER input
echo "[Gestures] $SUDO_USER added to input user group"
# Install prerequisites
echo "[Gestures] Install all depedencies"
apt-get install xdotool wmctrl libinput-tools python3 python3-setuptools python3-gi python-gobject python3-pip build-essential git 
# Install/Update
if [ -d libinput-gestures ]; then
	rm -r libinput-gestures 
fi
echo "[Gestures] Downloading libinput-gestures from GitHub..."
git clone https://github.com/bulletmark/libinput-gestures.git
cd libinput-gestures
make install
cd ..
echo "[Gestures] libinput-gestures installed"
#
# Install Gestures - https://gitlab.com/cunidev/gestures
#
# Install 
if [ -d gestures ]; then
	rm -r gestures 
fi
echo "[Gestures] Downloading Gestures from GitLab..."
git clone https://gitlab.com/cunidev/gestures
cd gestures
python3 setup.py install
# Cleanup
cd ..
rm -r gestures 
rm -r libinput-gestures 
echo "[Gestures] Gestures installation complete"
# Autostart libinput-gestures at boot and start now for current user
su $SUDO_USER libinput-gestures-setup stop
su $SUDO_USER libinput-gestures-setup autostart
su $SUDO_USER libinput-gestures-setup start
echo "[Gestures] libinput-gestures started for $SUDO_USER"
# Autostart Gestures 
cp /usr/share/applications/org.cunidev.gestures.desktop /home/$SUDO_USER/.config/autostart/
sed -i 's/=gestures/=gestures\&/g' /home/$SUDO_USER/.config/autostart/org.cunidev.gestures.desktop
chown $SUDO_USER:$SUDO_USER /home/$SUDO_USER/.config/autostart/org.cunidev.gestures.desktop
echo
echo "[Gestures] Reboot to complete the installation"
```
解决无法支持三指和四指的遗憾.


### 亮度异常

安装完成之后发现亮度是不可以调节 :

```shell
# edit by nano, choose one between vim and nano. 
# 按 Ctrl+O 保存、按 Ctrl+X 退出编辑
sudo nano /etc/default/grub

# edit by vim/vi
sudo apt
sudo vim /etc/default/grub
```

将` GRUB_CMDLINE_LINEX_DEFAULT`那一行改成: 

```shell
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash acpi_backlight=vendor acpi_osi=Linux"
# 更新后重启 (重启可能时间比较长)
sudo update-grub && reboot
```

### 语言设置

一个小小的建议: 语言设置这是用拖动的 [笑] . 

### dpkg:错误: 另外一个进程已经为 dpkg 状态数据库 加锁

可能是开机自动更新会占用一会儿这个进程, 要么PS kill 他, 要么等一会就可以. 

### 安装deb 包缺少以来关系, 仍未被处理的时候

```shell
sudo apt install -f
```
### ubuntu 18.04无法从fwupd下载固件

> 通常是更新BIOS、更新网卡之类的需要fwupd. Android手机的bootloader就相当于电脑BIOS, 所以Android更容易刷成砖. 电脑重装系统是不会碰BIOS的, 所以特殊情况才会成砖. 


### 双系统的时间不统一

```shell
#这个是Bios里面的 Boot Secury 的问题, 但是关闭之后在进入Ubuntu后又会出现一系列问题.
sudo hwclock -w --localtime
```

### initramfs-tools报错

当初分盘的时候太小气, 看见别人`/boot`分区给了200M, 但是太小了, 以后给大点就不会有这问题了. 解决方法是删掉多余的内核. dpkg命令是Debian Linux系统用来安装、创建和管理软件包的实用工具. 查看自己的linux内核和正使用的内核, 然后选择性删除. 

```shell
sudo dpkg --get-selections |grep linux-image
sudo uname -a
sudo apt purge 内核名称
```

然后清理/usr/src目录,删除你已经卸载的内核目录

内核版本显示为**install, 表示系统已经安装了相应的内核, 使用purge命令删除相应的内核. **

```shell
sudo apt purge linux-image-4.4.0-130-generic
```

**deinstall**, 表示系统没有安装此内核, 但是在配置文件中还残留它的信息, 也有可能是以前卸载的时候不彻底.  正常情况下, 就已经清理完成辣. 输入`df`查看/boot的已用百分比. 

```shell
 sudo dpkg -P linux-image-extra-4.4.0-128-generic
```

### 更换介质: 请把标有……

> “更换介质: 请把标有…… DVD 的盘片插入驱动器“/media/cdrom/”再按回车键, 

```shell
# 修改`/etc/apt/sources.list`文件, 注释掉`deb cdrom:`开头的一行 (第一行) 
cd ~
vim /etc/apt/sources.list
apt update
```

### ubuntu支持`exfat`方法

> 推荐u盘使用exfat格式, 为什么呢？两个原因: 
> 1、三大主流操作系统 (Linux、Mac、Windows) 都支持exfat格式. 
> 2、exfat支持大于4G的文件. 

在ubuntu下, 由于版权的原因 (据说) , 默认不支持exfat格式的u盘, 对于ubuntu 14.04以上版本, 直接运行下面的命令就可以了: 

```shell
sudo apt install exfat-utils
```

### Ubuntu的在线账户

及时获取Ubuntu社区的更新.

### snap错误has install-snap change in progress

```shell
snap changes # 获取任务Id
sudo snap abort 14
```

### Ubuntu 永久挂载Win10磁盘

实际挂载前, D盘为 `/dev/XX`, E盘为 `/dev/XXX` (**注意！这里 sd 后面的不一定和 Windows 一样, 图里 Windows 和 Ubuntu 同处于 SSD 上, 而 D 和 E 盘均位于 HDD 上, 所以从 `a` 变成了 `b`**) 

> **接下来, 我们假设你要挂载的分区地址为 `/dev/XX` (原 Windows 中的非系统文件目录, 即通常意义上的 Windows 分区) , 要挂载到地址为 `/mnt/windows/d` (Ubuntu 中的非系统文件目录, 即 Linux 中的一个目录) **
> 你当然可以 (而且必须) 根据你的实际情况修改分区地址

```shell
sudo mkdir /mnt/windows/d# 然后关闭 WIndows 的**快速启动**, 临时挂载, 重启失效, 适用于偶尔需要一次的: 
sudo mount /dev/XX  /mnt/windows/d
```

在执行完成后, 访问你的 `/mnt/windows/d` 应该就能看到原盘符中的文件了, 没有文件显示请重启电脑查看

第二种方式——永久挂载. 

我们需要修改系统文件 `/etc/fstab`, 在此之前, 我们需要先获得 `/dev/XX` 的 `UUID`, 执行指令: 

```shell
sudo blkid /dev/XX  
sudo apt install vim
sudo vim /etc/fstab
#插入形如 UUID=XXXXXXXXXX   /mnt/windows/d   ntfs  defaults   0   2的字段; 其中第一列为UUID, 第二列为挂载目录 (该目录必须为空目录) , 第三列为文件系统类型, 第四列为参数, 第五列0表示不备份, 最后一列必须为２或0(除非引导分区为1), 如果你是grub引导的话, 你会注意到boot分区是1.
sudo mount -a#检查一下, 发现还是报错, The disk contains an unclean file system, 执行下面: 
sudo apt install ntfs-3g
sudo ntfsfix /dev/XX
sudo mount -a#再检查一下, 发现全是OK, 哈哈
```

上面流程走一遍发现该目录下没有文件, 可以右键属性检查一下, 如果确实存在, 那么重启电脑就OK了, 我只挂载了我win的数据盘, 系统盘还是不要动的好……

### Grub Wifi

```shell
909778] iwlwifi 0000: 00: 14.3: BIOS contains HGDS but no HRDS
```
暂时无解, 不影响使用...

### Root模式 部分命令找不到

因为系统变量和用户变量不一样, 所以需要将用户变量配置到系统变量里.

### 没有批量操作的压缩命令

- 写 Shell/Python 脚本
```shell
    for i in (fileName)
    do
    xxx -x $i
    done
```
- 使用gnome的右键压缩指令.
- Other

### Ubuntu Utf-8 和 Win GBK 的转化

+ 使用`unar`命令: `unar (-o (GBK)) xx.zip`
+ Other

### /bin/shell^M: bad interpreter: No such file or directory

[Cause] : 脚本文件是DOS格式的, 即每一行的行尾以\r\n来标识

```shell
:set ff? # 如果显示是DOS/UNIX
set ff=unix
```

### Hang Up Bug

长时间挂起会导致显示出现问题, 我自己遇到的是 GUI页面崩溃. 可以进入tty2 输入 r 来重启 GUI页面, 但是声卡出现问题[输出显示伪输出]暂时没有什么有效的解决方法, 

#### 挂起后花屏？

挂起时间和导致的问题相关, 短时间内挂机不会产生什么作用, 但是长时间就会导致 Preface 里面的问题.

挂起:Suspend To RAM(STR)

休眠: Suspend To Disk(STD)

一种可能是设备的驱动问题不支持挂起, 但是短时间却可以这是什么鬼??? 

#### 伪输出[Undo]

+ 把你当前的用户加入audio组

```shell
sudo usermod -a -G audio $USER
```

更加详细的可以参考[这个](https://zhuanlan.zhihu.com/p/122887848)

+ 可能是内核的问题

暂无解决方法, TO BE CONTINUED...

### 输出文件中带有` 口[34;42m` `口[00m`等乱码字符

这个是因为输入的文件带有颜色转义符号引起的, 所以想办法临时禁用颜色即可.

### su提示认证失败

Ubuntu安装后, root用户默认是被锁定了的, 不允许登录, 也不允许 su 到 root , 对于桌面用户来说这个可能是为了增强安全性

```shell
sudo passwd # 输入安装时那个用户的密码 , 新的Root用户密码
```

### 扩展触摸屏触控错位

造成的原因是 触控的驱动进程的端口是自己的主显示器/旋转自己的显示器但是触控没有跟着旋转, 所以需要用命令让进程的端口开放给显示器 `HDMI接口` 上. 具体如下:

```shell
xrandr # primitive command line interface to RandR extension
xinput # utility to configure and test X input devices
xinput map-to-output XXX(ID) HDMI-0
# Restricts the movements of the absolute device to  the  RandR  crtc.  The output  name  must match a currently connected output (see xrandr(1)). If the NVIDIA binary driver is detected or RandR 1.2 or later is not  avail‐able,  a  Xinerama  output may be specified as "HEAD-N", with N being the Xinerama screen number. This option has no effect on relative devices.
```

但是关于显示器用来画画那种需要频繁切换的用户, 建议走:
- [Ubuntu下触摸屏校准及自动旋转屏幕](https://all2h.com/post/2011/01/08/%E8%BF%99%E5%A4%A9%E6%9D%80%E7%9A%84web-qq-2-0-6)
- [树莓派(Linux 系统)触摸屏翻转显示以及触摸翻转](https://blog.csdn.net/u013491946/article/details/79895853)


### libinput

一个触控屏驱动, 更多参考:
- [What is libinput](https://wayland.freedesktop.org/libinput/doc/latest/what-is-libinput.html)

### Linux 下蓝牙鼠标连接几秒后自动断开

- https://www.v2ex.com/t/399966
- https://unix.stackexchange.com/questions/91027/how-to-disable-usb-autosuspend-on-kernel-3-7-10-or-above%E3%80%82
- https://www.it-swarm.asia/zh/usb/%e5%a6%82%e4%bd%95%e7%a6%81%e7%94%a8%e7%89%b9%e5%ae%9a%e8%ae%be%e5%a4%87%e7%9a%84usbautosuspend%ef%bc%9f/959819442/


###  Gtk-WARNING theme directory

之前为了移除系统以及自己折腾留下的冗余主题包, 尝试了一些 `/usr/share/icons` 的删改工作, 但是

```bash
sudo rm -rf hicolor
# then
(firefox:3133): Gtk-WARNING **: 14:37:30.455: Theme file for Bibata-Original-Ice has no directories
# reinstall the software
gtk-update-icon-cache: No theme index file. WARNING: icon cache generation failed
```

`/usr/share/icons/hicolor/*` or `~/.local/share/icons/hicolor` 是图标缓存的目录, 并且在编辑 `.desktop` 文件中可以直接忽略路径引用名字来调用图片, 如果你希望 `software menu` 图表得到刷新, 你可以尝试执行<sup>[8](#j8)</sup>:

```shell
sudo touch /usr/share/icons/hicolor ~/.local/share/icons/hicolor
sudo gtk-update-icon-cache
```

### Suspend 挂起唤醒后桌面卡死

在平时挂起时间久了之后, 再次唤醒界面就会变得模糊/黑块, 目前探索到的唯一一个解决方案就是切换到 `tty4`, `top` 然后杀掉 `Xorg` 应用, GDM 返回登录框以另外一个用户重新系统, 据查到的相关资料<sup>[9](#j9)</sup>, 之前 `xfree86(tinyx一种) + gdm` 搭配，在杀死 `xfree86` 进程后，`GDM` 不会重启到登录框


## BEAUTIFY

### Theme

`Ubuntu GNOME` 最简单的美化依赖 `gnome-tweaks`, 包含显示秒数, 动画, 插件安装, 主题选择等. 命令行直接安装即可.

如果需要主题美化的话, 这里只推荐一个 vinceliuice 的 [WhiteSur-gtk-theme](https://github.com/vinceliuice/WhiteSur-gtk-theme), 里面包含了在 `GDM` 环境下安装 `Theme`, `Dash to Dock` 的主题修改, `Firefox` 布局的重排. 更多的可以去看[Gnome-look](https://www.gnome-look.org/).

其中, `GDM(GNOME Display Manager)` 环境下安装主题意味着, 它可以带来使用命令行即可切换 `dark mode` 和 `light mode`的效果, 弥补了 `Ubuntu Gnome Tweaks` 切换的繁琐. `Firefox` 可以通过 `Dark Reader` 弥补网页, `VsCode` 可以通过 `Atom Dark/Light Theme` 以及 `Window:auto detect color scheme` 来进行选择.

```shell
gsettings set org.gnome.desktop.interface gtk-theme "XXX" # theme
gsettings set org.gnome.desktop.wm.preferences theme "XXX" # shell
```

### Fonts

<sup>[2](#j2)</sup>
- 通用方法粘到 `/usr/share/fonts` 后 `fc-cache` 生成字体缓存 fontconfig.
- 双系统可以在挂载系统盘后链接到该路径, `ln -s /XXX(Windowsdrive)/Windows/Fonts /usr/share/fonts/WindowsFonts` 将字体位置链接到 Linux 系统的字体文件夹后再生成字体缓存.

### Icons

Freedesktop.org 致力于Linux和其他类Unix上的X窗口系统的桌面环境之间的互操作性和基础技术共享的项目. 目前托管在 GitLab.

- 图标目录: `/usr/share/icons/`

## Extensions

- **Caffeine**
- **Dash to Dock** 
   - [禁用 Ubuntu Dock 的方法](https://zhuanlan.zhihu.com/p/48078003)
  - [为什么会有两个 Dock 的贴](https://qastack.cn/ubuntu/975387/why-do-i-have-two-docks-in-ubuntu-17-10-desktop)
  - `sudo apt remove gnome-shell-extension-ubuntu-dock`
- **Desktop Icons**
- Desktop Scroller (Left and Overview version) 
- **Dynamic Panel Transparency** 
- Extensions 
- **Files Menu** 
- **Gnomesome**-[Github](https://github.com/ChWick/gnomesome)
  - 拓展天然与 `Dash to Dock` 的 `Super+num` 冲突, `Super + a`/`Super + Up/Down/Left/Rifht (maximize/restore/left/right)` 可能失效, 需要重新设置一下.
  - Shortcuts-快捷键:
    - `Mod4+e`: Select the next layout on the current monitor and workspace
    - `Mod4+j`: Select the next window on the current monitor and workspace
    - `Mod4+k`: Select the previous window on the current monitor and workspace
    - `Mod4+Ctrl+j`: Select the next monitor
    - `Mod4+Ctrl+k`: Select the previous monitor
    - `Mod4+o`: Move the active window to the next monitor
    - `Mod4+Ctrl+Shift+j`: Move the active window to the next monitor
    - `Mod4+Ctrl+Shift+k`: Move the active window to the previous monitor
    - `Mod4+(1-5)`: Select the workspace with id (1-5)
    - `Mod4+Ctrl+(1-5)`: Move the current window to the workspace with id (1-5)
    - `Mod4+return`: Launch a gnome terminal
  - [使用 Material Shell 扩展将你的 GNOME 桌面打造成平铺式风格-Linux 中国](https://zhuanlan.zhihu.com/p/350535415)
    - 拓展很高效, 但会修改桌面的一些参数, 比如 `Titlebar` 的布局会右移.
- gTile
- **Material Shell** 
- NoAnnoyance 
- **OpenWeather** 
- Places Status Indicator 
- Removable Drive Menu 
- **Simple net speed** 
- Sound Input & Output Device Chooser 
- **system- monitor** 
- TopIcons Plus 
- **Unite** 
- **User Themes** 

## DESKTOP

编辑 `.desktop` 文件可以参考下面模板<sup>[3](#j3)</sup>:

```shell
$ sudo vim /usr/share/applications/Clash.desktop
$ vim Clash.desktop
＃[Desktop Entry] 文件头
＃Version    版本
＃Name    应用名称
＃Name[xx]    不同语言的应用名称
＃Comment 注释
＃Exec    执行文件路径
＃Icon    图标路径
＃Terminal    是否使用终端
＃Type    启动器类型
＃Categories  应用的类型 (内容相关) 
```

## AUTO RUN
### 指定运行级别

`/etc/inittab`

- 0: 关机
- 1: 单用户【找回丢失密码】
- 2: 多用户状态没有网络服务
- **3**: 多用户状态有网络服务
- 4: 系统未使用保留给用户
- **5**: 图形界面
- 6: 系统重启


如何找回 root 密码, 如果我们不小心, 忘记 root  密码, 怎么找回. 
- 思路:  进入到 单用户模式, 然后修改 root 密码. 因为进入单用户模式, root 不需要密码就可以登录. 


## FM(File Manage) 


|                      | 可分享的（shareable）        | 不可分享的（unshareable） |
| -------------------- | ---------------------------- | ------------------------- |
| 不变的（static）     | /usr （软件放置处）          | /etc （配置文件）         |
|                      | /opt （第三方协力软件）      | /boot （开机与核心档）    |
| 可变动的（variable） | /var/mail （使用者邮件信箱） | /var/run （程序相关）     |
|                      | /var/spool/news （新闻群组） | /var/lock （程序相关）    |


- 可分享的：可以分享给其他系统挂载使用的目录，所以包括可执行文件与使用者的邮件等数据， 是能够分享给网络上其他主机挂载用的目录；
- 不可分享的：自己机器上面运行的设备文件或者是与程序有关的socket文件等， 由于仅与自身机器有关，所以当然就不适合分享给其他主机了。
- 不变的：有些数据是不会经常变动的，跟随着distribution而不变动。 例如函数库、文件说明文档、系统管理员所管理的主机服务配置文件等等；
- 可变动的：经常改变的数据，例如登录文件、一般用户可自行收受的新闻群组等。

## LINUX FILE TREE

- FHS: Filesystem Hierarchy Standard. 重点在于规范每个特定的目录下应该要放置什么样子的数据, Linux操作系统就能够在既有的面貌下（目录架构不变）发展出开发者想要的独特风格。

  - `/lost+found`: 当文件系统发生错误时， 将一些遗失的片段放置到这个目录下
    - 标准的ext2/ext3/ext4文件系统格式才会产生的一个目录, xfs 文件系统的话，就不会存在这个目录
  - `/proc`: virtual file system, 虚拟文件系统, 他放置的数据都是在内存当中(不占任何硬盘空间)，例如系统核心、行程信息（process）、周边设备的状态及网络状态等等。比较重要的文件
    - `/proc/cpuinfo`, `/proc/dma`, `/proc/interrupts`, `/proc/ioports`, `/proc/net/*`......
  - `/sys`: 这个目录其实跟/proc非常类似，也是一个虚拟的文件系统，主要也是记录核心与系统硬件信息较相关的信息。 包括目前已载入的核心模块与核心侦测到的硬件设备信息等等。这个目录同样不占硬盘容量喔！
  - / （root, 根目录）：与开机系统有关；因为根目录很重要，所以根目录不要放在非常大的分区内，因为越多的数据可能有较多发生错误的机会


| 目录       | 应放置文件内容                                               |
| ---------- | ------------------------------------------------------------ |
| 第一部份   | FHS 要求必须要存在的目录                                     |
| /bin       | 系统有很多放置可执行文件的目录，但/bin比较特殊。因为/bin放置的是在单人维护模式下还能够被操作的指令。 在/bin下面的指令可以被root与一般帐号所使用，主要有：cat, chmod, chown, date, mv, mkdir, cp, shell等等常用的指令。 |
| /boot      | 这个目录主要在放置开机会使用到的文件，包括Linux核心文件以及开机菜单与开机所需配置文件等等。 Linux kernel常用的文件名为：vmlinuz，如果使用的是grub2这个开机管理程序， 则还会存在/boot/grub2/这个目录喔！ |
| /dev       | 在Linux系统上，任何设备与周边设备都是以文件的型态存在于这个目录当中的。 你只要通过存取这个目录下面的某个文件，就等于存取某个设备啰～ 比要重要的文件有/dev/null, /dev/zero, /dev/tty, /dev/loop*, /dev/sd*等等 |
| /etc       | 系统主要的配置文件几乎都放置在这个目录内，例如人员的帐号密码档、 各种服务的启始档等等。一般来说，这个目录下的各文件属性是可以让一般使用者查阅的， 但是只有root有权力修改。FHS建议不要放置可可执行文件（binary）在这个目录中喔。比较重要的文件有： /etc/modprobe.d/, /etc/passwd, /etc/fstab, /etc/issue 等等。另外 FHS 还规范几个重要的目录最好要存在 /etc/ 目录下喔：<br />/etc/opt（必要）：这个目录在放置第三方协力软件 <br />/opt 的相关配置文件<br />/etc/X11/（建议）：与 X Window 有关的各种配置文件都在这里，尤其是 xorg.conf 这个 X Server 的配置文件。<br />/etc/sgml/（建议）：与 SGML 格式有关的各项配置文件<br />/etc/xml/（建议）：与 XML 格式有关的各项配置文件 |
| /lib       | 系统的函数库非常的多，而/lib放置的则是在开机时会用到的函数库， 以及在/bin或/sbin下面的指令会调用的函数库而已。 什么是函数库呢？你可以将他想成是“外挂”，某些指令必须要有这些“外挂”才能够顺利完成程序的执行之意。 另外 FSH 还要求下面的目录必须要存在：/lib/modules/：这个目录主要放置可抽换式的核心相关模块（驱动程序）喔！ |
| /media     | media是“媒体”的英文，顾名思义，这个/media下面放置的就是可移除的设备啦！ 包括软盘、光盘、DVD等等设备都暂时挂载于此。常见的文件名有：/media/floppy, /media/cdrom等等。 |
| /mnt       | 如果你想要暂时挂载某些额外的设备，一般建议你可以放置到这个目录中。 在古早时候，这个目录的用途与/media相同啦！只是有了/media之后，这个目录就用来暂时挂载用了。 |      
| /opt       | 这个是给第三方协力软件放置的目录。什么是第三方协力软件啊？ 举例来说，KDE这个桌面管理系统是一个独立的计划，不过他可以安装到Linux系统中，因此KDE的软件就建议放置到此目录下了。 另外，如果你想要自行安装额外的软件（非原本的distribution提供的），那么也能够将你的软件安装到这里来。 不过，以前的Linux系统中，我们还是习惯放置在/usr/local目录下呢！ |
| /run       | 早期的 FHS 规定系统开机后所产生的各项信息应该要放置到 /var/run 目录下，新版的 FHS 则规范到 /run 下面。 由于 /run 可以使用内存来仿真，因此性能上会好很多！ |
| /sbin      | Linux有非常多指令是用来设置系统环境的，这些指令只有root才能够利用来“设置”系统，其他使用者最多只能用来“查询”而已。 放在/sbin下面的为开机过程中所需要的，里面包括了开机、修复、还原系统所需要的指令。 至于某些服务器软件程序，一般则放置到/usr/sbin/当中。至于本机自行安装的软件所产生的系统可执行文件（system binary）， 则放置到/usr/local/sbin/当中了。常见的指令包括：fdisk, fsck, ifconfig, mkfs等等。 |
| /srv       | srv可以视为“service”的缩写，是一些网络服务启动之后，这些服务所需要取用的数据目录。 常见的服务例如WWW, FTP等等。举例来说，WWW服务器需要的网页数据就可以放置在/srv/www/里面。 不过，系统的服务数据如果尚未要提供给网际网络任何人浏览的话，默认还是建议放置到 /var/lib 下面即可。 |
| /tmp       | 这是让一般使用者或者是正在执行的程序暂时放置文件的地方。 这个目录是任何人都能够存取的，所以你需要定期的清理一下。当然，重要数据不可放置在此目录啊！ 因为FHS甚至建议在开机时，应该要将/tmp下的数据都删除唷！ |
| /usr       | 第二层 FHS 设置，后续介绍                                    |
| /var       | 第二曾 FHS 设置，主要为放置变动性的数据，后续介绍            |
| 第二部份   | FHS 建议可以存在的目录                                       |
| /home      | 这是系统默认的使用者主文件夹（home directory）。在你新增一个一般使用者帐号时， 默认的使用者主文件夹都会规范到这里来。比较重要的是，主文件夹有两种代号喔：~：代表目前这个使用者的主文件夹~dmtsai ：则代表 dmtsai 的主文件夹！ |
| /lib<qual> | 用来存放与 /lib 不同的格式的二进制函数库，例如支持 64 位的 /lib64 函数库等 |
| /root      | 系统管理员（root）的主文件夹。之所以放在这里，是因为如果进入单人维护模式而仅挂载根目录时， 该目录就能够拥有root的主文件夹，所以我们会希望root的主文件夹与根目录放置在同一个分区中。 |

  - /usr: unix software resource, Unix操作系统软件资源, 与软件安装/执行有关；/usr里面放置的数据属于可分享的与不可变动的（shareable, static）， 如果你知道如何通过网络进行分区的挂载（例如在服务器篇会谈到的NFS服务器），那么/usr确实可以分享给区域网络内的其他主机来使用喔 因为是所有系统默认的软件（distribution发布者提供的软件）都会放置到/usr下面，因此这个目录有点类似Windows 系统的“C:\Windows\ （当中的一部份） + C:\Program files\”这两个目录的综合体，系统刚安装完毕时，这个目录会占用最多的硬盘容量。一般来说，/usr的次目录建议有下面这些：

> 早期 Linux 在设计的时候，若发生问题时，救援模式通常仅挂载根目录而已，因此有五个重要的目录被要求一定要与根目录放置在一起， 那就是 /etc, /bin, /dev, /lib, /sbin 这五个重要目录。现在许多的 Linux distributions 由于已经将许多非必要的文件移出 /usr 之外了， 所以 /usr 也是越来越精简，同时因为 /usr 被建议为“即使挂载成为只读，系统还是可以正常运行”的模样，所以救援模式也能同时挂载 /usr 喔！ 例如我们的这个 CentOS 7.x 版本在救援模式的情况下就是这样。因此那个五大目录的限制已经被打破了呦！例如 CentOS 7.x 就已经将 /sbin, /bin, /lib 通通移动到 /usr 下面了哩！

| 目录            | 应放置文件内容                                               |
| --------------- | ------------------------------------------------------------ |
| 第一部份：      | FHS 要求必须要存在的目录                                     |
| /usr/bin/       | 所有一般用户能够使用的指令都放在这里！目前新的 CentOS 7 已经将全部的使用者指令放置于此，而使用链接文件的方式将 /bin 链接至此！ 也就是说， /usr/bin 与 /bin 是一模一样了！另外，FHS 要求在此目录下不应该有子目录！ |
| /usr/lib/       | 基本上，与 /lib 功能相同，所以 /lib 就是链接到此目录中的！   |
| /usr/local/     | 系统管理员在本机自行安装自己下载的软件（非distribution默认提供者），建议安装到此目录， 这样会比较便于管理。举例来说，你的distribution提供的软件较旧，你想安装较新的软件但又不想移除旧版， 此时你可以将新版软件安装于/usr/local/目录下，可与原先的旧版软件有分别啦！ 你可以自行到/usr/local去看看，该目录下也是具有bin, etc, include, lib...的次目录喔！ |
| /usr/sbin/      | 非系统正常运行所需要的系统指令。最常见的就是某些网络服务器软件的服务指令（daemon）啰！不过基本功能与 /sbin 也差不多， 因此目前 /sbin 就是链接到此目录中的。 |
| /usr/share/     | 主要放置只读架构的数据文件，当然也包括共享文件。在这个目录下放置的数据几乎是不分硬件架构均可读取的数据， 因为几乎都是文字文件嘛！在此目录下常见的还有这些次目录：/usr/share/man：线上说明文档/usr/share/doc：软件杂项的文件说明/usr/share/zoneinfo：与时区有关的时区文件 |
| 第二部份：      | FHS 建议可以存在的目录                                       |
| /usr/games/     | 与游戏比较相关的数据放置处                                   |
| /usr/include/   | c/c++等程序语言的文件开始（header）与包含档（include）放置处，当我们以tarball方式 （*.tar.gz 的方式安装软件）安装某些数据时，会使用到里头的许多包含档喔！ |
| /usr/libexec/   | 某些不被一般使用者惯用的可执行文件或脚本（script）等等，都会放置在此目录中。例如大部分的 X 窗口下面的操作指令， 很多都是放在此目录下的。 |
| /usr/lib<qual>/ | 与 /lib<qual>/功能相同，因此目前 /lib<qual> 就是链接到此目录中 |
| /usr/src/       | 一般源代码建议放置到这里，src有source的意思。至于核心源代码则建议放置到/usr/src/linux/目录下。 |

  - /var （variable）：与系统运行过程有关。/var就是在系统运行后才会渐渐占用硬盘容量的目录。 因为/var目录主要针对常态性变动的文件，包括高速缓存（cache）、登录文件（log file）以及某些软件运行所产生的文件， 包括程序文件（lock file, run file），或者例如MySQL数据库的文件等等

| 目录        | 应放置文件内容                                               |
| ----------- | ------------------------------------------------------------ |
| 第一部份    | FHS 要求必须要存在的目录                                     |
| /var/cache/ | 应用程序本身运行过程中会产生的一些暂存盘；                   |
| /var/lib/   | 程序本身执行的过程中，需要使用到的数据文件放置的目录。在此目录下各自的软件应该要有各自的目录。 举例来说，MySQL的数据库放置到/var/lib/mysql/而rpm的数据库则放到/var/lib/rpm去！ |
| /var/lock/  | 某些设备或者是文件资源一次只能被一个应用程序所使用，如果同时有两个程序使用该设备时， 就可能产生一些错误的状况，因此就得要将该设备上锁（lock），以确保该设备只会给单一软件所使用。 举例来说，烧录机正在烧录一块光盘，你想一下，会不会有两个人同时在使用一个烧录机烧片？ 如果两个人同时烧录，那片子写入的是谁的数据？所以当第一个人在烧录时该烧录机就会被上锁， 第二个人就得要该设备被解除锁定（就是前一个人用完了）才能够继续使用啰。目前此目录也已经挪到 /run/lock 中！ |
| /var/log/   | 重要到不行！这是登录文件放置的目录！里面比较重要的文件如/var/log/messages, /var/log/wtmp（记录登陆者的信息）等。 |
| /var/mail/  | 放置个人电子邮件信箱的目录，不过这个目录也被放置到/var/spool/mail/目录中！ 通常这两个目录是互为链接文件啦！ |
| /var/run/   | 某些程序或者是服务启动后，会将他们的PID放置在这个目录下喔！至于PID的意义我们会在后续章节提到的。 与 /run 相同，这个目录链接到 /run 去了！ |
| /var/spool/ | 这个目录通常放置一些伫列数据，所谓的“伫列”就是排队等待其他程序使用的数据啦！ 这些数据被使用后通常都会被删除。举例来说，系统收到新信会放置到/var/spool/mail/中， 但使用者收下该信件后该封信原则上就会被删除。信件如果暂时寄不出去会被放到/var/spool/mqueue/中， 等到被送出后就被删除。如果是工作调度数据（crontab），就会被放置到/var/spool/cron/目录中！ |


### 权限管理

- 速记:
  - 755: 拥有者具备全部权限, 群组和其他人没有写的权限.
  - 625: 拥有者只有读写的权利, 没有执行的权利, 群组只有覆盖的权利, 无法读取和运行, 而其他人没有写的权利, 可以读取执行.
- 命令: `chown [-R] owner :group filename`
- 权限设定<sup>[7](#j7)</sup>
  - `abc`
    - a: 拥有者
    - b: 所属群组
    - c: 其他人
  - 表示方法:
    - 数字法: 用权限值表示.
      - r权限＋4
      - w权限＋2
      - x权限＋1
    - 符号法: `人＋动作（+加入-除去=设定）＋权限符号（rwx）`; 不同动作间用“,”分隔
      - u拥有者
      - g群组
      - o其他人
      - a所有人
- 意义
  - 文件：
    - r：读内容
    - w：写内容 (无法删除), 若无r权限, 新写入的内容将覆盖原来的内容
    - x：被系统执行，蕴含r权限。
  - 目录：
    - r：读取目录结构清单的权限，也就是查询该目录下的文件名
    - w：修改该目录结构清单的权限
    - x：进入该目录，访问目录下的文件

## UNINSTALL UBUNTU

用的不习惯当然要卸载了, 卸载比较简单, 如果安装无误的话, 启动引导用的是Ubuntu自带的的 `GUN GRUB`, 如果你分盘的时候没有选择下面的启动引导设置, 那么你第一次启动的时候一定不会进入Ubuntu的系统. 所以要卸载Ubuntu, 我们可以直接用 `EasyUEFI` 把 `GUN GRUB` 干掉, 然后选择磁盘分区的删除卷即可. , 软件的话, 用, 官网下载的话需要梯子, 然后我这里如果有时间会给出下载链接, 去网上随便下载一个就好了

## LINK

- [Debain](http://www.debian.org/)
- [Ubuntu](http://www.ubuntu.com/) 
- [Wiki_Ubuntu_En](http://wiki.ubuntu.com/)
- [写给工程师的 Ubuntu 20.04 最佳配置指南](https://juejin.cn/post/6844904149822210056)

### *NIX SITES

- [ubutntu_launchpad](https://launchpad.net/ubuntu)
- [linux_forum](https://linustechtips.com)
- [cn-wiki ubuntu](https://wiki.ubuntu.org.cn/%E9%A6%96%E9%A1%B5) 
- [lulinux](//linux.zone/)
- [linux_cn](https://linux.cn/)
- [linux dir](https://www.linuxidc.com/)
- [linux ywnz](https://ywnz.com/)
- [linux_hint](https://linuxhint.com/)
- [linux_probe](https://www.linuxprobe.com)

### Tools

- [Linux Command Search](https://wangchujiang.com/linux-command/)
- [Mirrors Linux](http://mirrors.kernel.org/)

### Guidences

- [ubuntu常见问题指南 新手发问前必看](https://forum.ubuntu.org.cn/viewtopic.php?f=120&t=35100&sid=dedd568ab12c1f6937889c57562b7476)
- [ubuntu安装好之后, 怎样再重新分区？](https://forum.ubuntu.org.cn/viewtopic.php?t=105237#p628762)
- [ubuntu系统重新分区、根目录扩容](https://blog.csdn.net/code_segment/article/details/79237500)

![](https://z3.ax1x.com/2021/06/28/RNt0kn.png)

<div id="j1">[1]. </div>
<div id="j2">[2]. https://zhuanlan.zhihu.com/p/40434062</div>
<div id="j3">[3]. https://www.jianshu.com/p/99d3eebcf17f</div>
<div id="j4">[4]. https://blog.csdn.net/gatieme/article/details/52829907</div>
<div id="j5">[5]. https://blog.csdn.net/u010648555/article/details/88542150</div>
<div id="j6">[6]. </div>
<div id="j7">[7]. https://blog.csdn.net/dangpu/article/details/41597749</div>
<div id="j8">[8]. https://askubuntu.com/questions/722708/how-do-i-refresh-the-icon-cache</div>
<div id="j9">[9]. http://bbs.chinaunix.net/thread-1979347-1-1.html</div>
<div id="j10">[10]. https://bbs.huaweicloud.com/forum/thread-62703-1-1.html</div>



I’ve been following the development of RxJS over the last few months. It’s exciting to see how the library evolves. So seeing the [release](https://github.com/ReactiveX/rxjs/blob/master/CHANGELOG.md#640-2019-01-30) of this new version made me curious to see what’s new.

In this short post I’d like to share a small improvement that was made to the [`range`](https://rxjs.dev/api/index/function/range) function.

If you’ve used the `range` function before, you know that you have to pass two arguments in order to create an Observable that emits a sequence of numbers.

Here’s a quick refresh on how it works ([StackBlitz](https://stackblitz.com/edit/range-two-arguments?devtoolsheight=60)):

```ts
import { range } from 'rxjs';

const numbers = range(0, 5);
numbers.subscribe(x => console.log(x));

// Output:
// 0
// 1
// 2
// 3
// 4
```

Now, here’s the new part.

As of v6.4.0, the `range` function can also accept only one argument. In this case, the range will start from zero and will emit until it reaches the specified number.

So the above example can be shorten like this ([StackBlitz](https://stackblitz.com/edit/range-one-argument?devtoolsheight=60)):

```ts
import { range } from 'rxjs';

const numbers = range(5);
numbers.subscribe(x => console.log(x));

// Output:
// 0
// 1
// 2
// 3
// 4
```

So there it is. A small improvement that makes it a bit easier to create a range of numbers.
