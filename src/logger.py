"""日志配置"""

import logging

# 配置我们自己的日志
logger = logging.getLogger("clash_config")
logger.setLevel(logging.DEBUG)

# 创建 console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 设置日志格式
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
)
console_handler.setFormatter(formatter)

# 添加 handler
logger.addHandler(console_handler)

# 抑制第三方库的 DEBUG 日志
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)
