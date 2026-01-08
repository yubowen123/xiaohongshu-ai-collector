"""
配置文件
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
BASE_DIR = Path(__file__).parent

# 数据库配置
DATABASE_PATH = BASE_DIR / "data" / "collector.db"

# 日志配置
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "collector.log"

# 飞书配置
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_TABLE_APP_TOKEN = os.getenv("FEISHU_TABLE_APP_TOKEN", "")  # 飞书多维表格的 app_token
FEISHU_TABLE_ID = os.getenv("FEISHU_TABLE_ID", "")  # 飞书多维表格的 table_id

# 小红书配置
XIAOHONGSHU_BASE_URL = "https://www.xiaohongshu.com"

# 定时任务配置
SCHEDULE_TIME = "09:00"  # 每天执行时间
TIMEZONE = "Asia/Shanghai"

# Chrome DevTools MCP 配置
CHROME_PAGE_INDEX = 0  # 使用第一个浏览器标签页

# 采集配置
MAX_NOTES_PER_AUTHOR = 10  # 每个博主最多采集多少篇最新笔记
COLLECTION_DELAY = 2  # 采集间隔（秒）

# 日志配置
LOG_LEVEL = "INFO"
LOG_ROTATION = "100 MB"
LOG_RETENTION = "30 days"
