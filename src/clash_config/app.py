"""程序主入口"""

from .config import Config
from .logger import logger
from .merger import Merger
from .updater.chrome_go import ChromeGoUpdater


class App:
    """Clash 配置自动整理工具主类"""

    def __init__(self) -> None:
        """初始化应用"""
        Config.init_dirs()

    def run(self) -> None:
        """运行应用主流程"""
        chrome_updater = ChromeGoUpdater()

        chrome_updated, chrome_group = chrome_updater.update()

        if chrome_updated:
            Merger().merge(chrome_group)
        else:
            logger.info("未检测到配置更新")


def run() -> None:
    """便捷运行函数"""
    App().run()
