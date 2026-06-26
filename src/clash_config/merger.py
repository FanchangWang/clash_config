"""配置合并器"""

import copy
import textwrap

import yaml

from .config import Config
from .logger import logger
from .models import ProxyDict, ProxyGroup


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
        lines.append('    url: "https://www.google.com/generate_204"')
        lines.append("    interval: 0")
        lines.append("    timeout: 5000")
        lines.append("    lazy: false")

        lines.append("")
        lines.append('  - name: "_p_udp"')
        lines.append("    type: load-balance")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["udp"]))
        lines.append("    strategy: sticky-sessions")

        lines.append("")
        lines.append('  - name: "_p_ai_gemini"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["ai_gemini"]))

        lines.append("")
        lines.append('  - name: "_p_porn_x"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["porn_x"]))

        lines.append("")
        lines.append('  - name: "_p_porn_all"')
        lines.append("    type: url-test")
        lines.append("    proxies:")
        lines.extend(f'      - "{name}"' for name in self._proxy_names(all_data["porn_all"]))

        return "\n".join(lines)

    def merge(self, chrome_group: ProxyGroup, ripao_group: ProxyGroup) -> None:
        """合并配置并生成 dist/config.yaml"""
        logger.info("检测到配置更新, 重新生成...")

        merged = {
            "all": copy.deepcopy(chrome_group.all) + copy.deepcopy(ripao_group.all),
            "udp": copy.deepcopy(chrome_group.udp) + copy.deepcopy(ripao_group.udp),
            "ai_gemini": copy.deepcopy(chrome_group.ai_gemini)
            + copy.deepcopy(ripao_group.ai_gemini),
            "porn_all": copy.deepcopy(chrome_group.porn_all) + copy.deepcopy(ripao_group.porn_all),
            "porn_x": copy.deepcopy(chrome_group.porn_x) + copy.deepcopy(ripao_group.porn_x),
        }

        all_data: dict[str, list[ProxyDict]] = dict(merged)

        if len(chrome_group.udp) > 2:
            udp_proxies = copy.deepcopy(chrome_group.udp)
        elif len(merged["udp"]) > 2:
            udp_proxies = copy.deepcopy(merged["udp"])
        elif len(chrome_group.all) > 2:
            udp_proxies = copy.deepcopy(chrome_group.all)
        else:
            udp_proxies = copy.deepcopy(merged["all"])
        all_data["udp"] = udp_proxies

        if len(merged["ai_gemini"]) > 2:
            all_data["ai_gemini"] = copy.deepcopy(merged["ai_gemini"])
        else:
            all_data["ai_gemini"] = copy.deepcopy(merged["all"])

        template = (Config.TEMPLATE_DIR / "config.yaml").read_text(encoding="utf-8")

        proxies_yaml = yaml.dump(
            all_data["all"],
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        proxies_yaml = textwrap.indent(proxies_yaml, "  ")

        groups_yaml = self._build_dynamic_groups(all_data)

        result = template.replace("{{PROXIES}}", proxies_yaml)
        result = result.replace("{{DYNAMIC_GROUPS}}", groups_yaml)

        output = Config.DIST_DIR / "config.yaml"
        output.write_text(result, encoding="utf-8", newline="")
        logger.info(f"已生成 {output}")
