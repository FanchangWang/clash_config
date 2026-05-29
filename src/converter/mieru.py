"""Mieru 协议转换器"""

import json
from pathlib import Path

from ..logger import logger
from ..utils import get_geoip_country


class MieruConverter:
    """Mieru 协议转换器"""

    @staticmethod
    def convert(config_file: Path) -> list[dict]:
        """将 mieru 配置转换为 mihomo 格式"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            mihomo_proxies = []
            profiles = config.get("profiles", [])

            for profile in profiles:
                user = profile.get("user", {})
                username = user.get("name", "")
                password = user.get("password", "")
                servers = profile.get("servers", [])

                for server in servers:
                    address = server.get("ipAddress", "")
                    country = get_geoip_country(address)
                    portBindings = server.get("portBindings", [])

                    for portBinding in portBindings:
                        port = portBinding.get("port", "443")
                        portRange = portBinding.get("portRange", "")
                        protocol = portBinding.get("protocol", "TCP")

                        mihomo_proxy = {
                            "name": country,
                            "type": "mieru",
                            "server": address,
                            "transport": protocol.upper(),
                            "udp": True,
                            "username": username,
                            "password": password,
                        }

                        if portRange:
                            mihomo_proxy["portRange"] = portRange
                        else:
                            mihomo_proxy["port"] = port

                        logger.info(f"转换 mieru 配置: {mihomo_proxy}")
                        mihomo_proxies.append(mihomo_proxy)

            return mihomo_proxies
        except Exception as e:
            logger.error(f"转换 mieru 配置失败: {e}")
            return []
