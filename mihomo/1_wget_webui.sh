#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

config_dir="./config"
webui_dir="$config_dir/ui/"
download_file="$config_dir/metacubexd-gh-pages.zip"

# 如果目标目录不存在，则创建
if [ ! -d "$webui_dir" ]; then
    mkdir -p "$webui_dir"
fi

# 下载文件到 config_dir 目录
wget https://mirror.ghproxy.com/https://github.com/MetaCubeX/metacubexd/archive/refs/heads/gh-pages.zip -O "$download_file"

# 解压文件到临时目录
unzip -j "$download_file" -d "$webui_dir"

# 删除下载的压缩包
rm "$download_file"

# 查看 webui_dir 文件
ls -la "$webui_dir"
