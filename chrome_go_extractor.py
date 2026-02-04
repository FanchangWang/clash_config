import os

import yaml

from proxy_converter import ProxyConverter

class ChromeGoExtractor:
    def __init__(self):
        self.temp_dir = "temp"
        self.chrome_go_temp_dir = os.path.join(self.temp_dir, "ipupdate-master-backup-img-1-2-ipp", "backup", "img", "1", "2", "ipp")
        self.chrome_go_data_dir = os.path.join(self.temp_dir, "chrome_go")
        self.data_dir = "data"
        self.chrome_proxies_filename =  os.path.join(self.data_dir, "chromego_proxies.yaml")

        # 确保 chrome_go_data_dir 目录存在
        if not os.path.exists(self.chrome_go_data_dir):
            os.makedirs(self.chrome_go_data_dir, exist_ok=True)
        else:
            # 清空 chrome_go_data_dir 目录
            for file_name in os.listdir(self.chrome_go_data_dir):
                file_path = os.path.join(self.chrome_go_data_dir, file_name)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"删除文件失败: {file_path}, 错误: {e}")


    def recursive_scan(self, scan_dir, config_filename, parse_func):
        """
        递归扫描目录，匹配配置文件名，并使用指定的解析函数解析

        Args:
            scan_dir: 要递归扫描的目录名（相对于 chrome_go_temp_dir
            config_filename: 要匹配的配置文件名
            parse_func: 解析配置文件的函数

        Returns:
            list: 解析后的配置列表
        """
        full_scan_dir = os.path.join(self.chrome_go_temp_dir, scan_dir)
        results = []

        if not os.path.exists(full_scan_dir):
            print(f"扫描目录不存在: {full_scan_dir}")
            return results

        # 递归扫描目录
        for root, dirs, files in os.walk(full_scan_dir):
            for file in files:
                if file == config_filename:
                    config_path = os.path.join(root, file)
                    print(f"\n配置文件: {config_path}")

                    # 使用解析函数解析配置
                    parsed_config = parse_func(config_path)
                    if parsed_config:
                        # 如果解析结果是列表，直接扩展，否则添加单个元素
                        if isinstance(parsed_config, list):
                            results.extend(parsed_config)
                        else:
                            results.append(parsed_config)

        return results

    def extract_all_proxies(self):
        """
        提取所有代理配置
        """
        # 定义要扫描的目录和对应的配置文件名及解析方法
        scan_configs = [
            {'dir': 'clash.meta2', 'filename': 'config.yaml', 'parser': ProxyConverter.convert_clash_meta2},
            {'dir': 'hysteria', 'filename': 'config.json', 'parser': ProxyConverter.convert_hysteria},
            {'dir': 'hysteria2', 'filename': 'config.json', 'parser': ProxyConverter.convert_hysteria2},
            {'dir': 'mieru', 'filename': 'config.json', 'parser': ProxyConverter.convert_mieru},
            {'dir': 'xray', 'filename': 'config.json', 'parser': ProxyConverter.convert_xray},
        ]

        # 按协议类型存储结果
        proxies_by_protocol = {}
        # 存储所有代理节点
        chrome_proxies = {
            'all': [], # 所有协议配置
            'udp': [], # 所有UDP代理节点
            'ai': [], # 所有AI代理节点
            'udp_ai': [], # 所有UDP AI代理节点
            'porn_x': [], # porn x.com 代理节点
            'porn_all': [], # porn 所有代理节点
        } # 所有协议配置

        import copy

        # 扫描所有配置
        for config in scan_configs:
            print(f"\n开始扫描 {config['dir']} 目录...")
            proxies = self.recursive_scan(config['dir'], config['filename'], config['parser'])

            # 按协议类型分类
            for proxy in proxies:
                protocol = proxy.get('type', 'unknown')
                # 跳过未知协议
                if protocol == 'unknown':
                    continue
                if protocol not in proxies_by_protocol:
                    proxies_by_protocol[protocol] = []
                # 排除大陆代理节点 # 保留了香港与台湾节点
                if proxy['name'] == '中国':
                    continue
                # 排除重复代理节点
                if any(p['type'] == protocol and p['server'] == proxy['server'] and p.get('port') == proxy.get('port') and p.get('ports') == proxy.get('ports') for p in proxies_by_protocol[protocol]):
                    continue
                # 统计同一协议下相同名称的代理数量
                count = sum(1 for p in proxies_by_protocol[protocol] if p.get('name', '').startswith(f"go-{proxy['name']}-{protocol}-")) + 1
                country = proxy['name']
                proxy['name'] = f"go-{country}-{protocol}-{count}"
                proxies_by_protocol[protocol].append(copy.deepcopy(proxy))
                # 加入所有代理节点
                chrome_proxies['all'].append(copy.deepcopy(proxy))
                # country 判断是否为 AI 合法国家，加入 AI 节点
                if country in ['日本', '韩国', '台湾', '荷兰', '法国', '德国', '新加坡', '印度', '马来西亚', '泰国', '越南', '印度尼西亚', '菲律宾']:
                    chrome_proxies['ai'].append(copy.deepcopy(proxy))
                    # 判断是否为 UDP AI 节点
                    if protocol in ['hysteria', 'hysteria2', 'tuic']:
                        chrome_proxies['udp_ai'].append(copy.deepcopy(proxy))
                # protocal 为 hysteria|hysteria2|tuic 时，加入UDP代理节点
                if protocol in ['hysteria', 'hysteria2', 'tuic']:
                    chrome_proxies['udp'].append(copy.deepcopy(proxy))
                # config['dir'] == hysteria2 时，允许 porn
                if config['dir'] == 'hysteria2':
                    # country 判断是否为 porn 合法国家，加入 porn 节点
                    if country in ['美国', '日本', '韩国', '香港', '台湾', '荷兰', '德国']:
                        chrome_proxies['porn_all'].append(copy.deepcopy(proxy))
                        if country not in ['德国']: # 排除 x.com 不允许的节点
                            chrome_proxies['porn_x'].append(copy.deepcopy(proxy))

        # 保存所有协议配置到 chromego.yaml
        with open(self.chrome_proxies_filename, 'w', encoding='utf-8') as f:
            yaml.dump(chrome_proxies, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"已保存所有 {len(chrome_proxies['all'])} 个协议配置到 {self.chrome_proxies_filename}")

    def run(self):
        """
        执行提取和转换操作
        """
        print("开始提取 chromego 配置...")
        # 检查目录是否存在
        if not os.path.exists(self.chrome_go_temp_dir):
            print(f"目录不存在: {self.chrome_go_temp_dir}")
            print("chromego 目录不存在，脚本停止!")
        else:
            self.extract_all_proxies()
            print("chromego 配置提取完成！")

if __name__ == "__main__":
    ChromeGoExtractor().run()
