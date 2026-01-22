#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import yaml
import copy

# 添加当前目录到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from chrome_go_updater import ChromeGoUpdater
from chrome_go_extractor import ChromeGoExtractor
from ripao_updater import RipaoUpdater
from ripao_extractor import RipaoExtractor

def main():
    """
    主函数：先更新ChromeGo配置，然后提取代理配置
    """
    hasUpdate = False
    data_dir = "data"
    chrome_go_proxies_filename = os.path.join(data_dir, "chromego_proxies.yaml")
    ripao_proxies_filename = os.path.join(data_dir, "ripao_proxies.yaml")

    if ChromeGoUpdater().update():
        ChromeGoExtractor().run()
        hasUpdate = True

    if RipaoUpdater().update():
        RipaoExtractor().run()
        hasUpdate = True

    if hasUpdate:
        print("检测到配置更新，重新生成...")
        chrome_proxies = yaml.safe_load(open(chrome_go_proxies_filename, 'r', encoding='utf-8'))
        ripao_proxies = yaml.safe_load(open(ripao_proxies_filename, 'r', encoding='utf-8'))

        # 合并所有协议配置
        all_proxies = {
            'all': copy.deepcopy(chrome_proxies['all']) + copy.deepcopy(ripao_proxies['all']),
            'udp': copy.deepcopy(chrome_proxies['udp']) + copy.deepcopy(ripao_proxies['udp']),
            'ai': copy.deepcopy(chrome_proxies['ai']) + copy.deepcopy(ripao_proxies['ai']),
            'udp_ai': copy.deepcopy(chrome_proxies['udp_ai']) + copy.deepcopy(ripao_proxies['udp_ai']),
            'porn_all': copy.deepcopy(chrome_proxies['porn_all']) + copy.deepcopy(ripao_proxies['porn_all']),
            'porn_x': copy.deepcopy(chrome_proxies['porn_x']) + copy.deepcopy(ripao_proxies['porn_x']),
        }

        if len(chrome_proxies['udp']) > 2:
            udp_proxies = copy.deepcopy(chrome_proxies['udp'])
        elif len(all_proxies['udp']) > 2:
            udp_proxies = copy.deepcopy(all_proxies['udp'])
        elif len(chrome_proxies['all']) > 2:
            udp_proxies = copy.deepcopy(chrome_proxies['all'])
        else:
            udp_proxies = copy.deepcopy(all_proxies['all'])

        # 保存 udp 协议配置到 udp.yaml
        with open('udp.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'proxies': copy.deepcopy(udp_proxies)}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        if len(all_proxies['udp_ai']) > 2:
            ai_proxies = copy.deepcopy(all_proxies['udp_ai'])
        elif len(all_proxies['ai']) > 2:
            ai_proxies = copy.deepcopy(all_proxies['ai'])
        else:
            ai_proxies = copy.deepcopy(all_proxies['udp_proxies'])

        # 保存 ai 协议配置到 ai.yaml
        with open('ai.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'proxies': copy.deepcopy(ai_proxies)}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        # 保存 porn_x 协议配置到 porn_x.yaml
        with open('porn_x.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'proxies': copy.deepcopy(all_proxies['porn_x'] + ripao_proxies['porn_x'])}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        # 保存 porn_all 协议配置到 porn_all.yaml
        with open('porn_all.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'proxies': copy.deepcopy(all_proxies['porn_all'] + ripao_proxies['porn_all'])}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        # 保存 all 协议配置到 all.yaml
        with open('all.yaml', 'w', encoding='utf-8') as f:
            yaml.dump({'proxies': copy.deepcopy(all_proxies['all'])}, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"已保存所有 {len(udp_proxies)} 个 UDP 协议配置到 udp.yaml")
        print(f"已保存所有 {len(ai_proxies)} 个 AI 协议配置到 ai.yaml")
        print(f"已保存所有 {len(all_proxies['porn_x'])} 个 porn_x 协议配置到 porn_x.yaml")
        print(f"已保存所有 {len(all_proxies['porn_all'])} 个 porn_all 协议配置到 porn_all.yaml")
        print(f"已保存所有 {len(all_proxies['all'])} 个协议配置到 all.yaml")
        print("配置更新完成")
    else:
        print("未检测到配置更新, 无需重新生成")

if __name__ == "__main__":
    main()
