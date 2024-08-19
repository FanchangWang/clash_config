#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

# 获取 version.txt 中的字符串
version_link="https://mirror.ghproxy.com/https://github.com/MetaCubeX/mihomo/releases/latest/download/version.txt"
echo "mihomo version_link: $version_link"

version=$(curl -L -s $version_link)
echo "mihomo version: $version"
if [ -z "$version" ]; then
    echo "ERROR: mihomo get version error!"
    exit 1
fi

# 拼接下载链接
download_link="https://mirror.ghproxy.com/https://github.com/MetaCubeX/mihomo/releases/latest/download/mihomo-linux-arm64-${version}.gz"
echo "mihomo download_link: $download_link"

# 下载文件
echo "mihomo downloading ~"
wget -q $download_link

# 解压文件
echo "mihomo gunzip ~"
gunzip "mihomo-linux-arm64-${version}.gz"

## 增加执行权限
echo "mihomo chmod +x ~"
chmod +x "mihomo-linux-arm64-${version}"

# 创建软连接
echo "mihomo creat symbolic link ~"
ln -sf "mihomo-linux-arm64-${version}" mihomo

# 打印文件列表
echo "mihomo file list ~"
ls -la
