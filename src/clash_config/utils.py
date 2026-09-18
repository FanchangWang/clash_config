"""工具函数模块"""

import contextlib
import ipaddress
import json
import socket
from pathlib import Path
from typing import Any, override

import geoip2.database
import geoip2.errors
import httpx
import yaml

from .config import Config
from .logger import logger
from .models import ChromeGoState, StoreData


class _Dumper(yaml.Dumper):
    """缩进列表项的自定义 Dumper"""

    @override
    def increase_indent(self, flow: bool = False, indentless: bool = False) -> None:
        super().increase_indent(flow, False)


_ip_country_map: dict[str, str] | None = None
_ip_group_allow: dict[str, set[str]] | None = None

# ProxyGroup 里可被白名单追加的字段名
GROUP_NAMES: tuple[str, ...] = ("all", "udp", "ai_gemini", "porn_all", "porn_x")


def _map_keys(key: str) -> list[str]:
    """映射表 key 的原值与 IP 规范化值(IPv6 大小写/前导零/缩写写法统一)"""
    keys = [key]
    with contextlib.suppress(ValueError):
        keys.append(str(ipaddress.ip_address(key)))
    return keys


def _load_ip_country_map() -> dict[str, str]:
    """加载手动 IP/域名 -> 国家 映射(带进程内缓存)"""
    global _ip_country_map
    if _ip_country_map is not None:
        return _ip_country_map

    mapping: dict[str, str] = {}
    if Config.IP_COUNTRY_MAP_FILE.exists():
        data = load_yaml(Config.IP_COUNTRY_MAP_FILE)
        for raw_key, raw_value in (data or {}).items():
            if raw_key and raw_value:
                value = str(raw_value).strip()
                for k in _map_keys(str(raw_key).strip()):
                    mapping.setdefault(k, value)
    else:
        logger.warning(f"手动 IP 映射文件不存在: {Config.IP_COUNTRY_MAP_FILE}")

    _ip_country_map = mapping
    return mapping


def _load_ip_group_allow() -> dict[str, set[str]]:
    """加载 IP/域名 -> 额外允许分组 映射(带进程内缓存)"""
    global _ip_group_allow
    if _ip_group_allow is not None:
        return _ip_group_allow

    mapping: dict[str, set[str]] = {}
    if Config.IP_GROUP_ALLOW_FILE.exists():
        data = load_yaml(Config.IP_GROUP_ALLOW_FILE)
        for raw_key, raw_value in (data or {}).items():
            if not (raw_key and raw_value):
                continue
            key = str(raw_key).strip()
            names = raw_value if isinstance(raw_value, list) else [raw_value]
            groups = {str(n).strip() for n in names}
            unknown = groups - set(GROUP_NAMES)
            if unknown:
                logger.warning(f"未知分组名 {sorted(unknown)}, 可选: {', '.join(GROUP_NAMES)}")
            valid = groups & set(GROUP_NAMES)
            if valid:
                for k in _map_keys(key):
                    mapping.setdefault(k, valid)
    else:
        logger.warning(f"分组白名单文件不存在: {Config.IP_GROUP_ALLOW_FILE}")

    _ip_group_allow = mapping
    return mapping


def _resolve_ips(server: str) -> list[str]:
    """解析 server 为 IP 字符串列表(支持 IPv4/IPv6), 解析失败返回空列表"""
    # 已是 IP 字面量: 同时给出原值与规范化值
    try:
        ip = ipaddress.ip_address(server)
    except ValueError:
        pass
    else:
        return [server, str(ip)]

    try:
        return [
            str(info[4][0]) for info in socket.getaddrinfo(server, None, type=socket.SOCK_STREAM)
        ]
    except socket.gaierror:
        return []


def _server_keys(server: str) -> list[str]:
    """server 的全部匹配 key: 原值 + 解析/规范化后的 IP"""
    return [server, *_resolve_ips(server)]


def get_allowed_groups(server: str) -> set[str]:
    """获取该 IP/域名被额外允许加入的分组"""
    if not server:
        return set()

    mapping = _load_ip_group_allow()
    for key in _server_keys(server):
        if key in mapping:
            logger.debug(f"分组白名单命中: {key} -> {sorted(mapping[key])}")
            return mapping[key]
    return set()


def get_geoip_country(server: str) -> str:
    """获取 IP 地址的国家名称(中文), 优先使用手动映射纠正"""
    mapping = _load_ip_country_map()
    for key in _server_keys(server):
        if key in mapping:
            logger.debug(f"手动映射命中: {key} -> {mapping[key]}")
            return mapping[key]

    ip_candidates = _resolve_ips(server)
    ip_address = ip_candidates[0] if ip_candidates else server

    api_url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN&fields=country,status,message"
    try:
        response = httpx.get(api_url, timeout=10)
        result = response.json()

        if result.get("status") != "success":
            logger.warning(f"ip-api 查询失败: {result.get('message', '未知错误')}")
        else:
            country = result.get("country")
            if country:
                return str(country)
            logger.warning("ip-api 返回成功但缺少国家信息")
    except httpx.RequestError as e:
        logger.warning(f"ip-api 网络异常: {e}")
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"ip-api 解析异常: {e}")

    try:
        if not Config.GEOIP_DB.exists():
            logger.warning(f"GeoIP 数据库不存在: {Config.GEOIP_DB}")
            return "未知"
        with geoip2.database.Reader(str(Config.GEOIP_DB)) as reader:
            response = reader.country(ip_address)
            return response.country.names.get("zh-CN", response.country.name or "未知")
    except geoip2.errors.AddressNotFoundError:
        return "未知"
    except geoip2.errors.GeoIP2Error as e:
        logger.warning(f"GeoIP 查询异常: {e}")
        return "未知"


def load_yaml(file_path: Path) -> dict[str, Any]:
    """加载 YAML 文件"""
    with file_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: dict[str, Any], file_path: Path) -> None:
    """保存 YAML 文件"""
    with file_path.open("w", encoding="utf-8", newline="") as f:
        yaml.dump(
            data, f, Dumper=_Dumper, allow_unicode=True, default_flow_style=False, sort_keys=False
        )


def dump_yaml(data: Any) -> str:
    """将数据转为 YAML 字符串"""
    return str(
        yaml.dump(
            data, Dumper=_Dumper, allow_unicode=True, default_flow_style=False, sort_keys=False
        )
    )


def load_store() -> StoreData:
    """加载状态存储"""
    if Config.STORE_FILE.exists():
        data = load_yaml(Config.STORE_FILE)
        return StoreData(
            chrome_go=ChromeGoState(created_at=data.get("chrome_go", {}).get("created_at", ""))
        )
    return StoreData()


def save_store(store: StoreData) -> None:
    """保存状态存储"""
    data = {
        "chrome_go": {
            "created_at": store.chrome_go.created_at,
        },
    }
    save_yaml(data, Config.STORE_FILE)
