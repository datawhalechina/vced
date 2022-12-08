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
  echo "使用原生指令安装环境"
fi
