"""代理转换器基类和工厂"""

from pathlib import Path

from .clash_meta2 import ClashMeta2Converter
from .hysteria import HysteriaConverter
from .hysteria2 import Hysteria2Converter
from .mieru import MieruConverter
from .xray import XrayConverter


class ProxyConverter:
    """代理协议转换类, 用于将各种协议转换为 mihomo 协议格式"""

    @staticmethod
    def convert_hysteria(config_file: Path):
        """将 hysteria 配置转换为 mihomo 格式"""
        return HysteriaConverter.convert(config_file)

    @staticmethod
    def convert_hysteria2(config_file: Path):
        """将 hysteria2 配置转换为 mihomo 格式"""
        return Hysteria2Converter.convert(config_file)

    @staticmethod
    def convert_mieru(config_file: Path):
        """将 mieru 配置转换为 mihomo 格式"""
        return MieruConverter.convert(config_file)

    @staticmethod
    def convert_xray(config_file: Path):
        """将 xray 配置转换为 mihomo 格式"""
        return XrayConverter.convert(config_file)

    @staticmethod
    def convert_clash_meta2(config_file: Path):
        """将 clash.meta2 配置转换为 mihomo 格式"""
        return ClashMeta2Converter.convert(config_file)

    @staticmethod
    def convert(config_file: Path, protocol: str):
        """根据协议类型转换配置"""
        converters = {
            "hysteria": ProxyConverter.convert_hysteria,
            "hysteria2": ProxyConverter.convert_hysteria2,
            "mieru": ProxyConverter.convert_mieru,
            "xray": ProxyConverter.convert_xray,
            "clash.meta2": ProxyConverter.convert_clash_meta2,
        }
        converter_func = converters.get(protocol.lower())
        if not converter_func:
            from ..logger import logger

            logger.warning(f"未知的协议类型: {protocol}")
            return None
        return converter_func(config_file)
