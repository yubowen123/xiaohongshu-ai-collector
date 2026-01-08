"""
小红书 AI 内容采集器 - 主程序
"""
import sys
import time
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

import config
from database import init_database, SessionLocal, AuthorDB, NoteDB, CollectionTaskDB
from collectors.xiaohongshu import XiaohongshuCollector
from integrations.feishu import FeishuClient
from scheduler import CollectorScheduler
from models import Author, Note


# 配置日志
config.LOG_DIR.mkdir(parents=True, exist_ok=True)
logger.add(
    config.LOG_FILE,
    rotation=config.LOG_ROTATION,
    retention=config.LOG_RETENTION,
    level=config.LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)


class CollectorApp:
    """采集器应用"""

    def __init__(self):
        """初始化应用"""
        self.db = SessionLocal()
        self.feishu_client = FeishuClient()
        self.collector = None  # 需要传入 MCP 客户端
        self.scheduler = None

        logger.info("=" * 60)
        logger.info("小红书 AI 内容采集器")
        logger.info("=" * 60)

    def initialize(self):
        """初始化"""
        # 初始化数据库
        init_database()
        logger.info("✅ 数据库初始化完成")

        # 初始化调度器
        self.scheduler = CollectorScheduler(self.run_collection_task)
        logger.info("✅ 调度器初始化完成")

    def add_author(self, user_id: str, nickname: str, homepage_url: str, category: str = "AI"):
        """
        添加博主

        Args:
            user_id: 小红书用户 ID
            nickname: 昵称
            homepage_url: 主页链接
            category: 分类
        """
        try:
            # 检查是否已存在
            existing = self.db.query(AuthorDB).filter(AuthorDB.user_id == user_id).first()
            if existing:
                logger.warning(f"博主 {nickname} 已存在")
                return existing

            # 创建新博主
            author = AuthorDB(
                user_id=user_id,
                nickname=nickname,
                homepage_url=homepage_url,
                category=category,
                is_active=True
            )
            self.db.add(author)
            self.db.commit()
            self.db.refresh(author)

            logger.info(f"✅ 成功添加博主: {nickname} ({user_id})")
            return author

        except Exception as e:
            logger.error(f"添加博主失败: {e}")
            self.db.rollback()
            return None

    def get_active_authors(self):
        """获取所有启用的博主"""
        return self.db.query(AuthorDB).filter(AuthorDB.is_active == True).all()

    def run_collection_task(self):
        """执行采集任务"""
        logger.info("🚀 开始执行采集任务...")

        # 创建任务记录
        task = CollectionTaskDB(
            task_type='auto',
            status='running',
            started_at=datetime.now()
        )
        self.db.add(task)
        self.db.commit()

        try:
            # 获取所有启用的博主
            authors = self.get_active_authors()
            task.total_authors = len(authors)
            self.db.commit()

            logger.info(f"找到 {len(authors)} 个启用的博主")

            if len(authors) == 0:
                logger.warning("没有启用的博主，请先添加博主")
                task.status = 'completed'
                task.completed_at = datetime.now()
                self.db.commit()
                return

            total_notes = 0
            new_notes = 0
            synced_notes = 0

            # 遍历每个博主
            for author_db in authors:
                logger.info(f"\n处理博主: {author_db.nickname}")

                # 转换为 Pydantic 模型
                author = Author(
                    id=author_db.id,
                    user_id=author_db.user_id,
                    nickname=author_db.nickname,
                    homepage_url=author_db.homepage_url,
                    category=author_db.category
                )

                # 采集笔记
                # 注意: 这里需要实际的 MCP 客户端支持
                # notes = await self.collector.collect_author_notes(author)
                notes = []  # 暂时为空

                logger.info(f"采集到 {len(notes)} 篇笔记")
                total_notes += len(notes)

                # 处理每篇笔记
                for note in notes:
                    # 检查是否已采集
                    existing = self.db.query(NoteDB).filter(NoteDB.note_id == note.note_id).first()
                    if existing:
                        logger.debug(f"笔记已存在: {note.title}")
                        continue

                    # 保存到数据库
                    note_db = NoteDB(
                        note_id=note.note_id,
                        author_user_id=note.author_user_id,
                        title=note.title,
                        content=note.content,
                        note_url=note.note_url,
                        cover_image=note.cover_image,
                        publish_time=note.publish_time,
                        likes_count=note.likes_count,
                        collected=True
                    )
                    self.db.add(note_db)
                    new_notes += 1

                    # 同步到飞书
                    record_id = self.feishu_client.add_note_to_table(note)
                    if record_id:
                        note_db.synced_to_feishu = True
                        note_db.feishu_record_id = record_id
                        synced_notes += 1

                    self.db.commit()

                # 延迟，避免请求过快
                time.sleep(config.COLLECTION_DELAY)

            # 更新任务状态
            task.status = 'completed'
            task.total_notes = total_notes
            task.new_notes = new_notes
            task.synced_notes = synced_notes
            task.completed_at = datetime.now()
            self.db.commit()

            logger.info("=" * 60)
            logger.info(f"✅ 采集任务完成!")
            logger.info(f"总笔记数: {total_notes}, 新采集: {new_notes}, 已同步: {synced_notes}")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"采集任务失败: {e}")
            task.status = 'failed'
            task.error_message = str(e)
            task.completed_at = datetime.now()
            self.db.commit()

    def start(self):
        """启动应用"""
        self.initialize()

        # 启动调度器
        self.scheduler.start()

        logger.info("\n✅ 应用已启动!")
        logger.info(f"定时任务: 每天 {config.SCHEDULE_TIME} 自动执行")
        logger.info("按 Ctrl+C 停止应用\n")

        try:
            # 保持运行
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n正在停止应用...")
            self.scheduler.stop()
            self.db.close()
            logger.info("应用已停止")


def main():
    """主函数"""
    app = CollectorApp()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "add-author":
            # 添加博主示例
            if len(sys.argv) < 4:
                print("用法: python main.py add-author <user_id> <nickname> <homepage_url>")
                sys.exit(1)

            user_id = sys.argv[2]
            nickname = sys.argv[3]
            homepage_url = sys.argv[4]
            app.initialize()
            app.add_author(user_id, nickname, homepage_url)

        elif command == "run-now":
            # 立即执行一次采集
            app.initialize()
            app.run_collection_task()

        elif command == "start":
            # 启动定时任务
            app.start()

        else:
            print(f"未知命令: {command}")
            print("可用命令: add-author, run-now, start")

    else:
        # 默认启动
        app.start()


if __name__ == "__main__":
    main()
