"""配置合并器"""

import copy
import textwrap

from .config import Config
from .logger import logger
from .models import ProxyDict, ProxyGroup
from .utils import dump_yaml


class Merger:
    """配置合并器"""

    def _proxy_names(self, proxies: list[ProxyDict]) -> list[str]:
        return [p["name"] for p in proxies]

    def _build_dynamic_groups(self, all_data: dict[str, list[ProxyDict]]) -> str:
        lines: list[str] = []

        lines.append('  - name: "Sall"')
        lines.append("    type: select")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["all"]))

        lines.append("")
        lines.append('  - name: "_p_udp"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["udp"]))
        lines.append('    url: "https://www.google.com/generate_204"')
        lines.append("    interval: 3600")
        lines.append("    timeout: 5000")
        lines.append("    lazy: false")

        lines.append("")
        lines.append('  - name: "_p_ai_gemini"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["ai_gemini"]))
        lines.append('    url: "https://www.google.com/generate_204"')
        lines.append("    interval: 3600")
        lines.append("    timeout: 5000")
        lines.append("    lazy: true")

        lines.append("")
        lines.append('  - name: "_p_porn_x"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["porn_x"]))
        lines.append('    url: "https://www.google.com/generate_204"')
        lines.append("    interval: 3600")
        lines.append("    timeout: 5000")
        lines.append("    lazy: true")

        lines.append("")
        lines.append('  - name: "_p_porn_all"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["porn_all"]))
        lines.append('    url: "https://www.google.com/generate_204"')
        lines.append("    interval: 3600")
        lines.append("    timeout: 5000")
        lines.append("    lazy: true")

        return "\n".join(lines)

    def merge(self, group: ProxyGroup) -> None:
        """合并配置并生成 dist/config.yaml"""
        logger.info("检测到配置更新, 重新生成...")

        all_data: dict[str, list[ProxyDict]] = {
            "all": copy.deepcopy(group.all),
            "udp": copy.deepcopy(group.udp) if len(group.udp) > 2 else copy.deepcopy(group.all),
            "ai_gemini": copy.deepcopy(group.ai_gemini)
            if len(group.ai_gemini) > 2
            else copy.deepcopy(group.all),
            "porn_all": copy.deepcopy(group.porn_all),
            "porn_x": copy.deepcopy(group.porn_x),
        }

        template = (Config.TEMPLATE_DIR / "config.yaml").read_text(encoding="utf-8")

        proxies_yaml = dump_yaml(all_data["all"])
        proxies_yaml = textwrap.indent(proxies_yaml, "  ")

        groups_yaml = self._build_dynamic_groups(all_data)

        result = template.replace("{{PROXIES}}", proxies_yaml)
        result = result.replace("{{DYNAMIC_GROUPS}}", groups_yaml)

        output = Config.DIST_DIR / "config.yaml"
        output.write_text(result, encoding="utf-8", newline="")
        logger.info(f"已生成 {output}")
