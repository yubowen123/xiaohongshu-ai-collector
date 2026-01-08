"""
测试脚本 - 小红书内容采集

这个脚本展示了如何使用采集器进行实际采集
"""
from datetime import datetime
from loguru import logger
import sys
sys.path.append('.')

from database import init_database, SessionLocal, AuthorDB
from integrations.feishu import FeishuClient
from models import Author, Note


# 配置日志
logger.add("logs/test.log", rotation="10 MB")


def test_database():
    """测试数据库连接"""
    logger.info("测试数据库...")

    init_database()
    db = SessionLocal()

    # 测试添加博主
    test_author = AuthorDB(
        user_id="test_user_123",
        nickname="测试博主",
        homepage_url="https://www.xiaohongshu.com/user/profile/test_user_123",
        category="AI",
        is_active=True
    )

    # 检查是否已存在
    existing = db.query(AuthorDB).filter(AuthorDB.user_id == "test_user_123").first()
    if existing:
        logger.info("测试博主已存在")
    else:
        db.add(test_author)
        db.commit()
        logger.info("✅ 测试博主添加成功")

    # 查询所有博主
    authors = db.query(AuthorDB).all()
    logger.info(f"数据库中共有 {len(authors)} 个博主")

    db.close()
    logger.info("✅ 数据库测试通过")


def test_feishu():
    """测试飞书连接"""
    logger.info("测试飞书连接...")

    try:
        feishu_client = FeishuClient()

        # 创建测试笔记
        test_note = Note(
            note_id="test_note_123",
            author_user_id="test_user_123",
            title="测试笔记 - " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            content="这是一条测试笔记内容",
            note_url="https://www.xiaohongshu.com/explore/test_note_123",
            cover_image="https://example.com/image.jpg",
            publish_time="2024-01-08",
            likes_count=100,
            created_at=datetime.now()
        )

        # 添加到飞书
        record_id = feishu_client.add_note_to_table(test_note)

        if record_id:
            logger.info(f"✅ 飞书测试通过，记录 ID: {record_id}")
        else:
            logger.error("❌ 飞书添加记录失败")

    except Exception as e:
        logger.error(f"❌ 飞书测试失败: {e}")
        logger.info("请检查 .env 文件中的飞书配置")


def print_usage():
    """打印使用说明"""
    print("""
=================================================================
小红书 AI 内容采集器 - 测试脚本
=================================================================

可用测试命令:

1. 测试数据库:
   python test_collector.py db

2. 测试飞书连接:
   python test_collector.py feishu

3. 查看所有博主:
   python test_collector.py list-authors

=================================================================

使用 Chrome DevTools MCP 进行实际采集:

由于 Chrome DevTools MCP 只能在 Claude Code 交互环境中使用，
实际采集需要在 Claude Code 中执行以下操作：

1. 在 Chrome 浏览器中打开小红书并登录
2. 打开博主主页
3. 使用 Claude Code 的 MCP 工具获取页面快照
4. 解析快照内容提取笔记信息
5. 保存到数据库和飞书

详细步骤请参考 README.md 中的"使用 Chrome DevTools MCP"章节

=================================================================
""")


def list_authors():
    """列出所有博主"""
    db = SessionLocal()
    authors = db.query(AuthorDB).all()

    print(f"\n找到 {len(authors)} 个博主:\n")
    print(f"{'ID':<5} {'用户ID':<25} {'昵称':<20} {'状态':<10}")
    print("=" * 70)

    for author in authors:
        status = "✅ 启用" if author.is_active else "❌ 禁用"
        print(f"{author.id:<5} {author.user_id:<25} {author.nickname:<20} {status:<10}")

    db.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)

    command = sys.argv[1]

    if command == "db":
        test_database()
    elif command == "feishu":
        test_feishu()
    elif command == "list-authors":
        list_authors()
    else:
        print(f"未知命令: {command}")
        print_usage()
