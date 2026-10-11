# clash_config — AGENTS.md

## 项目概述

Clash 配置自动整理工具。从 ChromeGo 数据源抓取代理，经过提取、转换、分类后，输出到 `dist/` 目录供 Clash 订阅使用。

## 核心技术栈

| 约定 | 值 |
|------|----|
| Python | **3.12+**（强制） |
| 包管理 | **`uv`**（禁止 pip/poetry/conda） |
| 代码质量 | **ruff**（检查+格式化）、**ty**（类型检查） |
| 依赖原则 | YAGNI，最小可用 |

## 项目结构

```
clash_config/
├── pyproject.toml                 # uv 项目配置
├── AGENTS.md                      # 本文件 — opencode 预读用
├── .gitattributes                 # LF 换行符强制
├── .github/workflows/hourly_update.yml  # GitHub Actions 每小时自动运行
├── src/clash_config/
│   ├── __init__.py                # __version__ = "1.1.0"
│   ├── _check.py                  # 代码质量检查（ruff + ty）
│   ├── app.py                     # 主流程编排
│   ├── config.py                  # Config 类（路径、常量、GitHub token）
│   ├── logger.py                  # logging 封装
│   ├── models.py                  # ProxyDict, ProxyGroup, StoreData 等
│   ├── utils.py                   # load_yaml / save_yaml / get_geoip_country / store 持久化
│   ├── merger.py                  # Merger.merge() — 合并 ProxyGroup 并输出 dist/config.yaml
│   ├── templates/
│   │   └── config.yaml            # 输出模板（含 {{PROXIES}} / {{DYNAMIC_GROUPS}} 占位符）
│   ├── updater/
│   │   ├── __init__.py
│   │   ├── base.py                # BaseUpdater（抽象基类）
│   │   └── chrome_go.py           # ChromeGoUpdater（GitLab → zip → 提取）
│   ├── extractor/
│   │   ├── __init__.py
│   │   ├── base.py                # BaseExtractor（抽象基类）
│   │   └── chrome_go.py           # ChromeGoExtractor（递归扫描各类协议目录）
│   └── converter/
│       ├── __init__.py
│       ├── base.py                # ProxyConverter 工厂
│       ├── clash_meta2.py         # Clash Meta2 → mihomo
│       ├── hysteria.py            # hysteria → mihomo
│       ├── hysteria2.py           # hysteria2 → mihomo
│       ├── mieru.py               # mieru → mihomo
│       └── xray.py                # xray（vless/vmess/trojan）→ mihomo
├── data/
│   ├── store.yaml                 # 状态持久化（chrome_go.created_at）
│   ├── chromego_proxies.yaml      # ChromeGo 缓存
│   ├── ip_country_map.yaml        # 手动 IP/域名 -> 国家 映射（纠正 ip-api 错误归属）
│   └── ip_group_allow.yaml        # IP/域名 -> 额外允许加入的分组（绕过国家/协议限制）
├── dist/
│   ├── config.yaml                # 主 Clash 配置（订阅输出，已提交）
│   └── proxies/                   # 代理列表（gitignored，运行时生成）
└── temp/                          # 临时文件（gitignored）
```

## 核心数据流

```
ChromeGo (GitLab) ──→ zip ──→ ChromeGoUpdater ──→ ChromeGoExtractor ──→ ProxyGroup ──→ Merger.merge() ──→ dist/config.yaml
```

### 各层职责

1. **Updater**：检查远程是否有更新（对比 created_at），有则下载
2. **Extractor**：读取原始配置，通过 Converter 转为统一格式，按国家和地区分类到 ProxyGroup
3. **Converter**：各协议（clash.meta2 / hysteria / hysteria2 / mieru / xray）→ mihomo 格式字典
4. **Merger**：接收单个 ProxyGroup，写入 dist/config.yaml

## 数据模型（models.py）

- **ProxyDict** (TypedDict)：`name, type, server, port, country, udp` 等
- **ProxyGroup** (dataclass)：`all, udp, ai_gemini, porn_all, porn_x` 五个分类列表
- **StoreData**：`chrome_go.created_at` 用于增量更新判断

## 配置分类规则（config.py）

| 分类 | 条件 |
|------|------|
| `AI_GEMINI` | country ∈ `[日本,韩国,台湾,荷兰,...]` |
| `UDP` | protocol ∈ `[hysteria, hysteria2, tuic]` |
| `PORN_X` | country ∈ `[美国,日本,韩国,...]` |
| `PORN_ALL` | country ∈ `[美国,日本,韩国,...]` **且** protocol ∈ `[hysteria, hysteria2, tuic]` |

以上四条均可被 `data/ip_group_allow.yaml` 白名单绕过（见下）。

## 代理命名

- 格式：`{国家}-{协议}-{序号}`，如 `日本-ss-1`（历史上有 `go-` 前缀用于区分数据源，单源后已去掉）

## IP 归属国家纠正

