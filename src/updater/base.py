"""Updater 基类"""

from abc import ABC, abstractmethod

from ..config import Config
from ..models import ProxyGroup, StoreData
from ..utils import load_store, save_store


class BaseUpdater(ABC):
    """更新器抽象基类"""

    source_name: str

    def __init__(self) -> None:
        self.config = Config()
        self.store: StoreData = load_store()

    @abstractmethod
    def check_update(self) -> bool:
        """检查是否有更新"""
        pass

    @abstractmethod
    def download(self) -> bool:
        """下载更新"""
        pass

    @abstractmethod
    def update(self) -> tuple[bool, ProxyGroup]:
        """完整更新流程，返回(是否更新, ProxyGroup)"""
        pass

    def _save_state(self) -> None:
        """保存更新状态"""
        save_store(self.store)
