<!--
 * @Author: Firmin.Sun fmsunyh@gmail.com
 * @Date: 2024-07-19 13:48:41
 * @LastEditors: Firmin.Sun fmsunyh@gmail.com
 * @LastEditTime: 2024-07-19 14:27:21
 * @FilePath: \aistore\chfs.md
 * @Description: 
-->
## 官网
[chfs](http://iscute.cn/chfs)

1.下载
```sh
wget http://iscute.cn/tar/chfs/3.1/chfs-linux-amd64-3.1.zip
```

```sh
unzip chfs-linux-amd64-3.1.zip -d /opt/chfs
```

```sh
sudo chmod a+x /opt/chfs/chfs-linux-amd64-3.1
```

2. 配置开机启动
```sh
sudo vim /etc/systemd/system/chfs.service
```

```vim
[Unit]
Description=chfs server

[Service]
ExecStart=/opt/chfs/chfs-linux-amd64-3.1 -port 7860 -path /mnt/ai_store

Restart=always

[Install]
WantedBy=multi-user.target
```

```sh
sudo systemctl enable chfs.service
sudo systemctl start chfs.service
sudo systemctl stop chfs.service
sudo systemctl restart chfs.service
sudo systemctl status chfs.service
sudo systemctl disable chfs.service

```

3 其他
```sh
/opt/chfs/chfs-linux-amd64-3.1 --help
```

服务器
```vim
aistore
ip：120.233.206.35
user：ads
pwd：unaigc2024
```