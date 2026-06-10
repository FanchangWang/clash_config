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
        """完整更新流程, 返回(是否更新, ProxyGroup)"""
        pass

    def _save_state(self) -> None:
        """保存更新状态(重新加载最新 store, 仅覆盖当前源字段)"""
        store = load_store()
        if self.source_name == "chrome_go":
            store.chrome_go.created_at = self.store.chrome_go.created_at
        elif self.source_name == "ripao":
            store.ripao.sha = self.store.ripao.sha
        save_store(store)
