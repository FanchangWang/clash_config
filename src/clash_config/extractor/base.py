"""Extractor 基类"""

from abc import ABC, abstractmethod
from pathlib import Path

from ..config import Config
from ..logger import logger
from ..models import ProxyGroup
from ..utils import save_yaml


class BaseExtractor(ABC):
    """提取器抽象基类"""

    def __init__(self) -> None:
        self.config = Config()

    @abstractmethod
    def extract(self) -> ProxyGroup:
        """提取并处理代理配置"""

    def save(self, group: ProxyGroup, output_path: Path) -> None:
        """保存代理组到文件"""
        save_yaml({"proxies": group.all}, output_path)
        logger.info(f"已保存 {len(group.all)} 个代理到 {output_path}")
