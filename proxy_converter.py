import json
import os
import re
import socket

import geoip2.database
import yaml

class ProxyConverter:
    """
    代理协议转换类，用于将各种协议转换为 mihomo 协议格式
    支持的协议：hysteria2、hysteria、clash.meta2、mieru、quick、singbox(vmess/vless)、xray(vmess/vless)
    根据最新的 mihomo proxies 配置文档优化
    """

    @staticmethod
    def _get_geoip_country(server):
        """
        获取 IP 地址的国家名称（中文）

        Args:
            server: 服务器地址字符串

        Returns:
            str: 国家名称（中文），如果未找到则返回 未知
        """

        try:
            ip_address = socket.gethostbyname(server)
        except socket.gaierror:
            ip_address = server

        try:
            data_dir = "data"
            mmdb_file = os.path.join(data_dir, "GeoLite2-Country.mmdb")
            if not os.path.exists(mmdb_file):
                return "未知"
            response = geoip2.database.Reader(mmdb_file).country(ip_address)
            return response.country.names.get('zh-CN', response.country.name)
        except geoip2.errors.AddressNotFoundError:
            return "未知"

    @staticmethod
    def _parse_hysteria_server_address(server):
        """
        解析服务器地址，处理各种格式（IPv4、IPv6、域名，以及复杂的端口格式）

        Args:
            server: 服务器地址字符串，格式可以是：
                   - host:port
                   - [IPv6]:port
                   - host (默认端口 443)
                   - host:port,port-range

        Returns:
            tuple: (server_addr, port, ports, is_multi_port)
        """
        server_addr = server
        port = 443
        ports = None
        is_multi_port = False

        # 先检查是否是 IPv6 地址格式 [IPv6]:port
        ipv6_match = re.match(r'^\[([0-9a-fA-F:.]+)\]:(.+)$', server)
        if ipv6_match:
            server_addr = f"[{ipv6_match.group(1)}]"
            port_part = ipv6_match.group(2)

            # 总是从端口部分提取第一个端口作为 port
            first_port_match = re.search(r'^(\d+)', port_part)
            if first_port_match:
                port = int(first_port_match.group(1))

            # 检查是否包含端口范围或多个端口
            if ',' in port_part or '-' in port_part:
                ports = port_part
                is_multi_port = True
            else:
                is_multi_port = False
        else:
            # 检查是否是 IPv4 地址或域名:port 格式
            ipv4_or_domain_match = re.match(r'^([^:]+):(.+)$', server)
            if ipv4_or_domain_match:
                server_addr = ipv4_or_domain_match.group(1)
                port_part = ipv4_or_domain_match.group(2)

                # 总是从端口部分提取第一个端口作为 port
                first_port_match = re.search(r'^(\d+)', port_part)
                if first_port_match:
                    port = int(first_port_match.group(1))

                # 检查是否包含端口范围或多个端口
                if ',' in port_part or '-' in port_part:
                    ports = port_part
                    is_multi_port = True
                else:
                    is_multi_port = False
            else:
                # 只有 host，没有端口，默认使用443
                server_addr = server
                port = 443
                is_multi_port = False

        return server_addr, port, ports, is_multi_port

    @staticmethod
    def convert_hysteria(config_file):
        """
        将 hysteria 配置转换为 mihomo 格式
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 解析 hysteria 解析服务器地址
            server = config.get('server', '')
            server_addr, port, ports, is_multi_port = ProxyConverter._parse_hysteria_server_address(server)
            country = ProxyConverter._get_geoip_country(server_addr)

            # 构建 mihomo 格式
            mihomo_config = {
                'name': country,
                'type': 'hysteria',
                'server': server_addr,
                'protocol': config.get('protocol', ''),
                'port': port,
                'auth-str': config.get('auth_str', ''),
                'sni': config.get('server_name', ''),
                'alpn': config.get('alpn', []),
                'up': config.get('up_mbps', ''),
                'down': config.get('down_mbps', ''),
                'skip-cert-verify': config.get('insecure', False),
                'fast-open': config.get('fast_open', False),
                'recv-window-conn': config.get('recv_window_conn', 12582912),
                'recv-window': config.get('recv_window', 52428800),
                'disable-mtu-discovery': config.get('disable_mtu_discovery', False)
            }

            # 如果是多端口，添加 ports 字段
            if is_multi_port:
                mihomo_config['ports'] = ports

            print("配置内容:")
            print(mihomo_config)

            return mihomo_config
        except Exception as e:
            print(f"转换 hysteria 配置失败: {e}")
            return None

    @staticmethod
    def convert_hysteria2(config_file):
        """
        将 hysteria2 配置转换为 mihomo 格式
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 解析 hysteria2 配置
            server = config.get('server', '')
            auth = config.get('auth', '')
            tls_config = config.get('tls', {})
            sni = tls_config.get('sni', '')
            bandwidth = config.get('bandwidth', {})

            # 解析服务器地址
            server_addr, port, ports, is_multi_port = ProxyConverter._parse_hysteria_server_address(server)
            country = ProxyConverter._get_geoip_country(server_addr)

            # 构建 mihomo 格式
            mihomo_config = {
                'name': country,
                'type': 'hysteria2',
                'server': server_addr,
                'port': port,
                'password': auth,
                'sni': sni,
                'skip-cert-verify': tls_config.get('insecure', True)
            }

            # 如果是多端口，添加 ports 字段
            if is_multi_port:
                mihomo_config['ports'] = ports

            # 添加带宽配置（如果存在）
            if bandwidth:
                up_mbps = bandwidth.get('up', '')
                down_mbps = bandwidth.get('down', '')
                if up_mbps:
                    mihomo_config['up'] = up_mbps
                if down_mbps:
                    mihomo_config['down'] = down_mbps

            print("配置内容:")
            print(mihomo_config)

            return mihomo_config
        except Exception as e:
            print(f"转换 hysteria2 配置失败: {e}")
            return None

    @staticmethod
    def convert_clash_meta2(config_file):
        """
        将 clash.meta2 配置转换为 mihomo 格式
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)

            # 解析 clash.meta2 配置
            proxies = config.get('proxies', [])

            # 确保返回的代理配置符合最新的 mihomo 格式
            mihomo_proxies = []
            for proxy in proxies:
                # 保留原始配置，确保它符合 mihomo 格式
                proxy['name'] = ProxyConverter._get_geoip_country(proxy['server'])
                print("\n配置内容:")
                print(proxy)
                mihomo_proxies.append(proxy)

            return mihomo_proxies
        except Exception as e:
            print(f"转换 clash.meta2 配置失败: {e}")
            return []

    @staticmethod
    def convert_mieru(config_file):
        """
        将 mieru 配置转换为 mihomo 格式
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            mihomo_proxies = []
            # 解析 mieru 配置
            profiles = config.get('profiles', [])
            for profile in profiles:
                user = profile.get('user', {})
                username = user.get('name', '')
                password = user.get('password', '')
                servers = profile.get('servers', [])
                for server in servers:
                    address = server.get('ipAddress', '')
                    country = ProxyConverter._get_geoip_country(address)
                    portBindings = server.get('portBindings', [])
                    for portBinding in portBindings:
                        port = portBinding.get('port', '443')
                        portRange = portBinding.get('portRange', '')
                        protocol = portBinding.get('protocol', 'TCP')
                        # 构建 mihomo 格式
                        mihomo_proxy = {
                            'name': f'mieru-{country}',
                            'type': 'mieru',
                            'server': address,
                            'transport': protocol.upper(),
                            'udp': True,
                            'username': username,
                            'password': password,
                        }
                        if portRange:
                            mihomo_proxy['portRange'] = portRange
                        else:
                            mihomo_proxy['port'] = port
                        print("\n配置内容:")
                        print(mihomo_proxy)
                        mihomo_proxies.append(mihomo_proxy)

            return mihomo_proxies
        except Exception as e:
            print(f"转换 mieru 配置失败: {e}")
            return []

    @staticmethod
    def convert_xray(config_file):
        """
        将 xray 配置转换为 mihomo 格式
        """
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 解析 xray 配置
            outbounds = config.get('outbounds', [])
            mihomo_proxies = []

            for outbound in outbounds:
                protocol = outbound.get('protocol', '')
                # 只保留 trojan vless vmess 协议
                if protocol not in ['trojan', 'vless', 'vmess']:
                    continue

                # 传输层配置
                streamSettings = outbound.get('streamSettings', {})
                xray_security = streamSettings.get('security', '')
                if xray_security != 'reality':
                    continue # 只支持 reality 加密
                realitySettings = streamSettings.get('realitySettings', {})
                transport_config = {
                    'tls': True,
                    'udp': True,
                    'sni': realitySettings.get('serverName', ''),
                    'servername': realitySettings.get('serverName', ''),
                    'client-fingerprint': realitySettings.get('fingerprint', ''),
                    "reality-opts": {
                        "public-key": realitySettings.get('publicKey', ''),
                        "short-id": realitySettings.get('shortId', '')
                    },
                }
                xray_network = streamSettings.get('network', 'tcp')
                if xray_network == 'raw' or xray_network == 'tcp':
                    transport_config.update({
                        'network': 'tcp',
                    })
                elif xray_network == 'xhttp':
                    transport_config.update({
                        'network': 'http',
                        'http-opts': {
                            'path': streamSettings.get('xhttpSettings', {}).get('path', '/'),
                        }
                    })
                elif xray_network == 'grpc':
                    transport_config.update({
                        'network': 'grpc',
                        'grpc-opts': {
                            'grpc-service-name': streamSettings.get('grpcSettings', {}).get('serviceName', ''),
                        }
                    })
                else:
                    continue # 其他网络类型暂不支持

                settings = outbound.get('settings', {})

                if protocol == 'vless':
                    vnext = settings.get('vnext', [])

                    for v in vnext:
                        address = v.get('address', '')
                        country = ProxyConverter._get_geoip_country(address)
                        port = v.get('port', 443)
                        users = v.get('users', [])

                        for user in users:
                            # 以 transport_config 为基础构建 mihomo 格式
                            mihomo_proxy = transport_config.copy()
                            mihomo_proxy.update({
                                'name': country,
                                'type': 'vless',
                                'server': address,
                                'port': port,
                                'uuid': user.get('id', ''),
                                'flow': user.get('flow', ''),
                                'encryption': user.get('encryption', ''),
                                'skip-cert-verify': True
                            })
                            print("\n配置内容:")
                            print(mihomo_proxy)
                            mihomo_proxies.append(mihomo_proxy)

                elif protocol == 'vmess':
                    vnext = settings.get('vnext', [])

                    for v in vnext:
                        address = v.get('address', '')
                        country = ProxyConverter._get_geoip_country(address)
                        port = v.get('port', 443)
                        users = v.get('users', [])

                        for user in users:
                            # 以 transport_config 为基础构建 mihomo 格式
                            mihomo_proxy = transport_config.copy()
                            mihomo_proxy.update({
                                'name': country,
                                'type': 'vmess',
                                'server': address,
                                'port': port,
                                'uuid': user.get('id', ''),
                                'alterId': user.get('alterId', 0),
                                'cipher': user.get('security', 'auto'),
                            })
                            print("\n配置内容:")
                            print(mihomo_proxy)
                            mihomo_proxies.append(mihomo_proxy)

                elif protocol == 'trojan':
                    servers = settings.get('servers', [])

                    for server in servers:
                        address = server.get('address', '')
                        country = ProxyConverter._get_geoip_country(address)
                        port = server.get('port', 443)
                        password = server.get('password', '')

                        # 以 transport_config 为基础构建 mihomo 格式
                        mihomo_proxy = transport_config.copy()
                        mihomo_proxy.update({
                            'name': country,
                            'type': 'trojan',
                            'server': address,
                            'port': port,
                            'password': password,
                            'skip-cert-verify': True
                        })
                        print("\n配置内容:")
                        print(mihomo_proxy)
                        mihomo_proxies.append(mihomo_proxy)

            return mihomo_proxies
        except Exception as e:
            print(f"转换 xray 配置失败: {e}")
            return []
