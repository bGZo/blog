---
layout: post
title: TTRSS on WSL2
updated: 2022-05-29
category: posts
comment_link: https://github.com/bGZo/blog/issues/3
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

## Deploy TTRSS with Proxy ð¤¯

é¨ç½² TTRSS çé¨åå¯ä»¥åèè¿äºåå®¢, ä»ä»¬åçé½æ¯æèå¿åè¯¦ç», è¿éæå°±ä¸è®²åºè¯äº.

- Offical Doc: [Awesome-TTRSS HenryQW/Awesome-TTRSS](https://github.com/HenryQW/Awesome-TTRSS/blob/main/docs/zh/README.md )
- Nice Blog: [Tiny Tiny RSSï¼æéé¨ç½²ç§æ RSS æå¡å¨ - Spencer's Blog](https://spencerwoo.com/blog/tiny-tiny-rss#an-zhuang-docker-compose )

é¨ç½²çå½ä»¤å¯è½ç¨æä¸å:

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

`docker-compose.yml` éç½®æä»¶éè¦æ³¨æè¿å è¡, `HTTP_PROXY` åªæåå¨éç½®æä»¶ä¸­æä¼çæ, ç¶èå½ä»¤è¡ä¼ åä¹ä¸å¯è¡, æä»¥åªè½ç¨å¦ä¸ä¸ªæä»¶ `.env` ä¼ å¼.

```diff
    ports:
      - 4040:80
    environment:
!     - SELF_URL_PATH=http://${URL_PATH}:4040 # please change to your own domain
!     - HTTP_PROXY=http://${HTTP_PROXY}:7890
```

é¨ç½²çæ¶åå ä¸ºç¨å°äºä¸¤ä¸ªä¸ç¡®å®ç IP, è WSL2 IP æ æ³[åºå®](https://github.com/microsoft/WSL/issues/4210), å½ç¶åèå¯ä»¥éè¿è·¯ç±å¨çéæIPåéè§£å³, èéå¯¹ WSL2 è§£å³éæIPçåºæ¯æå¾å¤è§£å³æ¹æ¡, å¦:

- windows hosts æ å°, æ¯æ¬¡å¯å¨å hosts æä»¶è¿½å ä¸æ¡æ å°(via: [zhihu](https://www.zhihu.com/question/387747506/answer/1820473311)). å°±å¯ä»¥åºå®ä¸æ¡é¢è®¾çååè®¿é® WSL2. ä½æ¯ Lan é®é¢æä¹è§£å³? èä¸è¿æ¡ hosts æ¥æ¸å¢å¤è¿ä¼æå®å¨éæ£.
- æä»¶ä¼ é, ææäºä¸¤ä¸ªæä»¶åå«å­ `windows` / `wsl` çä¸¤ä¸ªIP, è¿æ ·ä¸¤èå°±é½è½æ¿å°åèªç IP äº.
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

å ä¸º WSL2 çç¹æ®åå , å±åç½è®¿é®è®¾å¤éè¦ä¸»æº (Windows) å° WSL2 çç¹å®ç«¯å£æ´é²åºå», æ å°å° windows ä¸.

```powershell
sudo netsh interface portproxy add v4tov4 listenport=4040 listenaddress=* connectport=4040 connectaddress=xxx.xxx.xxx.xxx protocol=tcp
netsh interface portproxy show all
```

è³æ­¤ææçåå°±è¸©å®äº, é½æ¯äºç®åçå½ä»¤å ç , å¤§å¤æ¯è§£å³ä½¿ç¨ WSL2 è¿ä¸ªç¹æ§æéè¦ä»åºçä»£ä»·ç½¢äº

## Windows Docker Comparison

å¦å¤, åä¸»è¿å¯¹æ¯äº windows docker å©ç¨ WSL2 èæåæç®¡ TTRSS, åç°ç³»ç»å ç¨ä¸å¦ç´æ¥ç¨ WSL2 æ¥çè½»ä¾¿, å·ä½ä½éªæ¯

- windows + wsl2 => mem 3G
- wsl2 => 2G

å½ç¶, é¤äºåå­å ç¨æ´å¤ä¹å¤, éç½®ä»£çæ´æ¯æ ä»ä¸æ, ä¸æçéç½®æä»¶å¤±æ + GUI çé¢éç½®ä¹å¤±è´¥äº, æ»æ¯æ¾ä¸åä»£ççå°å, çæµæ¯å ä¸ WSL2 ç Buff, æ æ³ç®åçéè¿ `127.0.0.1:7890` æ¥è§£å³... è¿ä¸ªé®é¢å¯è½ççæ è§£, via: [Stackoverflow](https://stackoverflow.com/questions/48272933/docker-at-windows-10-proxy-propagation-to-containers-not-working), æ¥éå¦ä¸, å¸æç¥éçå¤§ä½¬å¯ä»¥æç¹ä¸äº.

```shell
docker Failed to connect to 127.0.0.1 port 7890 after 0 ms: Connection refused
```

![](https://user-images.githubusercontent.com/57313137/158712544-96fcd594-7628-41e8-a906-acdc672d5e22.png)
![](https://user-images.githubusercontent.com/57313137/158712547-68a408d5-a46d-42ec-ab6b-35f1f8a3af55.png)

ä¹è®¸è¿è¦åä¸æ¬¡ç«¯å£è½¬å, å¤æåº¦ä¸¤èé½å¿«ä¸æ ·äº, æä»¥æåæ¾å¼äºð...

## Backup Your Data

å½ç¶ä¸­éæ¢å° windows åè¿ä¸æ¬¡æ°æ®è¿ç§». å°è¯æè½½å¤ä»½äºæ°æ®, ç§»æ¤å° `windows`, å¶å®æéè¦çå°±æ¯ä¸ä¸ª `.sql` æä»¶, å¶ä»é½å¯ä»¥ä¸¢å¼.

```shell
$ docker run --rm --volumes-from a5b8c5847c8d -v /home/bgzocg/ttrss/backup:/backup ubuntu tar cvfP /backup/backup.tar /var/lib/postgresql/data/
```

via: [ð¯ å¤ä»½åè¿ç§»æ°æ® - Docker å¿«éå¥é¨ - æææ¡£](https://docker.easydoc.net/doc/81170005/cCewZWoN/XQEqNjiu )


## Finally

ä½¿ç¨å¦ä¸, ä»ä¾åè (èæ¬å æºå¨ç¯å¢èå¼, `windows` ç¨æ·å 15517 å `wsl2` ç¨æ·å `bgzocg`, `proxy` ç«¯å£ `7890`, `ttrss` ç«¯å£ `4040`).

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