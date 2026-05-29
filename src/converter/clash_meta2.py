"""Clash Meta2 协议转换器"""

from pathlib import Path

import yaml

from ..logger import logger
from ..utils import get_geoip_country


class ClashMeta2Converter:
    """Clash Meta2 协议转换器"""

    @staticmethod
    def convert(config_file: Path) -> list[dict]:
        """将 clash.meta2 配置转换为 mihomo 格式"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            proxies = config.get("proxies", [])
            mihomo_proxies = []

            for proxy in proxies:
                proxy["name"] = get_geoip_country(proxy["server"])
                logger.info(f"转换 clash.meta2 配置: {proxy}")
                mihomo_proxies.append(proxy)

            return mihomo_proxies
        except Exception as e:
            logger.error(f"转换 clash.meta2 配置失败: {e}")
            return []
