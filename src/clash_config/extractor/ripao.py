"""Ripao 配置提取器"""

import copy
import tempfile
from pathlib import Path
from typing import override

import yaml

from ..config import Config
from ..converter import ProxyConverter
from ..logger import logger
from ..models import ProxyDict, ProxyGroup
from .base import BaseExtractor


class RipaoExtractor(BaseExtractor):
    """Ripao 配置提取器"""

    def __init__(self) -> None:
        super().__init__()
        self.input_file = Config.TEMP_DIR / "ripao_clash.yaml"

    def load_and_fix_yaml(self, content: str) -> list[ProxyDict]:
        """加载 yaml 内容并提取 proxies 字段, 自动修复格式问题"""
        try:
            logger.info("尝试直接读取 YAML 内容...")
            yaml_data = yaml.safe_load(content)
            return yaml_data.get("proxies", [])
        except yaml.YAMLError as e:
            logger.warning(f"解析 YAML 内容失败: {e}")
            logger.info("尝试修复 YAML 格式...")

            lines = content.split("\n")
            fixed_lines = []
            in_proxies_section = False

            for line in lines:
                stripped_line = line.strip()

                if stripped_line == "proxies:":
                    in_proxies_section = True
                    fixed_lines.append(line)
                    continue

                if (
                    in_proxies_section
                    and stripped_line
                    and not stripped_line.startswith("-")
                    and not stripped_line.startswith("  ")
                ):
                    in_proxies_section = False

                if (
                    in_proxies_section
                    and stripped_line.startswith("- {")
                    and "{" in stripped_line
                    and "}" not in stripped_line
                ):
                    logger.info(f"修复行: {line}")
                    line = line.rstrip() + "}"

                fixed_lines.append(line)

            fixed_content = "\n".join(fixed_lines)

            try:
                logger.info("修复后再次尝试读取 YAML...")
                yaml_data = yaml.safe_load(fixed_content)
                return yaml_data.get("proxies", [])
            except yaml.YAMLError as e2:
                logger.warning(f"修复后解析仍失败: {e2}")
                logger.info("尝试使用分割方式提取 proxies...")

                try:
                    lines = fixed_content.split("\n")
                    proxies_start = -1
                    proxies_end = -1

                    for i, line in enumerate(lines):
                        line_stripped = line.strip()
                        if line_stripped == "proxies:":
                            proxies_start = i
                        elif (
                            proxies_start != -1
                            and line_stripped
                            and not line_stripped.startswith("-")
                            and not line_stripped.startswith("  ")
                        ):
                            proxies_end = i
                            break

                    if proxies_end == -1:
                        proxies_end = len(lines)

                    if proxies_start != -1:
                        proxies_content = "\n".join(lines[proxies_start:proxies_end])
                        yaml_data = yaml.safe_load(proxies_content)
                        return yaml_data.get("proxies", [])
                except (yaml.YAMLError, KeyError) as e3:
                    logger.error(f"分割提取也失败了: {e3}")

            return []

    def process_proxies(self, proxies: list[ProxyDict], prefix: str = "rp") -> ProxyGroup:
        """处理代理列表, 按照 chrome_go_extractor 的方式分类"""
        proxies_by_protocol = {}
        group = ProxyGroup()

        for proxy in proxies:
            protocol = proxy.get("type", "unknown")
            if protocol == "unknown":
                continue

            if proxy.get("name") == "中国":
                continue

            if protocol not in proxies_by_protocol:
                proxies_by_protocol[protocol] = []

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
                    if p.get("name", "").startswith(f"{prefix}-{proxy['name']}-{protocol}-")
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

            if country in Config.PORN_COUNTRIES:
                group.porn_all.append(copy.deepcopy(proxy))

        return group

    @override
    def extract(self) -> ProxyGroup:
        """提取和处理 clash 文件"""
        logger.info("开始提取 ripao clash 配置...")

        if not self.input_file.exists():
            logger.error(f"文件不存在: {self.input_file}")
            return ProxyGroup()

        logger.info(f"读取文件: {self.input_file}")

        with self.input_file.open(encoding="utf-8") as f:
            content = f.read()

        proxies = self.load_and_fix_yaml(content)
        if not proxies:
            logger.error("提取 proxies 失败")
            return ProxyGroup()

        logger.info("转换代理配置...")

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False, encoding="utf-8", newline=""
        ) as temp_file:
            yaml.dump({"proxies": proxies}, temp_file)
            temp_file_path = Path(temp_file.name)

        try:
            converted_proxies = ProxyConverter.convert_clash_meta2(temp_file_path)
        finally:
            temp_file_path.unlink()

        if not converted_proxies:
            logger.error("转换代理失败")
            return ProxyGroup()

        logger.info("处理转换结果...")
        group = self.process_proxies(converted_proxies)

        logger.info(f"ripao 配置提取完成, 共 {len(group.all)} 个协议配置")
        return group
