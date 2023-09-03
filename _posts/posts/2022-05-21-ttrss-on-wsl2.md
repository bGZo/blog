---
layout: post
title: TTRSS on WSL2
updated: 2023-04-08
category: posts
source: https://github.com/bGZo/blog/issues/3
number: 3
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

# Right Way: (via: https://stackoverflow.com/questions/52197246/wsl-redis-encountered-system-has-not-been-booted-with-systemd-as-init-system-pi
$sudo dockerd
$sudo service docker start
$sudo /etc/init.d/docker start
```

## Deploy TTRSS with Proxy 🤯

部署 TTRSS 的部分可以參考這些博客，他們寫的都比我耐心和詳細，這裏我就不講廢話了.

- Offical Doc: [Awesome-TTRSS HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docs/zh/README.md )
- Nice Blog: [Tiny Tiny RSS：最速部署私有 RSS 服務器 - Spencer's Blog](https://spencerwoo.com/blog/tiny-tiny-rss#an-zhuang-docker-compose )

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

`docker-compose.yml` 配置文件需要注意這幾行, `HTTP_PROXY` 只有寫在配置文件中才會生效，然而命令行傳參也不可行，所以只能用另一個文件 `.env` 傳值.

```diff
    ports:
      - 4040:80
    environment:
!     - SELF_URL_PATH=http://${URL_PATH}:4040 # please change to your own domain
!     - HTTP_PROXY=http://${HTTP_PROXY}:7890
```

部署的時候因爲用到了兩個不確定的 IP, 而 WSL2 IP 無法[固定](https://github.com/microsoft/WSL/issues/4210), 當然後者可以通過路由器的靜態IP分配解決，而針對 WSL2 解決靜態IP的場景有很多解決方案，如:

- windows hosts 映射，每次啓動向 hosts 文件追加一條映射(via: [zhihu](https://www.zhihu.com/question/387747506/answer/1820473311)). 就可以固定一條預設的域名訪問 WSL2. 但是 Lan 問題怎麼解決? 而且這條 hosts 日漸增多還會有安全隱患.
- 文件傳遞，我挑了兩個文件分別存 `windows` / `wsl` 的兩個IP, 這樣兩者就都能拿到各自的 IP 了.
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

因爲 WSL2 的特殊原因，局域網訪問設備需要主機 (Windows) 將 WSL2 的特定端口暴露出去，映射到 windows 上.

```powershell
sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=xxx.xxx.xxx.xxx protocol=tcp
netsh interface portproxy show all
```

至此所有的坑就踩完了，都是些簡單的命令堆砌，大多是解決使用 WSL2 這個特性所需要付出的代價罷了

## Windows Docker Comparison

另外，博主還對比了 windows docker 利用 WSL2 虛擬化託管 TTRSS, 發現系統佔用不如直接用 WSL2 來的輕便，具體體驗是

- windows + wsl2 => mem 3G
- wsl2 => 2G

當然，除了內存佔用更多之外，配置代理更是無從下手，上文的配置文件失效 + GUI 界面配置也失敗了，總是找不準代理的地址，猜測是疊上 WSL2 的 Buff, 無法簡單的通過 `127.0.0.1:7890` 來解決... 這個問題可能真的無解, via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working), 報錯如下，希望知道的大佬可以指點一二.

```shell
docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused
```

![](https://user-images.githubusercontent.com/57313137/158712544-96fcd594-7628-41e8-a906-acdc672d5e22.png)
![](https://user-images.githubusercontent.com/57313137/158712547-68a408d5-a46d-42ec-ab6b-35f1f8a3af55.png)

也許還要做一次端口轉發，複雜度兩者都快一樣了，所以最後放棄了😁...

## Backup Your Data

當然中途換到 windows 做過一次數據遷移。嘗試掛載備份了數據，移植到 `windows`, 其實最重要的就是一個 `.sql` 文件，其他都可以丟棄.

```shell
$ docker run --rm --volumes-from a5b8c5847c8d -v /home/bgzocg/ttrss/backup:/backup ubuntu tar cvfP /backup/backup.tar /var/lib/postgresql/data/
```

via: [🎯 備份和遷移數據 - Docker 快速入門 - 易文檔](https://docker.easydoc.net/doc/81170005/cCewZWoN/XQEqNjiu )


## Finally

使用如下，僅供參考 (腳本因機器環境而異, `windows` 用戶名 15517 和 `wsl2` 用戶名 `bgzocg`, `proxy` 端口 `7890`, `ttrss` 端口 `4040`).

![image](https://user-images.githubusercontent.com/57313137/170861898-bfed1062-dbd2-478d-87aa-86591a270061.png)

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

    wsl sudo service docker start

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