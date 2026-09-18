## 自用 clash 配置

Clash/mihomo 配置自动整理工具。从 ChromeGo 数据源抓取代理，经过提取、转换、分类后，输出到 `dist/` 目录供 Clash 订阅使用。

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

### IP 归属国家纠正

`data/ip_country_map.yaml` 是手动映射表，用于纠正 ip-api 接口返回错误的 IP 归属国家：

```yaml
2001:bc8:32d7:17b::3: 西班牙
1.2.3.4: 日本
example.com: 韩国
```

- key 支持 IPv4 / IPv6 / 域名，先按原值匹配，再按解析、规范化后的 IP 匹配
- IPv6 不用加引号，大小写、前导零、缩写写法会自动规范化后比对
- value 填国家中文名，需与 `config.py` 的分类列表写法一致
- 命中映射后不再查询 ip-api 和 GeoIP 数据库

### 分组白名单

某些服务不是按国家一刀切的（如 Gemini 还分地区），国家不在默认名单里但实际可用的 IP，在 `data/ip_group_allow.yaml` 单独放行：

```yaml
157.254.223.43: [ai_gemini]
```

- key 支持 IPv4 / IPv6 / 域名，匹配逻辑与 `ip_country_map.yaml` 相同
- value 是分组字段名（可列表）：`udp` / `ai_gemini` / `porn_x` / `porn_all` / `all`
- 命中后无视国家、协议条件，直接加入对应分组；字段名写错会告警并忽略该项

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
│   ├── store.yaml                       # 增量更新状态
│   ├── chromego_proxies.yaml            # ChromeGo 代理缓存
│   ├── ip_country_map.yaml              # 手动 IP/域名(含 IPv6) -> 国家 映射
│   └── ip_group_allow.yaml              # IP/域名 -> 额外允许加入的分组
├── temp/                                # 临时文件
└── dist/                                # 输出目录
    └── config.yaml                      # 主配置（订阅输出）
```
