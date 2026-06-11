# clash_config — AGENTS.md

## 项目概述

Clash 配置自动整理工具。从多个数据源（ChromeGo / Ripao）抓取代理，经过提取、转换、分类后，合并输出到 `dist/` 目录供 Clash 订阅使用。

## 核心技术栈（源自 规则.md）

| 约定 | 值 |
|------|----|
| Python | **3.12+**（强制） |
| 包管理 | **`uv`**（禁止 pip/poetry/conda） |
| 代码质量 | **ruff**（检查+格式化）、**ty**（类型检查） |
| 依赖原则 | YAGNI，最小可用 |

## 项目结构

```
clash_config/
├── main.py                        # 入口（不再存在，使用 entry point）
├── pyproject.toml                 # uv 项目配置
├── AGENTS.md                      # 本文件 — opencode 预读用
├── .gitattributes                 # LF 换行符强制
├── .github/workflows/daily_update.yml  # GitHub Actions 每小时自动运行
├── src/clash_config/
│   ├── app.py                     # 主流程编排
│   ├── config.py                  # Config 类（路径、常量、GitHub token）
│   ├── logger.py                  # logging 封装
│   ├── models.py                  # ProxyDict, ProxyGroup, StoreData 等
│   ├── utils.py                   # load_yaml / save_yaml / get_geoip_country / store 持久化
│   ├── merger.py                  # Merger.merge() — 合并 ProxyGroup 并输出 dist/*.yaml
│   ├── updater/
│   │   ├── base.py                # BaseUpdater（抽象基类）
│   │   ├── chrome_go.py           # ChromeGoUpdater（GitLab → zip → 提取）
│   │   └── ripao.py               # RipaoUpdater（GitHub → clash.yaml → 提取）
│   ├── extractor/
│   │   ├── base.py                # BaseExtractor（抽象基类）
│   │   ├── chrome_go.py           # ChromeGoExtractor（递归扫描各类协议目录）
│   │   └── ripao.py               # RipaoExtractor（加载/修复 YAML，转换）
│   └── converter/
│       ├── base.py                # ProxyConverter 工厂
│       ├── clash_meta2.py         # Clash Meta2 → mihomo
│       ├── hysteria.py            # hysteria → mihomo
│       ├── hysteria2.py           # hysteria2 → mihomo
│       ├── mieru.py               # mieru → mihomo
│       └── xray.py                # xray（vless/vmess/trojan）→ mihomo
├── data/
│   ├── store.yaml                 # 状态持久化（chrome_go.created_at, ripao.sha）
│   ├── chromego_proxies.yaml      # ChromeGo 缓存
│   └── ripao_proxies.yaml         # Ripao 缓存
├── dist/
│   ├── config.yaml                # 主 Clash 配置（proxy-groups, proxy-providers, rules）
│   ├── proxies/                   # 代理列表（all/udp/ai_gemini/porn_x/porn_all）
│   └── providers/                 # rule-providers（direct/proxy/ai_gemini 域名列表）
└── temp/                          # 临时文件（gitignore 中忽略）
```

## 核心数据流

```
ChromeGo (GitLab)  ──→ zip ──→ ChromeGoUpdater ──→ ChromeGoExtractor ──→ ProxyGroup ──┐
                                                                                      ├──→ Merger.merge() ──→ dist/proxies/*.yaml
Ripao (GitHub)     ──→ yaml ──→ RipaoUpdater   ──→ RipaoExtractor   ──→ ProxyGroup ──┘
```

### 各层职责

1. **Updater**：检查远程是否有更新（对比 SHA / created_at），有则下载
2. **Extractor**：读取原始配置，通过 Converter 转为统一格式，按国家和地区分类到 ProxyGroup
3. **Converter**：各协议（clash.meta2 / hysteria / hysteria2 / mieru / xray）→ mihomo 格式字典
4. **Merger**：合并两个源的 ProxyGroup，去重，写入 dist/proxies/*.yaml

## 数据模型（models.py）

- **ProxyDict** (TypedDict)：`name, type, server, port, country, udp` 等
- **ProxyGroup** (dataclass)：`all, udp, ai_gemini, porn_all, porn_x` 五个分类列表
- **StoreData**：`chrome_go.created_at` + `ripao.sha` 用于增量更新判断

## 配置分类规则（config.py）

| 分类 | 条件 |
|------|------|
| `AI_GEMINI` | country ∈ `[日本,韩国,台湾,荷兰,...]` |
| `UDP` | protocol ∈ `[hysteria, hysteria2, tuic]` |
| `PORN_X` | country ∈ `[美国,日本,韩国,...]` |
| `PORN_ALL` | country ∈ `[美国,日本,韩国,...]` **且** protocol ∈ `[hysteria, hysteria2, tuic]` |

## 入口与命令

- 运行主程序：`uv run clash-config`（对应 `app.py:run()`）
- 代码检查：`uv run check`（对应 `_check.py:main()` → ruff + ty）
- 手动：`uv sync && uv run clash-config`

## YAML 输出约定

- 所有 `save_yaml()` 写文件使用 `newline=""` 确保 LF 换行符（防止 Windows CRLF）
- `.gitattributes` 已配置强制 LF

## 环境变量

- `.env`：`GITHUB_TOKEN`（GitHub API read 用，不需要任何权限）
- 通过 `Config.github_token()` 加载

## .gitignore

```
.env, .venv, __pycache__, *.pyc, .DS_Store, temp/, .ruff_cache/
```

## 注意

- 项目无 `tests/` 目录
- CI 在 `.github/workflows/daily_update.yml`，每小时运行一次
