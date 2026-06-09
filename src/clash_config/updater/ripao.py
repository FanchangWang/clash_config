"""Ripao 更新器"""

import httpx

from ..config import Config
from ..extractor.ripao import RipaoExtractor
from ..logger import logger
from ..models import ProxyGroup
from ..utils import load_yaml, save_yaml
from .base import BaseUpdater


class RipaoUpdater(BaseUpdater):
    """Ripao 仓库更新器"""

    source_name = "ripao"

    def __init__(self) -> None:
        super().__init__()
        self.repo_url = Config.RIPAO_REPO_URL
        self.ref = "main"
        self.headers = {"Accept": "application/vnd.github.v3+json"}
        token = Config.github_token()
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        self._remote_sha = ""
        self._download_url = ""

    def _get_local_sha(self) -> str:
        """获取本地记录的 SHA"""
        return self.store.ripao.sha

    def _get_remote_info(self) -> dict | None:
        """获取远程文件信息"""
        try:
            params = {"ref": self.ref}
            response = httpx.get(self.repo_url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"获取 GitHub 文件信息失败: {e}")
            return None

    def check_update(self) -> bool:
        """检查是否有更新"""
        logger.info("开始检查 ripao clash 文件更新...")

        remote_info = self._get_remote_info()
        if not remote_info:
            return False

        self._remote_sha = remote_info.get("sha", "")
        self._download_url = remote_info.get("download_url", "")

        if not self._remote_sha:
            logger.error("获取 SHA 失败")
            return False

        local_sha = self._get_local_sha()

        if self._remote_sha == local_sha:
            logger.info("ripao clash 文件本地与远程相同，无需更新")
            return False

        logger.info("ripao clash 文件有更新，开始下载...")
        logger.info(f"上次 SHA: {local_sha}")
        logger.info(f"当前 SHA: {self._remote_sha}")
        return True

    def download(self) -> bool:
        """下载 clash 文件"""
        try:
            if not self._download_url:
                logger.error("获取下载链接失败")
                return False

            response = httpx.get(self._download_url, timeout=10)
            response.raise_for_status()

            output_file = Config.TEMP_DIR / "ripao_clash.yaml"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(response.text)

            logger.info("ripao clash 文件更新成功")
            return True
        except httpx.RequestError as e:
            logger.error(f"下载文件失败: {e}")
            return False

    def update(self) -> tuple[bool, ProxyGroup]:
        """完整更新流程，返回(是否更新, ProxyGroup)"""
        if self.check_update():
            if self.download():
                self.store.ripao.sha = self._remote_sha
                self._save_state()
                group = RipaoExtractor().extract()
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
            Config.RIPAO_PROXIES_FILE,
        )

    def _load_group(self) -> ProxyGroup:
        """从文件加载 ProxyGroup"""
        if Config.RIPAO_PROXIES_FILE.exists():
            data = load_yaml(Config.RIPAO_PROXIES_FILE)
            return ProxyGroup(
                all=data.get("all", []),
                udp=data.get("udp", []),
                ai_gemini=data.get("ai_gemini", []),
                porn_all=data.get("porn_all", []),
                porn_x=data.get("porn_x", []),
            )
        return ProxyGroup()
