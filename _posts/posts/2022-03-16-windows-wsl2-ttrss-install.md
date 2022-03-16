---
layout: post
title: 本地(WSL2) TTRSS 搭建
updated: 2019-12-13
category: posts
---

> Q: 为什么不用在线服务?

之前一直配合 Vivaldi 的 Panel 用 [蚁阅](https://rss.anyant.com), 大概有半年的时间, Star 了 600 多篇文章, 但是一来没有导出功能, 二来没有一键 Unstar 的功能, 最后自己用 Github Action 摸🐟了一个每周备份收藏并清空收藏夹的小脚本, 详见 https://github.com/bGZo/rss/blob/main/anyant-backup.py. 原理很简单, 最有趣的地方就是抓包测 API 了😁

> Q: 为什么不用服务器? NAS? 软路由?

说到底还不是因为穷, 尽量开源节流, 也避免了国内备案, 服务商的选择难和很多不必要的麻烦. 说要用服务器练手的, 先自己吧 \*nix 玩转了再说吧😅, 家里面虽然有一台 老毛子(padavan) 的硬路由, 但128G的内存放弃🙃

> Q: 为什么不用现成的软件? 像是 [FluentRss](https://github.com/yang991178/fluent-reader) 多么优雅

软件挂后台是个麻烦(眼不见心不烦?), 软件多多少少有点 bug, 曾一度重度使用, 但是阅读体验不太适合我. 当然软件也有提供 TTRSS 后台服务, 不行就套壳嘛😅

## How?  

起初使用 `WSL2` 搭建了两个容器, 但是每次启动的时候要启动两次(顺序), 就上了 `docker-compose`, 因为抽象程度有点高一直有种空中楼阁的感觉, 所以今天尝试挂载备份了数据, 移植到 `windows` 后发现 `WSL2` 内存占用更高了(现大约3G左右, 对比之前的2G真是😅), 除此之外, 利用了 `WSL2` 的容器在 `windows` 下, 依旧没有办法使用 `proxy`, 这就受不了了, 因为你懂得😁. RSS 源国内可拉不下来得😏.

总体来说今天一天探索下来路径只有两个

- 在 `WSL2` 内搭建, 需要解决 双向 IP 交换 ( `WSL` 和 `Windows` 相互知道彼此IP), 动态虚拟 IP(`WSL2`) 和 端口转发三个问题
- 不依赖 `WSL2` 的 `Windows Docker`. 至少代理和内存占用目测要好一些.
- 依赖 `WSL2` 的 `Windows Docker`
  - 针对于 Win10 容器代理无法使用系统代理我还没有搞清楚, 这个问题之前就存在(via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working)), 我是用的是 `--env `+ `env file` 部署方式, 用的时候报错 `docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused`, 以为是代理没写对又写了 `WSL2` 的 IP 依旧无用, 个人认为是连不上 `WSL` 端口, 还需要做一次端口转发, 所以放弃了😁. 两头复杂都一样欸.

搭建过程不造轮子了, 参考下面两个教程就够用了.

- [Awesome-TTRSS · HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docs/zh/README.md )
- [Tiny Tiny RSS：最速部署私有 RSS 服务器 - Spencer's Blog](https://spencerwoo.com/blog/tiny-tiny-rss#an-zhuang-docker-compose )

搭建过程中遇到的的 动态IP 以及 端口转发 已经被我简化成了 `powershell` 的 `profile`了, 需要的朋友可以配合第二个需要在 `WSL2` 执行的脚本配合使用. 脚本因机器环境而异, 仅供参考. 

```shell
function Output-Lan-Ip-Bin ($cmdletname) {
    $Lan_Ip = ipconfig | findstr /i "ipv4" | select-object -Skip 1 | select-object -First 1 | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | % { $($_.matches.groups[1]).Value} 
    # get the second line IP
    
    echo "URL_PATH=$Lan_Ip" > C:\Users\usr\bin\lan_ip
    # output sharing Lan IP path

    echo "Output PC Lan Successfully."
}

function Netsh-Lan ($cmdletname) {
    $tmp=cat C:\Users\usr\bin\wsl_ip
    # get sharing IP

    sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=$tmp protocol=tcp
    echo "Port Forward Set Successfully."
    # port forward

    netsh interface portproxy show all
}


Output-Lan-Ip-Bin
wsl /mnt/c/Users/usr/bin/wsl-ip.sh

#via https://docs.docker.com/compose/compose-file/compose-file-v2/
wsl docker-compose -f /home/xxx/ttrss/docker-compose.yml --env  /home/xxx/ttrss/.env up -d

Netsh-Lan
```

```shell
#!/bin/sh
# author: bGZo
# update: 220316

# set env
host_ip=$(cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " ")
echo "HTTP_PROXY=$host_ip" > /home/bgzocg/ttrss/.env
cat /mnt/c/Users/15517/bin/lan_ip >> /home/bgzocg/ttrss/.env

# output shring IP
ip addr show eth0 | grep 'inet ' | cut -f 6 -d ' ' | cut -f 1 -d '/' > /mnt/c/Users/usr/bin/wsl_ip

echo "run successful."
```

- 运行之前记得先把 `WSL2` 的 Docker 服务打开: `sudo dockerd.`

当然也[有朋友](https://www.zhihu.com/question/387747506/answer/1820473311)之间用 `Hosts` 映射 `WSL2` 也是可以, 但只能在本机调试的时候用一下, 你如果手机也想看一下怎么办?😅
