"""全局配置管理"""

import os
from pathlib import Path

from dotenv import load_dotenv


class Config:
    """全局配置类"""

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    TEMP_DIR = BASE_DIR / "temp"
    DIST_DIR = BASE_DIR / "dist"
    DIST_PROXIES_DIR = DIST_DIR / "proxies"
    DIST_PROVIDERS_DIR = DIST_DIR / "providers"

    STORE_FILE = DATA_DIR / "store.yaml"
    GEOIP_DB = DATA_DIR / "GeoLite2-Country.mmdb"

    CHROME_GO_PROJECT_ID = "free9999/ipupdate"
    CHROME_GO_TARGET_DIR = "backup/img/1/2/ipp"
    CHROME_GO_PROXIES_FILE = DATA_DIR / "chromego_proxies.yaml"

    RIPAO_REPO_URL = "https://api.github.com/repos/ripaojiedian/freenode/contents/clash"
    RIPAO_PROXIES_FILE = DATA_DIR / "ripao_proxies.yaml"

    AI_GEMINI_COUNTRIES = [
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
    PORN_PROTOCOLS = ["hysteria", "hysteria2", "tuic"]
    PORN_COUNTRIES = ["美国", "日本", "韩国", "香港", "台湾", "荷兰", "德国"]
    PORN_X_COUNTRIES = ["美国", "日本", "韩国", "香港", "台湾", "荷兰"]
    UDP_PROTOCOLS = ["hysteria", "hysteria2", "tuic"]

    @classmethod
    def github_token(cls) -> str | None:
        """从 .env 获取 GitHub token"""
        load_dotenv(cls.BASE_DIR / ".env")
        return os.environ.get("GITHUB_TOKEN")

    @classmethod
    def init_dirs(cls) -> None:
        """初始化所有必要的目录"""
        for d in [
            cls.DATA_DIR,
            cls.TEMP_DIR,
            cls.DIST_DIR,
            cls.DIST_PROXIES_DIR,
            cls.DIST_PROVIDERS_DIR,
        ]:
            d.mkdir(parents=True, exist_ok=True)
