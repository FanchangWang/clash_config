#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import tempfile
from proxy_converter import ProxyConverter

class RipaoExtractor:
    def __init__(self):
        self.temp_dir = "temp"
        self.data_dir = "data"
        self.input_file = os.path.join(self.temp_dir, "ripao_clash.yaml")
        self.output_file = os.path.join(self.data_dir, "ripao_proxies.yaml")

        # 创建必要的目录
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def load_and_fix_yaml(self, content):
        """
        加载yaml内容并提取proxies字段，自动修复格式问题
        优先直接读取，失败后尝试修复，修复后再次读取
        """
        try:
            # 优先直接尝试标准加载
            print("尝试直接读取YAML内容...")
            yaml_data = yaml.safe_load(content)
            return yaml_data.get("proxies", [])
        except yaml.YAMLError as e:
            print(f"解析YAML内容失败: {e}")
            print("尝试修复YAML格式...")

            # 修复YAML格式问题
            lines = content.split('\n')
            fixed_lines = []
            in_proxies_section = False

            for line in lines:
                stripped_line = line.strip()

                # 检查是否进入proxies部分
                if stripped_line == 'proxies:':
                    in_proxies_section = True
                    fixed_lines.append(line)
                    continue

                # 检查是否离开proxies部分
                if in_proxies_section and stripped_line and not stripped_line.startswith('-') and not stripped_line.startswith('  '):
                    in_proxies_section = False

                # 在proxies部分中修复格式问题
                if in_proxies_section and stripped_line.startswith('- {'):
                    # 检查行是否缺少闭合括号
                    if '{' in stripped_line and '}' not in stripped_line:
                        print(f"修复行: {line}")
                        # 添加闭合括号
                        line = line.rstrip() + '}'

                fixed_lines.append(line)

            fixed_content = '\n'.join(fixed_lines)

            # 修复后再次尝试读取
            try:
                print("修复后再次尝试读取YAML...")
                yaml_data = yaml.safe_load(fixed_content)
                return yaml_data.get("proxies", [])
            except yaml.YAMLError as e2:
                print(f"修复后解析仍失败: {e2}")
                print("尝试使用分割方式提取proxies...")

                # 尝试直接分割内容，寻找proxies部分
                try:
                    lines = fixed_content.split('\n')
                    proxies_start = -1
                    proxies_end = -1

                    for i, line in enumerate(lines):
                        line_stripped = line.strip()
                        if line_stripped == 'proxies:':
                            proxies_start = i
                        elif proxies_start != -1 and line_stripped and not line_stripped.startswith('-') and not line_stripped.startswith('  '):
                            proxies_end = i
                            break

                    if proxies_end == -1:
                        proxies_end = len(lines)

                    if proxies_start != -1:
                        proxies_content = '\n'.join(lines[proxies_start:proxies_end])
                        yaml_data = yaml.safe_load(proxies_content)
                        return yaml_data.get("proxies", [])
                except Exception as e3:
                    print(f"分割提取也失败了: {e3}")

            return []

    def process_proxies(self, proxies):
        """
        处理代理列表，按照chrome_go_extractor.py的方式分类
        """
        import copy

        # 按协议类型存储结果
        proxies_by_protocol = {}
        # 存储所有代理节点
        processed_proxies = {
            'all': [],  # 所有协议配置
            'udp': [],  # 所有UDP代理节点
            'ai': [],  # 所有AI代理节点
            'udp_ai': [],  # 所有UDP AI代理节点
            'porn_x': [],  # porn x.com 代理节点
            'porn_all': [],  # porn 所有代理节点
        }

        # 按协议类型分类
        for proxy in proxies:
            protocol = proxy.get('type', 'unknown')
            # 跳过未知协议
            if protocol == 'unknown':
                continue
            # 排除大陆代理节点 # 保留了香港与台湾节点
            if proxy['name'] == '中国':
                continue
            # 初始化协议类型列表
            if protocol not in proxies_by_protocol:
                proxies_by_protocol[protocol] = []
            # 排除重复代理节点
            if any(p['type'] == protocol and p['server'] == proxy['server'] and p.get('port') == proxy.get('port') and p.get('ports') == proxy.get('ports') for p in proxies_by_protocol[protocol]):
                continue
            # 统计同一协议下相同名称的代理数量
            count = sum(1 for p in proxies_by_protocol[protocol] if p.get('name', '').startswith(f"rp-{proxy['name']}-{protocol}-")) + 1
            country = proxy['name']

            # 创建代理对象的深拷贝，避免PyYAML生成锚点
            proxy['name'] = f"rp-{country}-{protocol}-{count}"

            proxies_by_protocol[protocol].append(copy.deepcopy(proxy))

            # 加入所有代理节点（使用深拷贝）
            processed_proxies['all'].append(copy.deepcopy(proxy))

            # country 判断是否为 AI 合法国家，加入 AI 节点
            if country in ['日本', '韩国', '台湾', '荷兰', '法国', '德国', '新加坡', '印度', '马来西亚', '泰国', '越南', '印度尼西亚', '菲律宾']:
                processed_proxies['ai'].append(copy.deepcopy(proxy))
                # 判断是否为 UDP AI 节点
                if protocol in ['hysteria', 'hysteria2', 'tuic']:
                    processed_proxies['udp_ai'].append(copy.deepcopy(proxy))

            # protocal 为 hysteria|hysteria2|tuic 时，加入UDP代理节点
            if protocol in ['hysteria', 'hysteria2', 'tuic']:
                processed_proxies['udp'].append(copy.deepcopy(proxy))

            # country 判断是否为 porn 合法国家，加入 porn 节点
            if country in ['美国', '日本', '韩国', '香港', '台湾', '荷兰', '德国']:
                processed_proxies['porn_all'].append(copy.deepcopy(proxy))
                if country not in ['德国']:  # 排除 x.com 不允许的节点
                    processed_proxies['porn_x'].append(copy.deepcopy(proxy))

        return processed_proxies

    def extract(self):
        """
        提取和处理clash文件
        """
        print("开始提取 ripao clash 配置...")

        # 检查输入文件是否存在
        if not os.path.exists(self.input_file):
            print(f"输入文件不存在: {self.input_file}")
            print("请先运行ripao_updater.py下载文件")
            return False

        print(f"读取文件: {self.input_file}")

        # 读取文件内容
        with open(self.input_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 加载yaml内容并提取proxies，自动修复格式问题
        proxies = self.load_and_fix_yaml(content)
        if not proxies:
            print("提取proxies失败")
            return False

        # 使用ProxyConverter.convert_clash_meta2转换代理
        print("转换代理配置...")

        # 创建临时文件来存储proxies
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False, encoding='utf-8') as temp_file:
            yaml.dump({"proxies": proxies}, temp_file)
            temp_file_path = temp_file.name

        try:
            converted_proxies = ProxyConverter.convert_clash_meta2(temp_file_path)
        finally:
            os.unlink(temp_file_path)

        if not converted_proxies:
            print("转换代理失败")
            return False

        # 按照chrome_go_extractor.py的方式处理转换结果
        print("处理转换结果...")
        processed_proxies = self.process_proxies(converted_proxies)

        # 保存结果到ripao_proxies.yaml
        print(f"保存结果到 {self.output_file}...")
        with open(self.output_file, 'w', encoding='utf-8') as f:
            yaml.dump(processed_proxies, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

        print(f"已保存所有 {len(processed_proxies['all'])} 个协议配置到 {self.output_file}")
        return True

    def run(self):
        """
        执行提取和转换操作
        """
        print("开始执行ripao clash提取操作...")
        if self.extract():
            print("ripao clash提取操作完成！")
        else:
            print("ripao clash提取操作失败！")

if __name__ == "__main__":
    RipaoExtractor().run()
