import os
import socket
import yaml
import geoip2.database
import requests

def get_country_from_ipapi(server):
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

        # 接口地址（lang=zh-CN 返回中文结果，fields限制返回必要字段）
        api_url = f"http://ip-api.com/json/{ip_address}?lang=zh-CN&fields=country,status,message"
        try:
            # 设置超时时间，避免网络阻塞
            response = requests.get(api_url, timeout=10)
            result = response.json()

            # 处理接口返回结果
            if result.get("status") != "success":
                print(f"ip-api 查询失败：{result.get('message', '未知错误')}")
            else:
                # 返回中文国家名称
                return result.get("country", "未知")
        except requests.exceptions.RequestException as e:
            print(f"ip-api 网络异常：{e}")
        except Exception as e:
            print(f"ip-api 解析异常：{e}")
        return "未知"

def get_country_from_mmdb(server):
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

def main():
    chromego_yaml = os.path.join("data", "chromego_proxies.yaml")
    with open(chromego_yaml, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
        for proxy in config["all"]:
            server = proxy["server"]
            country = get_country_from_ipapi(server)
            country2 = get_country_from_mmdb(server)
            print(f"{proxy['name']} server: {server} country: {country} / {country2}")

if __name__ == "__main__":
    main()
