#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import requests
import base64

class RipaoUpdater:
    def __init__(self):
        self.repo_url = "https://api.github.com/repos/ripaojiedian/freenode/contents/clash"
        self.ref = "main"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        self.data_dir = "data"
        self.temp_dir = "temp"
        self.sha_file = os.path.join(self.data_dir, "ripao_sha.txt")
        self.output_file = os.path.join(self.temp_dir, "ripao_clash.yaml")

        # 创建必要的目录
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

    def get_remote_file_info(self):
        """
        通过GitHub API获取clash文件的完整信息
        """
        try:
            params = {"ref": self.ref}
            response = requests.get(self.repo_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"获取GitHub文件信息失败: {e}")
            return None

    def get_local_sha(self):
        """
        从文件中读取上次的SHA
        """
        if os.path.exists(self.sha_file):
            with open(self.sha_file, "r", encoding="utf-8") as f:
                return f.read().strip()
        return None

    def save_sha(self, sha):
        """
        保存当前SHA到文件
        """
        with open(self.sha_file, "w", encoding="utf-8") as f:
            f.write(sha)

    def download_clash_file(self, download_url):
        """
        根据下载链接下载clash文件到指定位置
        """
        try:
            if not download_url:
                print("获取下载链接失败")
                return False

            # 下载文件内容
            response = requests.get(download_url, timeout=10)
            response.raise_for_status()
            content = response.text

            # 保存文件到temp目录
            with open(self.output_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"成功下载文件到 {self.output_file}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"下载文件失败: {e}")
            return False

    def update(self):
        """
        更新clash文件
        """
        print(f"[{datetime.now()}] 开始检查 ripao clash 文件更新...")

        # 获取文件信息（只请求一次API）
        remote_file_info = self.get_remote_file_info()
        if not remote_file_info:
            return False

        # 提取sha和download_url
        remote_sha = remote_file_info.get("sha")
        download_url = remote_file_info.get("download_url")

        if not remote_sha:
            print("获取SHA失败")
            return False

        # 获取本地SHA
        local_sha = self.get_local_sha()

        # 对比SHA，判断是否有更新
        if remote_sha == local_sha:
            print(f"[{datetime.now()}] ripao clash文件本地与远程相同，无需更新")
            return False

        print(f"[{datetime.now()}] ripao clash文件有更新，开始下载...")
        print(f"上次SHA: {local_sha}")
        print(f"当前SHA: {remote_sha}")

        # 下载文件
        if self.download_clash_file(download_url):
            # 更新本地SHA记录
            self.save_sha(remote_sha)
            print(f"[{datetime.now()}] ripao clash文件更新成功")
            return True
        else:
            print(f"[{datetime.now()}] ripao clash文件更新失败")
            return False

if __name__ == "__main__":
    RipaoUpdater().update()
