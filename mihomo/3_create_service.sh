#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

# 获取脚本所在目录
MIHOMO_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 判断 mihomo.service 文件是否存在
if [ ! -e "${MIHOMO_DIR}/mihomo.service" ]; then
  # 文件不存在，创建并输出文件内容
  CONTENT=$(cat <<EOF
[Unit]
Description=mihomo Daemon, Another Clash Kernel.
After=network.target network-online.target NetworkManager.service systemd-networkd.service iwd.service

[Service]
Type=simple
LimitNPROC=500
LimitNOFILE=1000000
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_RAW CAP_NET_BIND_SERVICE CAP_SYS_TIME CAP_SYS_PTRACE CAP_DAC_READ_SEARCH CAP_DAC_OVERRIDE
Restart=always
ExecStartPre=/usr/bin/sleep 1s
ExecStart=${MIHOMO_DIR}/mihomo -d ${MIHOMO_DIR}/config
ExecReload=/bin/kill -HUP \$MAINPID

[Install]
WantedBy=multi-user.target
EOF
)

  # 将变量${MIHOMO_DIR}用脚本的目录替换，然后输出到文件
  echo -e "${CONTENT/\\\$\\{MIHOMO_DIR\}/${MIHOMO_DIR}}" > "${MIHOMO_DIR}/mihomo.service"
  # 添加系统服务
  ln -sf "${MIHOMO_DIR}/mihomo.service" "/etc/systemd/system/mihomo.service"
  systemctl enable mihomo
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] mihomo: mihomo.service created successfully."
fi
