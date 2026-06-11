"""ChromeGo 更新器"""

import zipfile
from typing import override
from urllib.parse import quote

import httpx

from ..config import Config
from ..extractor.chrome_go import ChromeGoExtractor
from ..logger import logger
from ..models import ProxyGroup
from ..utils import load_yaml, save_yaml
from .base import BaseUpdater


class ChromeGoUpdater(BaseUpdater):
    """ChromeGo 仓库更新器"""

    source_name = "chrome_go"

    def __init__(self) -> None:
        super().__init__()
        self.project_id = Config.CHROME_GO_PROJECT_ID
        self.target_dir = Config.CHROME_GO_TARGET_DIR
        self._remote_created_at = ""

    def _get_local_created_at(self) -> str:
        """获取本地记录的创建时间"""
        return self.store.chrome_go.created_at

    @override
    def check_update(self) -> bool:
        """检查是否有更新"""
        try:
            logger.info("开始检查 chrome_go 仓库更新...")

            encoded_project_id = quote(self.project_id, safe="")
            url = f"https://gitlab.com/api/v4/projects/{encoded_project_id}/repository/commits"
            params = {"path": self.target_dir, "per_page": 1}
            response = httpx.get(url, params=params)
            response.raise_for_status()
            commits = response.json()
            self._remote_created_at = commits[0]["created_at"]

            local_created_at = self._get_local_created_at()
            if local_created_at == self._remote_created_at:
                logger.info("chrome_go 仓库本地与远程相同, 无需更新")
                return False

            logger.info("chrome_go 仓库有更新, 开始下载...")
            logger.info(f"上次 created_at: {local_created_at}")
            logger.info(f"当前 created_at: {self._remote_created_at}")
        except (httpx.RequestError, OSError, KeyError, IndexError, ValueError) as e:
            logger.error(f"chrome_go 仓库检查更新失败: {e}")
            return False
        else:
            return True

    @override
    def download(self) -> bool:
        """下载并解压 ChromeGo 仓库"""
        try:
            zip_url = f"https://gitlab.com/{self.project_id}/-/archive/master/ipupdate-master.zip"
            params = {"path": self.target_dir, "ref_type": "heads"}
            zip_path = Config.TEMP_DIR / "ipupdate.zip"
            response = httpx.get(zip_url, params=params)
            response.raise_for_status()

            with zip_path.open("wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(Config.TEMP_DIR)

            zip_path.unlink()
            logger.info("chrome_go 仓库更新成功")
        except (httpx.RequestError, OSError, zipfile.BadZipFile) as e:
            logger.error(f"chrome_go 仓库下载失败: {e}")
            return False
        else:
            return True

    @override
    def update(self) -> tuple[bool, ProxyGroup]:
        """完整更新流程, 返回(是否更新, ProxyGroup)"""
        if self.check_update() and self.download():
            self.store.chrome_go.created_at = self._remote_created_at
            self._save_state()
            group = ChromeGoExtractor().extract()
            self._save_group(group)
            return True, group
        return False, self._load_group()

    def _save_group(self, group: ProxyGroup) -> None:
        """保存 ProxyGroup 到文件"""
        save_yaml(
            {
                "all": group.all,
                "udp": group.udp,
                "ai_gemini": group.ai_gemini,
                "porn_all": group.porn_all,
                "porn_x": group.porn_x,
            },
            Config.CHROME_GO_PROXIES_FILE,
        )

    def _load_group(self) -> ProxyGroup:
        """从文件加载 ProxyGroup"""
        if Config.CHROME_GO_PROXIES_FILE.exists():
            data = load_yaml(Config.CHROME_GO_PROXIES_FILE)
            return ProxyGroup(
                all=data.get("all", []),
                udp=data.get("udp", []),
                ai_gemini=data.get("ai_gemini", []),
                porn_all=data.get("porn_all", []),
                porn_x=data.get("porn_x", []),
            )
        return ProxyGroup()
