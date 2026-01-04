import os
import yaml
from proxy_converter import ProxyConverter

class ChromeGoExtractor:
    def __init__(self):
        self.temp_dir = "temp"
        self.chrome_go_temp_dir = os.path.join(self.temp_dir, "ipupdate-master-backup-img-1-2-ipp", "backup", "img", "1", "2", "ipp")
        self.chrome_go_data_dir = os.path.join(self.temp_dir, "chrome_go")

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

        # 扫描所有配置
        for config in scan_configs:
            print(f"开始扫描 {config['dir']} 目录...")
            proxies = self.recursive_scan(config['dir'], config['filename'], config['parser'])

            # 按协议类型分类
            for proxy in proxies:
                protocol = proxy.get('type', 'unknown')
                # 跳过未知协议
                if protocol == 'unknown':
                    continue
                if protocol not in proxies_by_protocol:
                    proxies_by_protocol[protocol] = []
                # todo 过滤重复配置并重置 name
                # 如果 protocol 且 proxy['server'] 已存在就跳过，不存在将 proxy['name'] 设置为 protocol-proxy['name']-index
                if any(p['type'] == protocol and p['server'] == proxy['server'] for p in proxies_by_protocol[protocol]):
                    continue
                proxy['name'] = f"{protocol}-{proxy['name']}-{len(proxies_by_protocol[protocol])+1}"
                proxies_by_protocol[protocol].append(proxy)

        # 保存到对应的数据文件
        all_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"chromego.yaml")
        all_proxies = {
            'proxies': [],
        }
        for protocol, proxies in proxies_by_protocol.items():
            # 构建文件名
            filename = os.path.join(self.chrome_go_data_dir, f"{protocol}.yaml")

            # 保存为 yaml 格式
            with open(filename, 'w', encoding='utf-8') as f:
                yaml.dump(proxies, f, allow_unicode=True, default_flow_style=False)
            all_proxies['proxies'].extend(proxies)

            print(f"已保存 {len(proxies)} 个 {protocol} 协议配置到 {filename}")

        # 保存所有协议配置到 chromego.yaml
        with open(all_filename, 'w', encoding='utf-8') as f:
            yaml.dump(all_proxies, f, allow_unicode=True, default_flow_style=False)
        print(f"已保存所有 {len(all_proxies['proxies'])} 个协议配置到 {all_filename}")

    def run(self):
        """
        执行提取和转换操作
        """
        print("开始提取 chromego 配置...")
        # 检查目录是否存在
        if not os.path.exists(self.chrome_go_temp_dir):
            print(f"目录不存在: {self.chrome_go_temp_dir}")
            print("chromego 目录不存在，脚本停止")
            exit(1)
        self.extract_all_proxies()
        print("chromego 配置提取完成！")

if __name__ == "__main__":
    ChromeGoExtractor().run()
