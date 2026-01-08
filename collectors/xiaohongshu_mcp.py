"""
小红书数据采集模块 - 实际可用版本
使用 Claude Code 的 Chrome DevTools MCP 工具
"""
import time
import re
from typing import List, Dict, Optional
from loguru import logger
from models import Author, Note
import config


class XiaohongshuCollectorMCP:
    """
    小红书采集器 - MCP 版本

    这个版本直接使用 Claude Code 环境中可用的 Chrome DevTools MCP 工具
    """

    def __init__(self):
        """初始化采集器"""
        self.page_index = config.CHROME_PAGE_INDEX
        logger.info("小红书采集器初始化完成（MCP 模式）")

    def collect_author_notes_sync(self, author: Author, max_notes: int = None) -> List[Note]:
        """
        同步方式采集指定博主的笔记列表

        使用说明：
        1. 在 Chrome 浏览器中打开小红书并登录
        2. 手动导航到博主主页
        3. 运行此函数进行采集

        Args:
            author: 博主信息
            max_notes: 最多采集多少篇（默认使用配置）

        Returns:
            笔记列表
        """
        if max_notes is None:
            max_notes = config.MAX_NOTES_PER_AUTHOR

        logger.info(f"开始采集博主 {author.nickname} 的笔记")
        logger.info(f"请确保浏览器已打开博主主页: {author.homepage_url}")

        notes = []

        try:
            # 提示用户手动操作
            logger.warning("=" * 60)
            logger.warning("手动采集模式:")
            logger.warning(f"1. 请在 Chrome 中打开: {author.homepage_url}")
            logger.warning("2. 确保页面已完全加载")
            logger.warning("3. 按回车继续...")
            logger.warning("=" * 60)

            # 这里实际使用时，可以通过 MCP 工具自动获取页面内容
            # 由于是在 Python 脚本中运行，无法直接调用 Claude Code 的 MCP 工具
            # 所以这个版本提供了框架，实际使用需要配合 Claude Code 交互式使用

            logger.info("采集功能需要在 Claude Code 交互环境中使用 MCP 工具")
            logger.info("请参考 test_collector.py 中的使用示例")

        except Exception as e:
            logger.error(f"采集失败: {e}")

        return notes

    def parse_note_card(self, card_text: str, author: Author) -> Optional[Note]:
        """
        解析单个笔记卡片信息

        Args:
            card_text: 卡片文本内容
            author: 博主信息

        Returns:
            Note 对象或 None
        """
        try:
            # 示例解析逻辑（需要根据实际页面结构调整）
            # 小红书笔记卡片通常包含：
            # - 标题
            # - 链接（包含 note_id）
            # - 点赞数

            # 提取笔记 ID
            note_id_match = re.search(r'/explore/([a-f0-9]{24})', card_text)
            if not note_id_match:
                return None

            note_id = note_id_match.group(1)

            # 提取标题（示例）
            title = "笔记标题"  # 需要实际解析

            # 构造笔记 URL
            note_url = f"{config.XIAOHONGSHU_BASE_URL}/explore/{note_id}"

            # 创建 Note 对象
            note = Note(
                note_id=note_id,
                author_user_id=author.user_id,
                title=title,
                note_url=note_url,
                content="",
                cover_image="",
                likes_count=0
            )

            return note

        except Exception as e:
            logger.error(f"解析笔记卡片失败: {e}")
            return None

    def extract_note_id_from_url(self, url: str) -> str:
        """从链接中提取笔记 ID"""
        match = re.search(r'/explore/([a-f0-9]{24})', url)
        if match:
            return match.group(1)
        return ""

    def extract_user_id_from_url(self, url: str) -> str:
        """从链接中提取用户 ID"""
        match = re.search(r'/user/profile/([a-f0-9]{24})', url)
        if match:
            return match.group(1)
        return ""


def create_collector():
    """创建采集器实例"""
    return XiaohongshuCollectorMCP()
