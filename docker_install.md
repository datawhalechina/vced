# docker安装

> Windows不支持docker, 所谓的Windows下的Docker Desktop本质也是通过wsl(可以理解为Win下轻量的虚拟机), 所以不论想通过docker部署还是本地配环境跑源码, 都建议先把wsl装起来

下面以docker engine安装为例(来源[官网文档](https://docs.docker.com/engine/install/ubuntu/))   (ps:docker engine只有command line, 没有图形界面, 更适合远程开发, 轻量而方便)

wsl中不支持`systemctl`，**不建议**直接按照终端的hint安装docker.io

```shell
1. sudo apt-get remove docker docker-engine docker.io containerd runc
2. sudo apt-get update
   sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
3. sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
4. echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
5. sudo apt-get update
6. sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

启动Docker Engine:

```shell
sudo service docker start
```

显示` * Starting Docker: docker `即为启动成功(**每次用docker都要先启动**)

> 常用指令
>
> ```
> sudo docker images  	# 查看镜像
> sudo docker ps [-a]     # 查看[所有]容器
> sudo docker info    	# 查看docker配置
> sudo docker pull		# 拉取镜像
> ```
>
> readme中是通过docker compose(docker的进一步封装，命令更加简洁，一条龙服务)来构建本地镜像，并创建和跑一个容器