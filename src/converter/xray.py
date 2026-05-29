"""Xray 协议转换器"""

import json
from pathlib import Path

from ..logger import logger
from ..utils import get_geoip_country


class XrayConverter:
    """Xray 协议转换器"""

    @staticmethod
    def convert(config_file: Path) -> list[dict]:
        """将 xray 配置转换为 mihomo 格式"""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)

            outbounds = config.get("outbounds", [])
            mihomo_proxies = []

            for outbound in outbounds:
                protocol = outbound.get("protocol", "")
                if protocol not in ["trojan", "vless", "vmess"]:
                    continue

                streamSettings = outbound.get("streamSettings", {})
                xray_security = streamSettings.get("security", "")
                if xray_security != "reality":
                    continue

                realitySettings = streamSettings.get("realitySettings", {})
                transport_config = {
                    "tls": True,
                    "udp": True,
                    "sni": realitySettings.get("serverName", ""),
                    "servername": realitySettings.get("serverName", ""),
                    "client-fingerprint": realitySettings.get("fingerprint", ""),
                    "reality-opts": {
                        "public-key": realitySettings.get("publicKey", ""),
                        "short-id": realitySettings.get("shortId", ""),
                    },
                }

                xray_network = streamSettings.get("network", "tcp")
                if xray_network in ("raw", "tcp"):
                    transport_config["network"] = "tcp"
                elif xray_network == "grpc":
                    transport_config["network"] = "grpc"
                    transport_config["grpc-opts"] = {
                        "grpc-service-name": streamSettings.get("grpcSettings", {}).get(
                            "serviceName", ""
                        ),
                    }
                elif xray_network == "xhttp":
                    xhttpSettings = streamSettings.get("xhttpSettings", {})
                    transport_config["network"] = "xhttp"
                    transport_config["xhttp-opts"] = {
                        "host": xhttpSettings.get("host", ""),
                        "path": xhttpSettings.get("path", ""),
                        "mode": xhttpSettings.get("mode", ""),
                    }
                else:
                    continue

                settings = outbound.get("settings", {})

                if protocol == "vless":
                    vnext = settings.get("vnext", [])
                    for v in vnext:
                        address = v.get("address", "")
                        country = get_geoip_country(address)
                        port = v.get("port", 443)
                        users = v.get("users", [])

                        for user in users:
                            mihomo_proxy = transport_config.copy()
                            mihomo_proxy.update(
                                {
                                    "name": country,
                                    "type": "vless",
                                    "server": address,
                                    "port": port,
                                    "uuid": user.get("id", ""),
                                    "flow": user.get("flow", ""),
                                    "encryption": user.get("encryption", ""),
                                    "skip-cert-verify": True,
                                }
                            )
                            logger.info(f"转换 vless 配置: {mihomo_proxy}")
                            mihomo_proxies.append(mihomo_proxy)

                elif protocol == "vmess":
                    vnext = settings.get("vnext", [])
                    for v in vnext:
                        address = v.get("address", "")
                        country = get_geoip_country(address)
                        port = v.get("port", 443)
                        users = v.get("users", [])

                        for user in users:
                            mihomo_proxy = transport_config.copy()
                            mihomo_proxy.update(
                                {
                                    "name": country,
                                    "type": "vmess",
                                    "server": address,
                                    "port": port,
                                    "uuid": user.get("id", ""),
                                    "alterId": user.get("alterId", 0),
                                    "cipher": user.get("security", "auto"),
                                }
                            )
                            logger.info(f"转换 vmess 配置: {mihomo_proxy}")
                            mihomo_proxies.append(mihomo_proxy)

                elif protocol == "trojan":
                    servers = settings.get("servers", [])
                    for server in servers:
                        address = server.get("address", "")
                        country = get_geoip_country(address)
                        port = server.get("port", 443)
                        password = server.get("password", "")

                        mihomo_proxy = transport_config.copy()
                        mihomo_proxy.update(
                            {
                                "name": country,
                                "type": "trojan",
                                "server": address,
                                "port": port,
                                "password": password,
                                "skip-cert-verify": True,
                            }
                        )
                        logger.info(f"转换 trojan 配置: {mihomo_proxy}")
                        mihomo_proxies.append(mihomo_proxy)

            return mihomo_proxies
        except Exception as e:
            logger.error(f"转换 xray 配置失败: {e}")
            return []
