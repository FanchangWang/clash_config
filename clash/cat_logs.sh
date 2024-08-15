#!/bin/bash

# 查看 systemctl start clash 启动后的 logs
journalctl -u clash -o cat -f
