"""ChromeGo 配置提取器"""

import copy
import os
from pathlib import Path

from ..config import Config
from ..converter import ProxyConverter
from ..logger import logger
from ..models import ProxyDict, ProxyGroup
from .base import BaseExtractor


class ChromeGoExtractor(BaseExtractor):
    """ChromeGo 配置提取器"""

    def __init__(self) -> None:
        super().__init__()
        self.chrome_go_temp_dir = (
            Config.TEMP_DIR
            / "ipupdate-master-backup-img-1-2-ipp"
            / "backup"
            / "img"
            / "1"
            / "2"
            / "ipp"
        )
        self.chrome_go_data_dir = Config.TEMP_DIR / "chrome_go"
        self.chrome_go_data_dir.mkdir(parents=True, exist_ok=True)

        if self.chrome_go_data_dir.exists():
            for file_name in os.listdir(self.chrome_go_data_dir):
                file_path = self.chrome_go_data_dir / file_name
                if file_path.is_file():
                    try:
                        file_path.unlink()
                    except Exception as e:
                        logger.warning(f"删除文件失败: {file_path}, 错误: {e}")

    def recursive_scan(
        self, scan_dir: Path, config_filename: str, parse_func
    ) -> list[ProxyDict]:
        """递归扫描目录，匹配配置文件名并解析"""
        full_scan_dir = self.chrome_go_temp_dir / scan_dir
        results = []

        if not full_scan_dir.exists():
            logger.warning(f"扫描目录不存在: {full_scan_dir}")
            return results

        for root, dirs, files in os.walk(full_scan_dir):
            for file in files:
                if file == config_filename:
                    config_path = Path(root) / file
                    logger.info(f"配置文件: {config_path}")
                    parsed_config = parse_func(config_path)
                    if parsed_config:
                        if isinstance(parsed_config, list):
                            results.extend(parsed_config)
                        else:
                            results.append(parsed_config)

        return results

    def process_proxies(
        self, proxies: list[ProxyDict], prefix: str = "go"
    ) -> ProxyGroup:
        """处理代理列表并分类"""
        proxies_by_protocol = {}
        group = ProxyGroup()

        for proxy in proxies:
            protocol = proxy.get("type", "unknown")
            if protocol == "unknown":
                continue

            if protocol not in proxies_by_protocol:
                proxies_by_protocol[protocol] = []

            if proxy.get("name") == "中国":
                continue

            if any(
                p["type"] == protocol
                and p["server"] == proxy["server"]
                and p.get("port") == proxy.get("port")
                and p.get("ports") == proxy.get("ports")
                for p in proxies_by_protocol[protocol]
            ):
                continue

            count = (
                sum(
                    1
                    for p in proxies_by_protocol[protocol]
                    if p.get("name", "").startswith(
                        f"{prefix}-{proxy['name']}-{protocol}-"
                    )
                )
                + 1
            )
            country = proxy["name"]
            proxy["name"] = f"{prefix}-{country}-{protocol}-{count}"

            proxies_by_protocol[protocol].append(copy.deepcopy(proxy))
            group.all.append(copy.deepcopy(proxy))

            if country in Config.AI_GEMINI_COUNTRIES:
                group.ai_gemini.append(copy.deepcopy(proxy))

            if protocol in Config.UDP_PROTOCOLS:
                group.udp.append(copy.deepcopy(proxy))

            if country in Config.PORN_X_COUNTRIES:
                group.porn_x.append(copy.deepcopy(proxy))

            if country in Config.PORN_COUNTRIES and protocol in Config.PORN_PROTOCOLS:
                group.porn_all.append(copy.deepcopy(proxy))

        return group

    def extract(self) -> ProxyGroup:
        """提取所有代理配置"""
        logger.info("开始提取 chromego 配置...")

        if not self.chrome_go_temp_dir.exists():
            logger.error(f"目录不存在: {self.chrome_go_temp_dir}")
            return ProxyGroup()

        scan_configs = [
            {
                "dir": "clash.meta2",
                "filename": "config.yaml",
                "parser": ProxyConverter.convert_clash_meta2,
            },
            {
                "dir": "hysteria",
                "filename": "config.json",
                "parser": ProxyConverter.convert_hysteria,
            },
            {
                "dir": "hysteria2",
                "filename": "config.json",
                "parser": ProxyConverter.convert_hysteria2,
            },
            {
                "dir": "mieru",
                "filename": "config.json",
                "parser": ProxyConverter.convert_mieru,
            },
            {
                "dir": "xray",
                "filename": "config.json",
                "parser": ProxyConverter.convert_xray,
            },
        ]

        all_proxies: list[ProxyDict] = []
        for config in scan_configs:
            logger.info(f"开始扫描 {config['dir']} 目录...")
            proxies = self.recursive_scan(
                Path(config["dir"]), config["filename"], config["parser"]
            )
            all_proxies.extend(proxies)

        group = self.process_proxies(all_proxies)

        logger.info(f"chrome_go 配置提取完成，共 {len(group.all)} 个协议配置")
        return group
