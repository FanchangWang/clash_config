"""extractor 模块"""

from .base import BaseExtractor
from .chrome_go import ChromeGoExtractor
from .ripao import RipaoExtractor

__all__ = ["BaseExtractor", "ChromeGoExtractor", "RipaoExtractor"]
