#!/bin/bash

# 查看 systemctl start mihomo 启动后的 logs
journalctl -u mihomo -o cat -f
