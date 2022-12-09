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

  # 安装相应依赖
  apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y
  apt install liblzma-dev -y
  apt install wget -y
  apt install vim -y
  apt install curl -y
  apt install git -y


  # 安装对应版本python
  wget https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz -O Python-3.9.15.tgz
  tar -xf Python-3.9.15.tgz
  cd Python-3.9.15
  ./configure --enable-optimizATIons
  make altinstall

  # 建立软链接
  ln -s /usr/local/bin/pip3.9 /usr/bin/pip
  ln -s /usr/local/bin/pip3.9 /usr/bin/pip3
  ln -s /usr/local/bin/python3.9 /usr/bin/python
  ln -s /usr/local/bin/python3.9 /usr/bin/python3

  # 安装rust
  curl https://sh.rustup.rs -sSf | sh
  apt install ffmpeg -y
  source "$HOME/.cargo/env"

  # 安装项目依赖
  cd ~/vced/code/service
  pip install -r requirements.txt
  cd ~/vced/code/web
  pip install -r requirements.txt
  pip install git+https://github.com/openai/CLIP.git

  # 运行前端
  nohup streamlit run app.py &
  # 运行后端
  cd ~/vced/code/service
  python app.py --timeout-ready
else
  echo "脚本未执行..."
fi
