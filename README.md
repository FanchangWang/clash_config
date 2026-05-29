## 自用 clash 配置

### 订阅链接
[https://raw.githubusercontent.com/FanchangWang/clash_config/main/dist/config.yaml](https://raw.githubusercontent.com/FanchangWang/clash_config/main/dist/config.yaml)

### 订阅链接(代理)
[https://fastly.jsdelivr.net/gh/FanchangWang/clash_config@main/dist/config.yaml](https://fastly.jsdelivr.net/gh/FanchangWang/clash_config@main/dist/config.yaml)

### 运行
```shell
uv sync
uv run python main.py
```

### 项目结构
```
clash_config/
├── main.py                  # 程序入口
├── pyproject.toml           # uv 项目配置
├── .github/
│   └── workflows/
│       └── daily_update.yml # 自动化部署
├── src/
│   ├── app.py              # 主应用逻辑
│   ├── config.py           # 全局配置
│   ├── logger.py           # 日志配置
│   ├── models.py           # 数据模型
│   ├── utils.py            # 工具函数
│   ├── merger.py           # 配置合并器
│   ├── updater/            # 更新器
│   ├── extractor/          # 配置提取器
│   └── converter/          # 协议转换器
├── data/                   # 数据存储
├── temp/                   # 临时文件
└── dist/                   # 输出目录
    ├── config.yaml         # 主配置
    ├── proxies/            # 代理配置
    │   ├── all.yaml
    │   ├── udp.yaml
    │   ├── ai_gemini.yaml
    │   ├── porn_x.yaml
    │   └── porn_all.yaml
    └── providers/          # 规则提供器
        ├── ai_gemini.yaml
        ├── direct.yaml
        └── proxy.yaml
```
