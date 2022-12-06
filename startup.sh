#!/bin/bash

if [ `arch` = "arm32" -o `arch` = "arm64" -o `arch` = "aarch64" ]; then \
  docker-compose -f docker-compose-arm.yml up -d ; \
else \
  docker-compose -f docker-compose.yml up -d; \
fi