## 入口与命令

- 运行主程序：`uv run clash-config`（对应 `app.py:run()`）
- 代码检查：`uv run check`（对应 `_check.py:main()` → ruff + ty）
- 手动：`uv sync && uv run clash-config`

## YAML 输出约定

- 所有 `save_yaml()` 写文件使用 `newline=""` 确保 LF 换行符（防止 Windows CRLF）
- `.gitattributes` 已配置强制 LF

## IP 归属国家纠正

- `data/ip_country_map.yaml`：手动 IP/域名 → 国家 映射，纠正 ip-api 返回的错误归属
- `utils.get_geoip_country()` 优先查该映射（原值 → 解析/规范化后的 IP），命中即返回，不走 ip-api / GeoIP
- 支持 IPv4 / IPv6 / 域名：`utils._resolve_ips()` 用 `socket.getaddrinfo` 解析（兼容 IPv6），IP 字面量额外比对 `ipaddress` 规范化形式
- 映射在进程内缓存一次，value 用国家中文名，需与 `config.py` 的分类列表写法一致

## GitLab Cloudflare 拦截

`updater/chrome_go.py` 探测更新时请求 `.../repository/commits.json`。GitLab.com 的 Cloudflare
会拦截**不带 `.json` 后缀**的 `GET /api/v4/projects/*/repository/commits`，返回
`403` + `Cf-Mitigated: challenge` + HTML 挑战页（与 UA、频率无关；同 URL 用 `HEAD` 请求反而 200）。

- 现象：CI 红，日志为 `httpx.HTTPStatusError: Client error '403 Forbidden'`，
  崩溃点在 `check_update()` 的 `raise_for_status()`，`Merger` / 提交步骤全不执行
- 排查命令：`curl -s -D- -o /dev/null "https://gitlab.com/api/v4/projects/free9999%2Fipupdate/repository/commits?per_page=1" | grep -i cf-mitigated`
  出现 `challenge` 即为该问题
- 当前用 `.json` 后缀绕过：`path` 过滤依然生效（实测不存在路径返回 `[]`），响应仍是 list，代码逻辑不变
- **隐患：这是对当前 WAF 规则的隐式依赖，非 GitLab 语义上的 API 选择。规则一变会再次 403**
- 失效后不要换别的 API 端点打补丁，改用 git 协议（见下）

### 失效后的正统方案（推荐 A'：git fetch 取子树 hash）

git over HTTPS 是 Cloudflare 明确放行的协议，不在 API 规则的风险面里。

```shell
git init -q && git remote add origin https://gitlab.com/free9999/ipupdate.git
git fetch -q --depth=1 --filter=blob:none origin master
git ls-tree FETCH_HEAD backup/img/1/2/    # tree 行第三列即 ipp 子树 hash
```

实测 `--filter=blob:none --depth=1` 空 clone 约 3s / 87K，成本与现在的 HTTP 请求相当。

- 判定依据从「某个 API 端点的可用性」换成「git 子树 hash 的内容寻址」，只对 `ipp` 目录内容敏感
- 该 hash 与 `/repository/tree` API 返回的 `id` **完全一致**（`9c95339c...`），两种方式可互换
- 必改项：`extractor/chrome_go.py:30-38` 硬编码了 zip 解压目录名
  `ipupdate-master-backup-img-1-2-ipp/`（带 `path` 参数的 archive zip 顶层目录即此名）。
  改用 git 拿内容后目录变为 `<repo>/backup/img/1/2/ipp`，该常量必须同步改
- 同步改名 `models.ChromeGoState.created_at` → `version`（含 `base.py:34`、`chrome_go.py:28-30`），
  因为存的不再是时间戳

### 备选：加 GitLab token

`PRIVATE-TOKEN` / `Authorization: Bearer` 头会被 Cloudflare 豁免（实测同样被拦的 URL 加 token 后
从 403 变 401，即已抵达 GitLab）。但本项目是**公开仓库**，为一个公开仓库的定时任务配置并长期维护
token 不划算；且效果与 `.json` 后缀等同。仅在确实需要绕开匿名 API 限流时才考虑，
理由应是限流而非绕防火墙。

## 分组白名单

- `data/ip_group_allow.yaml`：IP/域名 → 额外允许加入的分组，绕过国家/协议条件
  （典型场景：Gemini 不只看国家还看地区，某些美国 IP 实际可用）
- `utils.get_allowed_groups()` 返回分组名集合；可用值即 `ProxyGroup` 字段名：
  `all / udp / ai_gemini / porn_all / porn_x`，非法名告警后忽略
- 命中判定发生在 `extractor/chrome_go.py: process_proxies()` 的分类环节，key 匹配逻辑与 IP 映射共用 `_map_keys()` / `_server_keys()`

## 注意

- 项目无 `tests/` 目录
- CI 在 `.github/workflows/hourly_update.yml`，每小时运行一次，自动提交 `dist/` 和 `data/` 变更
