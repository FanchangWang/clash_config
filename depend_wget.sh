#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

# 下载 web ui
wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip -O gh-pages.zip
unzip gh-pages.zip
rm -rf ./ui
mv metacubexd-gh-pages ui
rm gh-pages.zip
ls -la ./ui

# 下载需求文件
wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.dat -O GeoIP.dat
wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geosite.dat -O GeoSite.dat
wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb -O GeoIP.metadb
wget https://mirror.ghproxy.com/https://github.com/xishang0128/geoip/releases/download/latest/GeoLite2-ASN.mmdb -O GeoLite2-ASN.mmdb

# 下载 config.yaml
wget https://mirror.ghproxy.com/https://raw.githubusercontent.com/FanchangWang/clash_config/main/config.yaml -O config.yaml

# 查看
ls -la .
