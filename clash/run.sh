#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

CLASH_DIR=$(cd "$(dirname "$0")" && pwd)

if [ "$(systemctl is-active clash)" = "active" ]; then
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: service is running……"
else
  if [[ -x "${CLASH_DIR}/clash.meta" ]]; then
    echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: starting service……"
    systemctl start clash
    if [ "$(systemctl is-active clash)" = "active" ]; then
      echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: service started successfully."
    else
      echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: service failed to start!"
    fi
  else
    echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: application is not executable!"
  fi
fi
