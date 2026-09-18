"""全局配置管理"""

from pathlib import Path
from typing import ClassVar

from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path)


class Config:
    """全局配置类"""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    TEMP_DIR = BASE_DIR / "temp"
    DIST_DIR = BASE_DIR / "dist"
    DIST_PROXIES_DIR = DIST_DIR / "proxies"
    TEMPLATE_DIR = BASE_DIR / "src" / "clash_config" / "templates"

    STORE_FILE = DATA_DIR / "store.yaml"
    GEOIP_DB = DATA_DIR / "GeoLite2-Country.mmdb"

    CHROME_GO_PROJECT_ID = "free9999/ipupdate"
    CHROME_GO_TARGET_DIR = "backup/img/1/2/ipp"
    CHROME_GO_PROXIES_FILE = DATA_DIR / "chromego_proxies.yaml"

    # 手动 IP/域名 -> 国家 映射, 用于纠正 ip-api 返回错误的归属国家
    IP_COUNTRY_MAP_FILE = DATA_DIR / "ip_country_map.yaml"
    # IP/域名 -> 额外允许加入的分组, 用于绕过国家/协议限制(如美国的 Gemini 可用 IP)
    IP_GROUP_ALLOW_FILE = DATA_DIR / "ip_group_allow.yaml"

    AI_GEMINI_COUNTRIES: ClassVar[list[str]] = [
        "日本",
        "韩国",
        "台湾",
        "荷兰",
        "法国",
        "新加坡",
        "印度",
        "马来西亚",
        "泰国",
        "越南",
        "印度尼西亚",
        "菲律宾",
    ]
    PORN_PROTOCOLS: ClassVar[list[str]] = ["hysteria", "hysteria2", "tuic"]
    PORN_COUNTRIES: ClassVar[list[str]] = ["美国", "日本", "韩国", "香港", "台湾", "荷兰", "德国"]
    PORN_X_COUNTRIES: ClassVar[list[str]] = ["美国", "日本", "韩国", "香港", "台湾", "荷兰"]
    UDP_PROTOCOLS: ClassVar[list[str]] = ["hysteria", "hysteria2", "tuic"]

    @classmethod
    def init_dirs(cls) -> None:
        """初始化所有必要的目录"""
        for d in [
            cls.DATA_DIR,
            cls.TEMP_DIR,
            cls.DIST_DIR,
            cls.DIST_PROXIES_DIR,
        ]:
            d.mkdir(parents=True, exist_ok=True)
