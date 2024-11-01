#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip -O gh-pages.zip
unzip gh-pages.zip
rm -rf ./ui
mv metacubexd-gh-pages ui
rm gh-pages.zip
ls -la ./ui
