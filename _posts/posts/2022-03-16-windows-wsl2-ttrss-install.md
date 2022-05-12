---
layout: post
title: TTRSS in WSL2
updated: 2022-05-12
category: posts
---

Keywords: `docker` / `wsl2` / `port forward`

## Some Points Noticed.

- WSL2 docker start method.
- Deploy container with proxy.
  - Communication IP between WSL2 & Windows.
- Under LAN accessing TTRSS(WSL2) cross the Windows IP.

## WSL2 Start Mothod

```shell
sudo dockerd
# sudo systemctl enable docker ????
```

## Deploy TTRSS with Proxy 🤯

部署 TTRSS 的部分可以参考这些博客, 他们写的都比我耐心和详细, 这里我就不讲废话了.

- Offical Doc: [Awesome-TTRSS HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docs/zh/README.md )
- Nice Blog: [Tiny Tiny RSS：最速部署私有 RSS 服务器 - Spencer's Blog](https://spencerwoo.com/blog/tiny-tiny-rss#an-zhuang-docker-compose )

部署的命令可能稍有不同:

```shell
docker-compose up -d --env .env
# docker-compose stop
# docker-compose down
# --env         environment setting using .env file
# -d            detached mode
$cat .env
HTTP_PROXY=172.29.160.1
URL_PATH=192.168.2.2
# HTTP_PROXY    proxy ip(windows' ip in wsl2)
# URL_PATH      lan ip
```

### Communication IP

`docker-compose.yml` 配置文件需要注意这几行, `HTTP_PROXY` 只有写在配置文件中才会生效, 然而命令行传参也不可行, 所以只能用另一个文件 `.env` 传值.

```diff
    ports:
      - 4040:80
    environment:
!     - SELF_URL_PATH=http://${URL_PATH}:4040 # please change to your own domain
!     - HTTP_PROXY=http://${HTTP_PROXY}:7890
```

部署的时候因为用到了两个不确定的 IP, 而 WSL2 IP 无法[固定](https://github.com/microsoft/WSL/issues/4210), 当然后者可以通过路由器的静态IP分配解决, 而针对 WSL2 解决静态IP的场景有很多解决方案, 如:

- windows hosts 映射, 每次启动向 hosts 文件追加一条映射(via: [zhihu](https://www.zhihu.com/question/387747506/answer/1820473311)). 就可以固定一条预设的域名访问 WSL2. 但是 Lan 问题怎么解决? 而且这条 hosts 日渐增多还会有安全隐患.
- 文件传递, 我挑了两个文件分别存 `windows` / `wsl` 的两个IP, 这样两者就都能拿到各自的 IP 了.
  - `C:\Users\15517\bin\lan_ip`
    - ```powershell
      netsh interface ip show address "WLAN" | findstr "IP Address" | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | %{ $_.matches.Value }
      ```
  - `C:\Users\15517\bin\wsl_ip`
    - ```shell
      cat /etc/resolv.conf |grep "nameserver" |cut -f 2 -d " " # or using
      ip addr show eth0 | grep 'inet ' | cut -f 6 -d ' ' | cut -f 1 -d '/'
      ```

## Lan Device Access

因为 WSL2 的特殊原因, 局域网访问设备需要主机 (Windows) 将 WSL2 的特定端口暴露出去, 映射到 windows 上.

```powershell
sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=xxx.xxx.xxx.xxx protocol=tcp
netsh interface portproxy show all
```

至此所有的坑就踩完了, 都是些简单的命令堆砌, 大多是解决使用 WSL2 这个特性所需要付出的代价罢了

## Windows Docker Comparison

另外, 博主还对比了 windows docker 利用 WSL2 虚拟化托管 TTRSS, 发现系统占用不如直接用 WSL2 来的轻便, 具体体验是

- windows + wsl2 => mem 3G
- wsl2 => 2G

当然, 除了内存占用更多之外, 配置代理更是无从下手, 上文的配置文件失效 + GUI 界面配置也失败了, 总是找不准代理的地址, 猜测是叠上 WSL2 的 Buff, 无法简单的通过 `127.0.0.1:7890` 来解决... 这个问题可能真的无解, via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working), 报错如下, 希望知道的大佬可以指点一二.

```shell
docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused
```

![](https://user-images.githubusercontent.com/57313137/158712544-96fcd594-7628-41e8-a906-acdc672d5e22.png)
![](https://user-images.githubusercontent.com/57313137/158712547-68a408d5-a46d-42ec-ab6b-35f1f8a3af55.png)

也许还要做一次端口转发, 复杂度两者都快一样了, 所以最后放弃了😁...

## Backup Your Data

当然中途换到 windows 做过一次数据迁移. 尝试挂载备份了数据, 移植到 `windows`, 其实最重要的就是一个 `.sql` 文件, 其他都可以丢弃.

```shell
$ docker run --rm --volumes-from a5b8c5847c8d -v /home/bgzocg/ttrss/backup:/backup ubuntu tar cvfP /backup/backup.tar /var/lib/postgresql/data/
```

via: [🎯 备份和迁移数据 - Docker 快速入门 - 易文档](https://docker.easydoc.net/doc/81170005/cCewZWoN/XQEqNjiu )


## Finally

使用如下, 仅供参考 (脚本因机器环境而异, `windows` 用户名 15517 和 `wsl2` 用户名 `bgzocg`, `proxy` 端口 `7890`, `ttrss` 端口 `4040`).

![image](https://user-images.githubusercontent.com/57313137/158714518-c1dd51d1-c3b1-4b1d-b3dc-ac448e4dbebd.png)

`C:\Users\15517\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`

```powershell
function Output-Lan-Ip-Bin {
    $Lan_Ip = netsh interface ip show address "WLAN" | findstr "IP Address" | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | %{ $_.matches.Value }
    #ipconfig | findstr /i "ipv4" | select-object -Skip 1 | select-object -First 1 | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | % { $($_.matches.groups[1]).Value}
    # NOTES: get the second line IP. I have three IPs, you could modify
    # select-object -Skip 1 | select-object -First 1
    # to fit your machine. :)

    echo "URL_PATH=$Lan_Ip" > C:\Users\15517\bin\lan_ip
    # output sharing Lan IP path

    echo "Your Server: http://${Lan_Ip}:4040"
    echo "Output PC Lan IP Successfully."
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

`C:\Users\15517\bin\wsl-ip.sh`

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

echo "Output WSL2 IP And Set Proxy Successfully."
```

<!-- 
$ docker run -d --name ttrssdb nornagon/postgres
$ docker run -d --link ttrssdb:db -p <port>:80 -e SELF_URL_PATH=http://<ttrss_domain>:<port> fischerman/docker-ttrss

从 Google Reader 倒闭的十年间 RSS 这种落后的摘要模式竟成为当代抵御信息轰炸的最优方式, What a Joke? 😏 虽然无法抵御信息的半衰期, 但将文字直接无差别地分发给每个订阅个体正可符合当下这个去全球化, 个性化的世界趋势, 可能几十年之后就消失在互联网上的微不足道的信息(未被快照留存, 未在 archive.org 等存档馆), 在你的 RSS 阅读器的数据库中就有一份, 饱受陆内 `404 NotFound` 的大家一定能体会这种失而复得的感觉吧. Awesome!!!

好的, 这已经是个被陆内媒体写烂了的话题, 

> Q: 为什么不用在线服务?

之前一直配合 `Vivaldi` 的 `Panel` 使用 [蚁阅](https://rss.anyant.com), 大概有半年的时间了, Star 了 600+ 篇文章, 越来越用得不舒服, 一来没有导出功能, 二来没有一键 Unstar 的功能, 最后自己用 Github Action 摸🐟了一个每周备份收藏并清空收藏夹的[小脚本](https://github.com/bGZo/rss/blob/main/anyant-backup.py). 原理很简单, 最有趣的地方就是抓包测 API 了😁

> Q: 为什么不用服务器? `NAS`? 软路由?

说到底还不是因为穷, 尽量开源节流, 也躲掉了国内备案, 选择服务商和很多不必要的麻烦. 说要用服务器练手的, 先自己把 `*nix` 玩转了再说吧😅, 家里面虽然有一台 老毛子(padavan) 的硬路由, 但迫于 `128G` 的内存选择放弃🙃

> Q: 为什么不用现成的软件? 像是 [FluentRss](https://github.com/yang991178/fluent-reader) 多么优雅

数据保存, 部分 RSS 不会输出全站内容, 个人考虑想尽早储存; 迁移难度, `docker` 迁移到更成熟的 软路由/`NAS` 更为灵活; [FluentRss](https://github.com/yang991178/fluent-reader) 定制化较少, 不喜欢其阅读体验, 当然软件也有提供 TTRSS 后台服务, 不行就套壳嘛😅


-->
