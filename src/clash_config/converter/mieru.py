"""Mieru 协议转换器"""

import json
from pathlib import Path
from typing import cast

from ..logger import logger
from ..models import ProxyDict
from ..utils import get_geoip_country


class MieruConverter:
    """Mieru 协议转换器"""

    @staticmethod
    def convert(config_file: Path) -> list[ProxyDict]:
        """将 mieru 配置转换为 mihomo 格式"""
        try:
            with open(config_file, encoding="utf-8") as f:
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
                    port_bindings = server.get("portBindings", [])

                    for port_binding in port_bindings:
                        port = port_binding.get("port", "443")
                        port_range = port_binding.get("portRange", "")
                        protocol = port_binding.get("protocol", "TCP")

                        mihomo_proxy = {
                            "name": country,
                            "type": "mieru",
                            "server": address,
                            "transport": protocol.upper(),
                            "udp": True,
                            "username": username,
                            "password": password,
                        }

                        if port_range:
                            mihomo_proxy["portRange"] = port_range
                        else:
                            mihomo_proxy["port"] = port

                        logger.info(f"转换 mieru 配置: {mihomo_proxy}")
                        mihomo_proxies.append(mihomo_proxy)

            return cast("list[ProxyDict]", mihomo_proxies)
        except Exception as e:
            logger.error(f"转换 mieru 配置失败: {e}")
            return []
