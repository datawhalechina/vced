#!/bin/bash

if [ "$1" == "" -o "$1" == "docker" ]; then
  if [ `arch` = "arm32" -o `arch` = "arm64" -o `arch` = "aarch64" ]; then
    docker-compose -f docker-compose-arm.yml build
    docker-compose -f docker-compose-arm.yml up -d
  else
    docker-compose build
    docker-compose up -d
  fi
elif [ "$1" == "native" ]; then
  cd ~
  # 更新系统信息
  apt update

  # 移出老版本python
  apt autoremove python -y
  apt autoremove python3 -y
  apt autoremove python3.8 -y
  apt autoremove python3.9 -y
  apt autoremove python3-pip -y

  # 下载新版本python
  apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
  apt install wget -y
  apt install vim -y
  wget https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz
  tar -xf Python-3.9.15.tgz
  cd Python-3.9.15
  ./configure --enable-optimizATIons
  make altinstall

  # 建立软链接
  rm /usr/bin/python
  rm /usr/bin/python3
  rm /usr/bin/pip
  rm /usr/bin/pip3

  ln -s /usr/local/bin/pip3.9 /usr/bin/pip
  ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
  ln -s /usr/local/bin/python3.9 /usr/bin/python
  ln -s /usr/local/bin/python3.9 /usr/bin/python3

  # 安装rust ffmpeg
  curl https://sh.rustup.rs -sSf | sh
  apt install ffmpeg -y

  # 下载项目
  apt install git
  cd ~
  git clone https://github.com/datawhalechina/vced.git
  cd  ./vced/code/service
  pip install -r requirements.txt
  cd ~/vced/code/web
  pip install -r requirements.txt
  pip install git+https://github.com/openai/CLIP.git
  #python app.py
fi
