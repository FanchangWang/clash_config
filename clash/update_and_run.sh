#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

CLASH_DIR=$(cd "$(dirname "$0")" && pwd)

PRYXY="http://ghproxy.homeboyc.cn/"

DOWNLOAD_URL=$(curl -s -H "Accept: application/vnd.github.v3+json" "${PRYXY}https://api.github.com/repos/Dreamacro/clash/releases/tags/premium" \
  | jq -r '.assets[] | select(.browser_download_url | index("clash-linux-arm64")) | .browser_download_url')
FILE=$(basename "${DOWNLOAD_URL}" | sed 's/\.gz$//')

if [[ ! -e "${CLASH_DIR}/${FILE}" ]]; then
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: a new version is available, updating now..."
  if wget -q --show-progress=off -O "${CLASH_DIR}/${FILE}.gz" "${PRYXY}${DOWNLOAD_URL}"; then
    gzip -d "${CLASH_DIR}/${FILE}.gz"
    chmod +x "${CLASH_DIR}/${FILE}"
    if [ "$(systemctl is-active clash)" = "active" ]; then
      echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: stopping service."
      systemctl stop clash
      while [ "$(systemctl is-active clash)" = "active" ]; do
          sleep 1
        done
      echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: service is stopped."
    fi
    if [[ -L "${CLASH_DIR}/clash" ]]; then
      rm -f "${CLASH_DIR}/clash"
    fi
    ln -sf "${CLASH_DIR}/${FILE}" "${CLASH_DIR}/clash"
  else
    echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: file download failed."
  fi
else
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: already has the latest release."
fi


if [ "$(systemctl is-active clash)" = "active" ]; then
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: service is running……"
else
  if [[ -x "${CLASH_DIR}/clash" ]]; then
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
