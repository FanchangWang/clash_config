"""配置合并器"""

import copy

from .config import Config
from .logger import logger
from .models import ProxyGroup
from .utils import save_yaml


class Merger:
    """配置合并器"""

    def merge(self, chrome_group: ProxyGroup, ripao_group: ProxyGroup) -> None:
        """合并配置并生成输出文件到 dist 目录"""
        logger.info("检测到配置更新，重新生成...")

        all_proxies = {
            "all": copy.deepcopy(chrome_group.all) + copy.deepcopy(ripao_group.all),
            "udp": copy.deepcopy(chrome_group.udp) + copy.deepcopy(ripao_group.udp),
            "ai_gemini": copy.deepcopy(chrome_group.ai_gemini)
            + copy.deepcopy(ripao_group.ai_gemini),
            "porn_all": copy.deepcopy(chrome_group.porn_all) + copy.deepcopy(ripao_group.porn_all),
            "porn_x": copy.deepcopy(chrome_group.porn_x) + copy.deepcopy(ripao_group.porn_x),
        }

        if len(chrome_group.udp) > 2:
            udp_proxies = copy.deepcopy(chrome_group.udp)
        elif len(all_proxies["udp"]) > 2:
            udp_proxies = copy.deepcopy(all_proxies["udp"])
        elif len(chrome_group.all) > 2:
            udp_proxies = copy.deepcopy(chrome_group.all)
        else:
            udp_proxies = copy.deepcopy(all_proxies["all"])

        save_yaml({"proxies": udp_proxies}, Config.DIST_PROXIES_DIR / "udp.yaml")
        logger.info(f"已保存所有 {len(udp_proxies)} 个 UDP 协议配置到 dist/proxies/udp.yaml")

        if len(all_proxies["ai_gemini"]) > 2:
            ai_gemini_proxies = copy.deepcopy(all_proxies["ai_gemini"])
        else:
            ai_gemini_proxies = copy.deepcopy(all_proxies["all"])

        save_yaml(
            {"proxies": ai_gemini_proxies},
            Config.DIST_PROXIES_DIR / "ai_gemini.yaml",
        )
        logger.info(
            f"已保存所有 {len(ai_gemini_proxies)} 个 AI gemini 协议配置到"
            f" dist/proxies/ai_gemini.yaml"
        )

        save_yaml(
            {"proxies": all_proxies["porn_x"]},
            Config.DIST_PROXIES_DIR / "porn_x.yaml",
        )
        logger.info(
            f"已保存所有 {len(all_proxies['porn_x'])} 个 porn_x 协议配置到 dist/proxies/porn_x.yaml"
        )

        save_yaml(
            {"proxies": all_proxies["porn_all"]},
            Config.DIST_PROXIES_DIR / "porn_all.yaml",
        )
        logger.info(
            f"已保存所有 {len(all_proxies['porn_all'])} 个 porn_all 协议配置到"
            f" dist/proxies/porn_all.yaml"
        )

        save_yaml(
            {"proxies": all_proxies["all"]},
            Config.DIST_PROXIES_DIR / "all.yaml",
        )
        logger.info(f"已保存所有 {len(all_proxies['all'])} 个协议配置到 dist/proxies/all.yaml")

        logger.info("配置更新完成")
