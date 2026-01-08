# 快速设置指南

## 1. 安装依赖（5分钟）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 2. 配置飞书（10分钟）

### 步骤 1：创建飞书应用

1. 访问 https://open.feishu.cn/app
2. 点击"创建企业自建应用"
3. 填写应用名称："小红书内容采集"
4. 记录 `App ID` 和 `App Secret`

### 步骤 2：开通权限

在应用管理页面，找到"权限管理"：
- 勾选 `bitable:app` (多维表格读写)
- 勾选 `bitable:app:readonly` (多维表格只读)
- 点击"发布版本"

### 步骤 3：创建多维表格

1. 在飞书中创建新的多维表格
2. 添加以下9个字段（严格按照此名称）：
   - `标题` (文本)
   - `作者` (文本)
   - `内容摘要` (文本)
   - `笔记链接` (URL)
   - `封面图` (URL)
   - `发布时间` (文本)
   - `点赞数` (数字)
   - `笔记ID` (文本)
   - `采集时间` (文本)

### 步骤 4：获取表格信息

打开多维表格，查看 URL：
```
https://xxx.feishu.cn/base/bascnXXXXXXXXXX?table=tblXXXXXXXXXX
                         ^^^^^^^^^^^^^^       ^^^^^^^^^^^^^^
                         app_token            table_id
```

复制这两个值。

### 步骤 5：配置环境变量

```bash
# 复制模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

填入您的配置：
```bash
FEISHU_APP_ID=cli_xxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_TABLE_APP_TOKEN=bascnxxxxxxxx
FEISHU_TABLE_ID=tblxxxxxxxx
```

## 3. 添加博主（2分钟）

### 方法：从小红书主页获取信息

1. 访问小红书，找到您想采集的 AI 博主
2. 进入博主主页，复制链接
3. 提取用户 ID：

示例链接：
```
https://www.xiaohongshu.com/user/profile/5c3e2a4b000000001001a6e5
                                         ^^^^^^^^^^^^^^^^^^^^^^
                                         user_id
```

4. 添加博主：

```bash
python main.py add-author <user_id> "<昵称>" "<主页链接>"

# 示例
python main.py add-author 5c3e2a4b000000001001a6e5 "AI工具分享达人" "https://www.xiaohongshu.com/user/profile/5c3e2a4b000000001001a6e5"
```

**推荐博主示例（需要自己查找真实ID）：**
- AI工具分享类博主
- ChatGPT教程类博主
- AI绘画分享类博主

建议先添加 2-3 个博主进行测试。

## 4. 测试运行（1分钟）

```bash
# 立即执行一次采集（测试）
python main.py run-now

# 查看日志
tail -f logs/collector.log
```

如果一切正常，您将看到：
- ✅ 数据库初始化完成
- ✅ 开始采集博主笔记
- ✅ 成功添加到飞书

## 5. 启动定时任务

```bash
# 使用启动脚本
./start.sh

# 或直接运行
python main.py start
```

定时任务会在每天 9:00 自动执行采集。

## ⚠️ 重要提示

1. **首次使用前必须：**
   - 在 Chrome 浏览器中登录小红书账号
   - 保持 Chrome 浏览器打开
   - 确保 Chrome DevTools MCP 已配置

2. **飞书表格字段名称必须完全一致**
   - 字段名称区分中英文标点符号
   - 建议复制粘贴字段名

3. **测试建议：**
   - 先手动添加 1-2 个博主
   - 使用 `run-now` 立即测试一次
   - 检查飞书表格是否有数据
   - 确认无误后再启动定时任务

## 🆘 常见问题

### Q1: 采集失败怎么办？

**A:** 检查以下几点：
1. Chrome 浏览器是否已打开
2. 小红书是否已登录
3. Chrome DevTools MCP 是否正常运行
4. 查看日志文件 `logs/collector.log`

### Q2: 飞书同步失败？

**A:** 检查：
1. `.env` 文件配置是否正确
2. 飞书应用权限是否已开通
3. 表格字段名称是否完全一致
4. 应用是否已"发布版本"

### Q3: 如何停止程序？

**A:** 按 `Ctrl + C` 即可停止。

## 📞 获取帮助

- 查看完整文档：[README.md](README.md)
- 查看日志：`tail -f logs/collector.log`
- 检查数据库：`sqlite3 data/collector.db`

---

**准备好了吗？开始第一步！** 🚀
