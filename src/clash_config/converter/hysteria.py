"""Hysteria 协议转换器"""

import json
import re
from pathlib import Path
from typing import cast

from ..logger import logger
from ..models import ProxyDict
from ..utils import get_geoip_country


class HysteriaConverter:
    """Hysteria 协议转换器"""

    @staticmethod
    def _parse_server_address(server: str) -> tuple[str, int, str | None, bool]:
        """解析服务器地址，处理各种格式"""
        server_addr = server
        port = 443
        ports = None
        is_multi_port = False

        ipv6_match = re.match(r"^\[([0-9a-fA-F:.]+)\]:(.+)$", server)
        if ipv6_match:
            server_addr = ipv6_match.group(1)
            port_part = ipv6_match.group(2)
            first_port_match = re.search(r"^(\d+)", port_part)
            if first_port_match:
                port = int(first_port_match.group(1))
            if "," in port_part or "-" in port_part:
                ports = port_part
                is_multi_port = True
        else:
            ipv4_or_domain_match = re.match(r"^([^:]+):(.+)$", server)
            if ipv4_or_domain_match:
                server_addr = ipv4_or_domain_match.group(1)
                port_part = ipv4_or_domain_match.group(2)
                first_port_match = re.search(r"^(\d+)", port_part)
                if first_port_match:
                    port = int(first_port_match.group(1))
                if "," in port_part or "-" in port_part:
                    ports = port_part
                    is_multi_port = True
            else:
                server_addr = server
                port = 443
                is_multi_port = False

        return server_addr, port, ports, is_multi_port

    @staticmethod
    def convert(config_file: Path) -> ProxyDict | None:
        """将 hysteria 配置转换为 mihomo 格式"""
        try:
            with open(config_file, encoding="utf-8") as f:
                config = json.load(f)

            server = config.get("server", "")
            server_addr, port, ports, is_multi_port = HysteriaConverter._parse_server_address(
                server
            )
            country = get_geoip_country(server_addr)

            mihomo_config = {
                "name": country,
                "type": "hysteria",
                "server": server_addr,
                "protocol": config.get("protocol", ""),
                "port": port,
                "auth-str": config.get("auth_str", ""),
                "sni": config.get("server_name", ""),
                "alpn": [config.get("alpn")]
                if isinstance(config.get("alpn"), str)
                else config.get("alpn", []),
                "up": config.get("up_mbps", ""),
                "down": config.get("down_mbps", ""),
                "skip-cert-verify": config.get("insecure", False),
                "fast-open": config.get("fast_open", False),
                "recv-window-conn": config.get("recv_window_conn", 12582912),
                "recv-window": config.get("recv_window", 52428800),
                "disable-mtu-discovery": config.get("disable_mtu_discovery", False),
            }

            if is_multi_port:
                mihomo_config["ports"] = ports

            logger.info(f"转换 hysteria 配置: {mihomo_config}")
            return cast(ProxyDict, mihomo_config)
        except Exception as e:
            logger.error(f"转换 hysteria 配置失败: {e}")
            return None
