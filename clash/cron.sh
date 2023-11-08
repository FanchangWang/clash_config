#!/bin/bash

set -e    # 立即退出脚本，如果任何命令的退出状态非零
set -u    # 未定义的变量将导致立即退出

CLASH_DIR=$(cd "$(dirname "$0")" && pwd)
SCRIPT_FILE=$(readlink -f "$0")
LOG_FILE="${CLASH_DIR}/$(basename ${SCRIPT_FILE} .sh).log"

if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
fi

MAX_LINES=100
LINE_COUNT=$(wc -l < "$LOG_FILE")
if [ $LINE_COUNT -gt $MAX_LINES ]; then
  DELETE_LINES=$((LINE_COUNT - MAX_LINES))
  sed -i "1,${DELETE_LINES}d" "$LOG_FILE"
fi

if ! crontab -l | grep -q "${SCRIPT_FILE}" ; then
  (crontab -l ; echo "0 * * * * ${SHELL} ${SCRIPT_FILE}") | crontab -
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: added cron job for $(basename ${SCRIPT_FILE})." >>${LOG_FILE}
else
  echo "[$(date +"%Y.%m.%d.%H:%M:%S")] Clash: cron job already exists for $(basename ${SCRIPT_FILE})." >>${LOG_FILE}
fi

${SHELL} ${CLASH_DIR}/run.sh >>${LOG_FILE}
