---
layout: post
title: 本地(wsl2) TTRSS 搭建
updated: 2019-12-13
category: posts
---

> Q: 为什么不用在线服务?

之前一直配合 `Vivaldi` 的 `Panel` 使用 [蚁阅](https://rss.anyant.com), 大概有半年的时间了, Star 了 600+ 篇文章, 越来越用得不舒服, 一来没有导出功能, 二来没有一键 Unstar 的功能, 最后自己用 Github Action 摸🐟了一个每周备份收藏并清空收藏夹的[小脚本](https://github.com/bGZo/rss/blob/main/anyant-backup.py). 原理很简单, 最有趣的地方就是抓包测 API 了😁

> Q: 为什么不用服务器? `NAS`? 软路由?

说到底还不是因为穷, 尽量开源节流, 也躲掉了国内备案, 选择服务商和很多不必要的麻烦. 说要用服务器练手的, 先自己把 `*nix` 玩转了再说吧😅, 家里面虽然有一台 老毛子(padavan) 的硬路由, 但迫于 `128G` 的内存选择放弃🙃

> Q: 为什么不用现成的软件? 像是 [FluentRss](https://github.com/yang991178/fluent-reader) 多么优雅

数据保存, 部分 RSS 不会输出全站内容, 个人考虑想尽早储存; 迁移难度, `docker` 迁移到更成熟的 软路由/`NAS` 更为灵活; [FluentRss](https://github.com/yang991178/fluent-reader) 定制化较少, 不喜欢其阅读体验, 当然软件也有提供 TTRSS 后台服务, 不行就套壳嘛😅

## Deploy

简单说一下 `windows` 部署思路和难点:

- ✔ `wsl2` 内搭建
  - 双向 IP 交换 ( `WSL`(动态虚拟 `IP`) <====互通===> `Windows`)
  - 端口转发
- ❌ `windows docker`
  - 依赖 `wsl2`
    - 容器代理
    - 内存占用等同于直接使用 `wsl2` 搭建.
  - 不依赖 `wsl2`
    -  代理应该比 `wsl2` 要好一些, 未测试🐟

### In Wsl2

搭建过程不造轮子了, 参考下面两个教程就够用了.

- [Awesome-TTRSS · HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docs/zh/README.md )
- [Tiny Tiny RSS：最速部署私有 RSS 服务器 - Spencer's Blog](https://spencerwoo.com/blog/tiny-tiny-rss#an-zhuang-docker-compose )

搭建过程中遇到的的 动态IP 以及 端口转发 已经被我简化成了 `powershell` 的 `profile`了, 需要的朋友可以配合第二个需要在 `wsl2` 执行的脚本配合使用. 脚本因机器环境而异, 我 `windows` 用户名 15517 和 `wsl2` 用户名 `bgzocg`, 使用如下, 仅供参考.

![WindowsTerminal_1ibNbTPfwq](https://user-images.githubusercontent.com/57313137/158712463-0f350cb8-e83b-41cf-a90b-6fa5a93b0113.png)

```shell
function Output-Lan-Ip-Bin {
    $Lan_Ip = ipconfig | findstr /i "ipv4" | select-object -Skip 1 | select-object -First 1 | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | % { $($_.matches.groups[1]).Value}
    # get the second line IP

    echo "URL_PATH=$Lan_Ip" > C:\Users\15517\bin\lan_ip
    # output sharing Lan IP path

    echo "Output PC Lan Successfully."
}

function Netsh-Lan {
    $tmp=cat C:\Users\15517\bin\wsl_ip
    # get sharing IP

    sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=$tmp protocol=tcp
    echo "Port Forward Set Successfully."
    # port forward

    netsh interface portproxy show all
}

function Start-TTRSS { # main
    Output-Lan-Ip-Bin
    wsl /mnt/c/Users/15517/bin/wsl-ip.sh

    #via https://docs.docker.com/compose/compose-file/compose-file-v2/
    wsl docker-compose -f /home/bgzocg/ttrss/docker-compose.yml --env /home/bgzocg/ttrss/.env up -d

    Netsh-Lan
}
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
ip addr show eth0 | grep 'inet ' | cut -f 6 -d ' ' | cut -f 1 -d '/' > /mnt/c/Users/15517/bin/wsl_ip

echo "run successful."
```

- 运行之前记得先把 `wsl2` 的 Docker 服务打开: `sudo dockerd.`

当然也[有朋友](https://www.zhihu.com/question/387747506/answer/1820473311)之间用 `Hosts` 映射 `wsl2` 也是可以, 但只能在本机调试的时候用一下, 你如果手机也想看一下怎么办?😅

### In Windows

起初使用 `wsl2` 搭建了两个容器

```shell
$ docker run -d --name ttrssdb nornagon/postgres
$ docker run -d --link ttrssdb:db -p <port>:80 -e SELF_URL_PATH=http://<ttrss_domain>:<port> fischerman/docker-ttrss
```

但每次启动的时候要启动两次(顺序), 就同上了 `docker-compose`

```shell
$ sudo docker-compose up -d
$ sudo docker-compose stop
$ sudo docker-compose down
```

明显抽象程度高了一个 level, 使用过程中一直有种空中楼阁的感觉, 所以尝试挂载备份了数据, 移植到 `windows`

```shell
$ docker run --rm --volumes-from a5b8c5847c8d -v /home/bgzocg/ttrss/backup:/backup ubuntu tar cvfP /backup/backup.tar /var/lib/postgresql/data/
```

发现 `wsl2` 内存占用更高了(现大约3G左右, 对比之前的2G真是😅), 除此之外, 利用了 `wsl2` 的容器在 `windows` 下, 依旧没有办法使用 `proxy`, 这就受不了了, 因为你懂得😁. RSS 源国内可拉不下来得😏. 解决方案未知, 这个问题之前就存在(via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working))

我目前使用使用的是 `--env `+ `env file` 部署方式报错

```shell
docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused
```

<img src="https://user-images.githubusercontent.com/57313137/158712544-96fcd594-7628-41e8-a906-acdc672d5e22.png" width=45%><img src="https://user-images.githubusercontent.com/57313137/158712547-68a408d5-a46d-42ec-ab6b-35f1f8a3af55.png" width=45%>

测试了 `wsl2` 和 `windows` 的 `IP` 依旧无用, 个人认为是连不上 `WSL` 端口, 还需要做一次端口转发, 遂放弃了😁. 两头复杂都一样欸.

## More References

- [🎯 备份和迁移数据 - Docker 快速入门 - 易文档](https://docker.easydoc.net/doc/81170005/cCewZWoN/XQEqNjiu )
