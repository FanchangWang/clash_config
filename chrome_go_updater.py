from datetime import datetime
import os
from urllib.parse import quote
import zipfile

import requests

class ChromeGoUpdater:
    def __init__(self):
        self.project_id = "free9999/ipupdate"
        self.target_dir = "backup/img/1/2/ipp"
        self.data_dir = "data"
        self.chrome_go_date_file = os.path.join(self.data_dir, "chrome_go_date.txt")
        self.temp_dir = "temp"
        # 创建data目录
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
        # 创建temp目录
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)

    def __get_last_commit_time(self):
        """
        获取ChromeGo仓库指定目录的最后一次提交时间
        """
        # 通过 GitLab API 获取 ChromeGo 仓库指定目录的最后一次提交时间
        encoded_project_id = quote(self.project_id, safe='')
        url = f"https://gitlab.com/api/v4/projects/{encoded_project_id}/repository/commits"
        params = {
            "path": self.target_dir,
            "per_page": 1
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        commits = response.json()
        return commits[0]["created_at"]

    def __get_local_commit_time(self):
        """
        读取本地记录的ChromeGo仓库指定目录的最后一次提交时间
        """
        if os.path.exists(self.chrome_go_date_file):
            with open(self.chrome_go_date_file, "r") as f:
                local_time = f.read().strip()
            return local_time
        return ""

    def __save_last_commit_time(self, time):
        """
        保存ChromeGo仓库指定目录的最后一次提交时间到本地文件
        """
        with open(self.chrome_go_date_file, "w") as f:
            f.write(time)

    def __download_and_extract(self):
        """
        下载并解压ChromeGo仓库指定目录的内容
        """
        # 下载zip文件
        zip_url = f"https://gitlab.com/{self.project_id}/-/archive/master/ipupdate-master.zip"
        params = {
            "path": self.target_dir,
            "ref_type": "heads"
        }
        zip_path = os.path.join(self.temp_dir, "ipupdate.zip")
        response = requests.get(zip_url, params=params)
        response.raise_for_status()

        with open(zip_path, "wb") as f:
            f.write(response.content)

        # 解压所有文件
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.temp_dir)

        # 删除zip文件
        os.remove(zip_path)

    def update(self):
        """
        更新ChromeGo仓库指定目录的内容
        """
        try:
            # 获取 本地 与 远程 最后一次提交时间
            local_time = self.__get_local_commit_time()
            remote_time = self.__get_last_commit_time()
            # 如果 本地 最后一次提交时间 与 远程 最后一次提交时间 相同，则无需更新
            if local_time == remote_time:
                print(f"[{datetime.now()}] chrome_go 仓库 本地与远程相同，无需更新")
                return False

            print(f"[{datetime.now()}] 开始更新 chrome_go 仓库...")
            # 下载并解压ChromeGo仓库指定目录的内容
            self.__download_and_extract()

            # 写入最后提交时间到chrome_go_date.txt
            self.__save_last_commit_time(remote_time)

            print(f"[{datetime.now()}] chrome_go 仓库 更新成功")
            return True
        except Exception as e:
            print(f"[{datetime.now()}] chrome_go 仓库 更新失败: {e}")
            return False

if __name__ == "__main__":
    ChromeGoUpdater().update()
