## 自用 clash 配置

Clash/mihomo 配置自动整理工具。从多个数据源（ChromeGo / Ripao）抓取代理，经过提取、转换、分类后，合并输出到 `dist/` 目录供 Clash 订阅使用。

### 订阅链接
[https://raw.githubusercontent.com/FanchangWang/clash_config/main/dist/config.yaml](https://raw.githubusercontent.com/FanchangWang/clash_config/main/dist/config.yaml)

### 订阅链接(代理)
[https://fastly.jsdelivr.net/gh/FanchangWang/clash_config@main/dist/config.yaml](https://fastly.jsdelivr.net/gh/FanchangWang/clash_config@main/dist/config.yaml)

### 环境要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Python | 3.12+ | 强制要求 |
| [uv](https://docs.astral.sh/uv/) | - | 包管理器，禁止使用 pip/poetry/conda |

### 快速开始

```shell
# 安装依赖
uv sync

# 运行主程序
uv run clash-config

# 代码检查（ruff + ty）
uv run check
```

### 环境变量

在项目根目录创建 `.env` 文件：

```
GITHUB_TOKEN=ghp_xxx
```

仅需 GitHub API 读取权限，用于拉取 Ripao 数据源。

### 项目结构
```
clash_config/
├── pyproject.toml                       # uv 项目配置
├── .github/
│   └── workflows/
│       └── hourly_update.yml            # GitHub Actions 每小时自动运行
├── src/clash_config/
│   ├── app.py                           # 主应用逻辑
│   ├── config.py                        # 全局配置
│   ├── logger.py                        # 日志配置
│   ├── models.py                        # 数据模型
│   ├── utils.py                         # 工具函数
│   ├── merger.py                        # 配置合并器
│   ├── _check.py                        # 代码质量检查（ruff + ty）
│   ├── templates/config.yaml            # 输出模板
│   ├── updater/                         # 更新器
│   ├── extractor/                       # 配置提取器
│   └── converter/                       # 协议转换器
├── data/                                # 数据存储
├── temp/                                # 临时文件
└── dist/                                # 输出目录
    └── config.yaml                      # 主配置（订阅输出）
```
