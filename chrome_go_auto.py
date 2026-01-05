#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chrome_go_updater import ChromeGoUpdater
from chrome_go_extractor import ChromeGoExtractor

def main():
    """
    主函数：先更新ChromeGo配置，然后提取代理配置
    """
    # 1. 调用ChromeGoUpdater().update()
    updater = ChromeGoUpdater()
    update_result = updater.update()
    
    # 2. 如果update()返回True，调用ChromeGoExtractor().run()
    if update_result:
        extractor = ChromeGoExtractor()
        extractor.run()

if __name__ == "__main__":
    main()
