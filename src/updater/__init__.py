"""updater 模块"""

from .base import BaseUpdater
from .chrome_go import ChromeGoUpdater
from .ripao import RipaoUpdater

__all__ = ["BaseUpdater", "ChromeGoUpdater", "RipaoUpdater"]
