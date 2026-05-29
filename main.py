#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Clash 配置自动整理工具 - 主入口"""

import sys
import traceback

from src import App, logger


def main() -> int:
    """程序主入口"""
    try:
        app = App()
        app.run()
        return 0
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        return 1
    except Exception as e:
        logger.critical(f"程序运行异常: {e}")
        logger.debug(f"异常详情:\n{traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
