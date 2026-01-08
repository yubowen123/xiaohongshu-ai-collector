# 小红书 AI 内容采集器

> 自动采集小红书 AI 分享类博主的最新内容，并保存到飞书多维表格

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📖 项目简介

小红书 AI 内容采集器是一个自动化工具，用于：
- 🤖 自动采集小红书 AI 分享类博主的最新笔记
- 📊 将采集的内容保存到飞书多维表格
- ⏰ 支持定时任务，每天自动执行
- 🔄 智能去重，避免重复采集
- 🌐 使用浏览器自动化（Chrome DevTools MCP），无需处理复杂的反爬虫

## ✨ 核心特性

- **浏览器自动化采集** - 利用 Chrome DevTools MCP 进行真实浏览器操作
- **飞书多维表格集成** - 自动同步到飞书，方便团队协作
- **定时任务调度** - 每天 9:00 自动执行采集（可自定义）
- **智能去重** - 自动识别已采集的笔记
- **数据持久化** - SQLite 本地数据库保存采集记录
- **灵活配置** - 支持添加/删除博主，自定义采集规则

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Chrome 浏览器
- 飞书多维表格
- Claude Code（用于 Chrome DevTools MCP）

### 1. 安装依赖

```bash
cd xiaohongshu-ai-collector
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置飞书

#### 2.1 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 获取 `App ID` 和 `App Secret`
4. 开通权限：
   - `bitable:app` - 查看、编辑多维表格
   - `bitable:app:readonly` - 查看多维表格

#### 2.2 创建飞书多维表格

1. 在飞书中创建一个多维表格
2. 添加以下字段：
   - **标题** (文本)
   - **作者** (文本)
   - **内容摘要** (文本)
   - **笔记链接** (URL)
   - **封面图** (URL)
   - **发布时间** (文本)
   - **点赞数** (数字)
   - **笔记ID** (文本)
   - **采集时间** (文本)

3. 获取表格的 `app_token` 和 `table_id`：
   - 打开表格，URL 格式：`https://xxx.feishu.cn/base/{app_token}?table={table_id}`

#### 2.3 配置环境变量

复制环境变量模板：
```bash
cp .env.example .env
```

编辑 `.env` 文件，填入您的配置：
```bash
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=your_secret_here
FEISHU_TABLE_APP_TOKEN=bascnxxxxxxxx
FEISHU_TABLE_ID=tblxxxxxxxx
```

### 3. 添加博主

```bash
# 添加博主
python main.py add-author <user_id> <nickname> <homepage_url>

# 示例
python main.py add-author 5c3e2a4b000000001001a6e5 "AI工具分享" "https://www.xiaohongshu.com/user/profile/5c3e2a4b000000001001a6e5"
```

**如何获取博主信息：**
1. 访问博主主页
2. URL 格式：`https://www.xiaohongshu.com/user/profile/{user_id}`
3. 复制 `user_id` 和主页链接

### 4. 运行采集器

#### 方式一：立即执行一次采集（测试）
```bash
python main.py run-now
```

#### 方式二：启动定时任务
```bash
python main.py start
```

定时任务会在每天 9:00 自动执行采集。

## 📁 项目结构

```
xiaohongshu-ai-collector/
├── collectors/              # 采集模块
│   └── xiaohongshu.py      # 小红书采集器
├── integrations/            # 集成模块
│   └── feishu.py           # 飞书集成
├── data/                    # 数据目录
│   └── collector.db        # SQLite 数据库
├── logs/                    # 日志目录
│   └── collector.log       # 采集日志
├── config.py                # 配置文件
├── database.py              # 数据库配置
├── models.py                # 数据模型
├── scheduler.py             # 定时任务
├── main.py                  # 主程序
├── requirements.txt         # 依赖列表
├── .env.example             # 环境变量模板
└── README.md                # 说明文档
```

## 🔧 配置说明

### config.py 主要配置

```python
# 定时任务时间
SCHEDULE_TIME = "09:00"  # 每天 9:00 执行

# 时区
TIMEZONE = "Asia/Shanghai"

# 采集配置
MAX_NOTES_PER_AUTHOR = 10  # 每个博主最多采集 10 篇最新笔记
COLLECTION_DELAY = 2  # 采集间隔（秒）

# 日志配置
LOG_LEVEL = "INFO"
LOG_ROTATION = "100 MB"
LOG_RETENTION = "30 days"
```

## 📊 数据库

项目使用 SQLite 数据库，包含以下表：

- **authors** - 博主表
- **notes** - 笔记表
- **collection_tasks** - 采集任务表

数据库文件位置：`data/collector.db`

## 🌐 使用 Chrome DevTools MCP

本项目需要配合 Claude Code 的 Chrome DevTools MCP 使用：

1. 确保已安装并配置 Chrome DevTools MCP
2. 在 Chrome 浏览器中登录小红书账号
3. 保持浏览器打开，采集器会自动操作浏览器

## ⚠️ 注意事项

1. **合规使用**
   - 仅用于个人学习和数据分析
   - 遵守小红书平台规则
   - 不要过度频繁采集

2. **浏览器要求**
   - 需要保持 Chrome 浏览器运行
   - 需要登录小红书账号
   - 建议使用独立的浏览器配置文件

3. **数据安全**
   - 飞书凭据保存在 `.env` 文件中
   - 不要将 `.env` 文件提交到 Git
   - 定期备份数据库文件

4. **性能建议**
   - 初次使用建议先添加 2-3 个博主测试
   - 根据实际情况调整采集频率
   - 监控日志文件，及时发现问题

## 📝 使用示例

### 示例 1：添加多个博主并立即采集

```bash
# 添加博主
python main.py add-author user_id_1 "AI工具箱" "https://www.xiaohongshu.com/user/profile/user_id_1"
python main.py add-author user_id_2 "ChatGPT分享" "https://www.xiaohongshu.com/user/profile/user_id_2"

# 立即执行采集
python main.py run-now
```

### 示例 2：启动定时任务

```bash
# 启动定时任务（会一直运行）
python main.py start

# 查看日志
tail -f logs/collector.log
```

## 🐛 故障排查

### 问题 1：采集失败

**可能原因：**
- Chrome 浏览器未运行
- 小红书未登录
- MCP 服务未启动

**解决方案：**
1. 确保 Chrome 浏览器已打开
2. 手动访问小红书并登录
3. 重启 Claude Code

### 问题 2：飞书同步失败

**可能原因：**
- 飞书凭据配置错误
- 表格字段不匹配
- 权限不足

**解决方案：**
1. 检查 `.env` 文件配置
2. 确认表格字段名称正确
3. 检查应用权限

### 问题 3：定时任务不执行

**可能原因：**
- 时区配置错误
- 程序被关闭

**解决方案：**
1. 检查 `TIMEZONE` 配置
2. 使用 `systemd` 或 `supervisor` 保持程序运行

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 开源协议

MIT License

## 👨‍💻 作者

由 Claude Code 辅助开发

---

**⭐ 如果这个项目对您有帮助，请给个 Star！**
