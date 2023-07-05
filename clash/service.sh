#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

# 获取脚本所在目录
CLASH_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# 判断 clash.service 文件是否存在
if [ ! -e "${CLASH_DIR}/clash.service" ]; then
  # 文件不存在，创建并输出文件内容
  CONTENT=$(cat <<EOF
[Unit]
Description=Clash Service
After=network-online.target

[Service]
ExecStart=${CLASH_DIR}/clash -d ${CLASH_DIR}/config
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
)

  # 将变量${CLASH_DIR}用脚本的目录替换，然后输出到文件
  echo -e "${CONTENT/\\\$\\{CLASH_DIR\}/${CLASH_DIR}}" > "${CLASH_DIR}/clash.service"
  # 添加系统服务
  ln -sf "${CLASH_DIR}/clash.service" "/etc/systemd/system/clash.service"
  systemctl enable clash
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: clash.service created successfully."
fi

${SHELL} "${CLASH_DIR}/cron.sh"
