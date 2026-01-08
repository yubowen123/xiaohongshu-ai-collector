# Chrome DevTools MCP 使用指南

本项目使用 Chrome DevTools MCP 进行浏览器自动化采集。

## 🎯 MCP 采集流程

### 准备工作

1. **确保 Chrome DevTools MCP 已配置**
   ```bash
   # 检查 MCP 配置
   cat ~/.mcp-all-in-one/mcp.json
   ```

   应包含：
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest"]
       }
     }
   }
   ```

2. **在 Chrome 中登录小红书**
   - 打开 Chrome 浏览器
   - 访问 https://www.xiaohongshu.com
   - 登录您的账号

3. **保持浏览器运行**
   - Chrome 需要保持打开状态
   - 可以最小化，但不要关闭

## 📝 手动采集流程（通过 Claude Code）

由于 Chrome DevTools MCP 只能在 Claude Code 交互环境中使用，这里提供实际操作步骤：

### 步骤 1：导航到博主主页

在 Claude Code 中执行：

```
请帮我使用 Chrome DevTools MCP 打开这个小红书博主主页：
https://www.xiaohongshu.com/user/profile/<user_id>

然后获取页面快照
```

### 步骤 2：解析笔记列表

Claude Code 会返回页面快照，然后你可以要求：

```
从这个快照中提取出所有笔记的信息，包括：
- 笔记标题
- 笔记链接
- 笔记 ID
- 点赞数（如果有）

请以 JSON 格式返回，格式如下：
[
  {
    "note_id": "...",
    "title": "...",
    "note_url": "...",
    "likes_count": 123
  }
]
```

### 步骤 3：保存到数据库和飞书

将解析出的数据保存：

```python
# 在 Claude Code 中运行 Python 代码
from database import SessionLocal
from integrations.feishu import FeishuClient
from models import Note
from datetime import datetime

# 从 JSON 创建 Note 对象
notes_data = [...]  # Claude 解析出的数据

feishu_client = FeishuClient()
db = SessionLocal()

for note_data in notes_data:
    note = Note(
        note_id=note_data['note_id'],
        author_user_id='<博主user_id>',
        title=note_data['title'],
        note_url=note_data['note_url'],
        likes_count=note_data.get('likes_count', 0),
        created_at=datetime.now()
    )

    # 保存到飞书
    record_id = feishu_client.add_note_to_table(note)
    print(f"✅ 已保存: {note.title}")
```

## 🤖 自动化采集（推荐方式）

### 创建 Claude Code Skill

您可以创建一个自定义 Skill 来自动化整个流程：

创建文件：`~/.claude/skills/xiaohongshu-collect.md`

```markdown
# /xiaohongshu-collect

自动采集小红书博主的最新笔记并保存到飞书

使用方法：
/xiaohongshu-collect <博主主页URL>

步骤：
1. 使用 Chrome DevTools MCP 打开博主主页
2. 获取页面快照
3. 解析笔记列表
4. 保存到数据库
5. 同步到飞书多维表格

示例：
/xiaohongshu-collect https://www.xiaohongshu.com/user/profile/5c3e2a4b000000001001a6e5
```

然后在 Claude Code 中直接使用：
```bash
/xiaohongshu-collect https://www.xiaohongshu.com/user/profile/<user_id>
```

## 🔍 实际采集示例

### 示例 1：采集单个博主

**步骤 1：** 在 Claude Code 中说：

```
我想采集小红书博主 "AI工具分享" 的最新笔记。
博主主页：https://www.xiaohongshu.com/user/profile/5c3e2a4b000000001001a6e5

请帮我：
1. 使用 Chrome DevTools MCP 打开这个页面
2. 获取页面快照
3. 提取所有笔记信息
4. 保存到飞书表格
```

**步骤 2：** Claude 会自动：
- 调用 `mcp__chrome-devtools__navigate_page`
- 调用 `mcp__chrome-devtools__take_snapshot`
- 解析快照内容
- 调用飞书 API 保存数据

### 示例 2：批量采集多个博主

**方式 A：使用主程序**

```bash
# 1. 添加博主到数据库
python main.py add-author <user_id_1> "AI工具箱" "<homepage_url_1>"
python main.py add-author <user_id_2> "ChatGPT分享" "<homepage_url_2>"

# 2. 在 Claude Code 中要求执行采集
# "请帮我使用 Chrome DevTools MCP 采集数据库中所有博主的笔记"
```

**方式 B：手动逐个采集**

在 Claude Code 中：
```
请依次采集以下博主的笔记：
1. https://www.xiaohongshu.com/user/profile/user_id_1
2. https://www.xiaohongshu.com/user/profile/user_id_2
3. https://www.xiaohongshu.com/user/profile/user_id_3

每个博主采集最新的 10 篇笔记
```

## 📊 MCP 工具参考

本项目使用的主要 MCP 工具：

### 1. navigate_page
```python
# 导航到指定页面
mcp__chrome-devtools__navigate_page(url="<url>", type="url")
```

### 2. take_snapshot
```python
# 获取页面文本快照
mcp__chrome-devtools__take_snapshot()
```

### 3. click
```python
# 点击页面元素（用于加载更多）
mcp__chrome-devtools__click(uid="<element_uid>")
```

### 4. evaluate_script
```python
# 执行 JavaScript 获取数据
mcp__chrome-devtools__evaluate_script(
    function="() => { return document.querySelectorAll('.note-item'); }"
)
```

## ⚠️ 注意事项

1. **页面加载时间**
   - 导航后等待 2-3 秒确保页面完全加载
   - 小红书有懒加载，可能需要滚动页面

2. **反爬限制**
   - 使用真实浏览器会话，登录后采集
   - 控制采集频率，避免被限制
   - 推荐间隔：每个博主采集后等待 5-10 秒

3. **错误处理**
   - 如果页面结构变化，需要更新解析逻辑
   - 定期检查采集结果

## 🎓 进阶技巧

### 技巧 1：使用 JavaScript 提取数据

小红书的笔记列表通常可以通过 JavaScript 提取：

```javascript
// 在 evaluate_script 中执行
const notes = Array.from(document.querySelectorAll('.note-item')).map(item => ({
    title: item.querySelector('.title')?.innerText,
    url: item.querySelector('a')?.href,
    likes: item.querySelector('.likes')?.innerText
}));
return notes;
```

### 技巧 2：滚动加载更多

```javascript
// 滚动到页面底部
window.scrollTo(0, document.body.scrollHeight);
```

### 技巧 3：等待元素出现

使用 `wait_for` 工具：
```python
mcp__chrome-devtools__wait_for(text="笔记", timeout=5000)
```

## 📚 相关文档

- [Chrome DevTools MCP 官方文档](https://github.com/modelcontextprotocol/servers)
- [小红书页面结构分析](./docs/xiaohongshu_structure.md)（需要创建）
- [故障排查指南](./docs/troubleshooting.md)（需要创建）

---

**提示：** 第一次使用建议先手动在 Claude Code 中测试单个博主的采集流程，熟悉后再使用自动化脚本。
