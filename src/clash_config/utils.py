"""工具函数模块"""

import socket
from pathlib import Path
from typing import Any

import geoip2.database
import geoip2.errors
import httpx
import yaml

from .config import Config
from .logger import logger
from .models import ChromeGoState, RipaoState, StoreData


def get_geoip_country(server: str) -> str:
    """获取 IP 地址的国家名称(中文)"""
    try:
        ip_address = socket.gethostbyname(server)
    except socket.gaierror:
        ip_address = server

    api_url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN&fields=country,status,message"
    try:
        response = httpx.get(api_url, timeout=10)
        result = response.json()

        if result.get("status") != "success":
            logger.warning(f"ip-api 查询失败: {result.get('message', '未知错误')}")
        else:
            country = result.get("country")
            if country:
                return country
            logger.warning("ip-api 返回成功但缺少国家信息")
    except httpx.RequestError as e:
        logger.warning(f"ip-api 网络异常: {e}")
    except Exception as e:
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
    except Exception as e:
        logger.warning(f"GeoIP 查询异常: {e}")
        return "未知"


def load_yaml(file_path: Path) -> dict[str, Any]:
    """加载 YAML 文件"""
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: dict[str, Any], file_path: Path) -> None:
    """保存 YAML 文件"""
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)


def load_store() -> StoreData:
    """加载状态存储"""
    if Config.STORE_FILE.exists():
        data = load_yaml(Config.STORE_FILE)
        return StoreData(
            chrome_go=ChromeGoState(created_at=data.get("chrome_go", {}).get("created_at", "")),
            ripao=RipaoState(sha=data.get("ripao", {}).get("sha", "")),
        )
    return StoreData()


def save_store(store: StoreData) -> None:
    """保存状态存储"""
    data = {
        "chrome_go": {
            "created_at": store.chrome_go.created_at,
        },
        "ripao": {
            "sha": store.ripao.sha,
        },
    }
    save_yaml(data, Config.STORE_FILE)
