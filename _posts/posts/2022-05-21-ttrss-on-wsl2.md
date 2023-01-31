---
layout: post
title: TTRSS on WSL2
updated: 2022-07-31
category: posts
comment_link: <https://github.com/bGZo/blog/issues/3>
---

Keywords: `docker` / `wsl2` / `port forward`

## Some Points Noticed.

- WSL2 docker start method.
- Deploy container with proxy.
  - Communication IP between WSL2 & Windows.
- Under LAN accessing TTRSS(WSL2) cross the Windows IP.

## WSL2 Start Mothod

```shell
# Error Way:
$systemctl start docker.service
# System has not been booted with systemd as init system (PID 1). Can't operate.
# Failed to connect to bus: Host is down

# Right Way: (via: <https://stackoverflow.com/questions/52197246/wsl-redis-encountered-system-has-not-been-booted-with-systemd-as-init-system-pi>
$sudo dockerd
$sudo service docker start
$sudo /etc/init.d/docker start
```

## Deploy TTRSS with Proxy 🤯

部署 TTRSS 的部分可以参考这些博客，他们写的都比我耐心和详细，这里我就不讲废话了.

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

`docker-compose.yml` 配置文件需要注意这几行, `HTTP_PROXY` 只有写在配置文件中才会生效，然而命令行传参也不可行，所以只能用另一个文件 `.env` 传值.

```diff
    ports:
      - 4040:80
    environment:
!     - SELF_URL_PATH=http://${URL_PATH}:4040 # please change to your own domain
!     - HTTP_PROXY=http://${HTTP_PROXY}:7890
```

部署的时候因为用到了两个不确定的 IP, 而 WSL2 IP 无法[固定](https://github.com/microsoft/WSL/issues/4210), 当然后者可以通过路由器的静态IP分配解决，而针对 WSL2 解决静态IP的场景有很多解决方案，如:

- windows hosts 映射，每次启动向 hosts 文件追加一条映射(via: [zhihu](https://www.zhihu.com/question/387747506/answer/1820473311)). 就可以固定一条预设的域名访问 WSL2. 但是 Lan 问题怎么解决。而且这条 hosts 日渐增多还会有安全隐患.
- 文件传递，我挑了两个文件分别存 `windows` / `wsl` 的两个IP, 这样两者就都能拿到各自的 IP 了.
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

因为 WSL2 的特殊原因，局域网访问设备需要主机 (Windows) 将 WSL2 的特定端口暴露出去，映射到 windows 上.

```powershell
sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=xxx.xxx.xxx.xxx protocol=tcp
netsh interface portproxy show all
```

至此所有的坑就踩完了，都是些简单的命令堆砌，大多是解决使用 WSL2 这个特性所需要付出的代价罢了

## Windows Docker Comparison

另外，博主还对比了 windows docker 利用 WSL2 虚拟化托管 TTRSS, 发现系统占用不如直接用 WSL2 来的轻便，具体体验是

- windows + wsl2 => mem 3G
- wsl2 => 2G

当然，除了内存占用更多之外，配置代理更是无从下手，上文的配置文件失效 + GUI 界面配置也失败了，总是找不准代理的地址，猜测是叠上 WSL2 的 Buff, 无法简单的通过 `127.0.0.1:7890` 来解决... 这个问题可能真的无解, via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working), 报错如下，希望知道的大佬可以指点一二.

```shell
docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused
```

![](https://user-images.githubusercontent.com/57313137/158712544-96fcd594-7628-41e8-a906-acdc672d5e22.png)
![](https://user-images.githubusercontent.com/57313137/158712547-68a408d5-a46d-42ec-ab6b-35f1f8a3af55.png)

也许还要做一次端口转发，复杂度两者都快一样了，所以最后放弃了😁...

## Backup Your Data

当然中途换到 windows 做过一次数据迁移。尝试挂载备份了数据，移植到 `windows`, 其实最重要的就是一个 `.sql` 文件，其他都可以丢弃.

```shell
$ docker run --rm --volumes-from a5b8c5847c8d -v /home/bgzocg/ttrss/backup:/backup ubuntu tar cvfP /backup/backup.tar /var/lib/postgresql/data/
```

via: [🎯 备份和迁移数据 - Docker 快速入门 - 易文档](https://docker.easydoc.net/doc/81170005/cCewZWoN/XQEqNjiu )


## Finally

使用如下，仅供参考 (脚本因机器环境而异, `windows` 用户名 15517 和 `wsl2` 用户名 `bgzocg`, `proxy` 端口 `7890`, `ttrss` 端口 `4040`).

![image](https://user-images.githubusercontent.com/57313137/170861898-bfed1062-dbd2-478d-87aa-86591a270061.png)

`C:\Users\15517\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` 

```powershell
function Output-Lan-Ip-Bin {
    $Lan_Ip = netsh interface ip show address "WLAN" | findstr "IP Address" | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' | %{ $_.matches.Value }
    #ipconfig | findstr /i "ipv4" | select-object -Skip 1 | select-object -First 1 | Select-String -Pattern '([0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*\.[0-9][0-9]*)' - % { $($_.matches.groups[^1]).Value}
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

    wsl sudo service docker start

    #via <https://docs.docker.com/compose/compose-file/compose-file-v2/>
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