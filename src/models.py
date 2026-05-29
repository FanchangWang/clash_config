"""数据模型定义"""

from dataclasses import dataclass, field
from typing import TypedDict


class ProxyDict(TypedDict, total=False):
    """代理配置字典类型"""

    name: str
    type: str
    server: str
    port: int
    country: str
    udp: bool


@dataclass
class ProxyGroup:
    """代理分组"""

    all: list[ProxyDict] = field(default_factory=list)
    udp: list[ProxyDict] = field(default_factory=list)
    ai_gemini: list[ProxyDict] = field(default_factory=list)
    porn_all: list[ProxyDict] = field(default_factory=list)
    porn_x: list[ProxyDict] = field(default_factory=list)


@dataclass
class ChromeGoState:
    """ChromeGo 数据源状态"""

    created_at: str = ""


@dataclass
class RipaoState:
    """Ripao 数据源状态"""

    sha: str = ""


@dataclass
class StoreData:
    """存储数据"""

    chrome_go: ChromeGoState = field(default_factory=ChromeGoState)
    ripao: RipaoState = field(default_factory=RipaoState)
