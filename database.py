"""
数据库配置和操作
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import config

Base = declarative_base()


class AuthorDB(Base):
    """博主表"""
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(100), unique=True, nullable=False, index=True)
    nickname = Column(String(200), nullable=False)
    homepage_url = Column(String(500), nullable=False)
    category = Column(String(50), default='AI')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class NoteDB(Base):
    """笔记表"""
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    note_id = Column(String(100), unique=True, nullable=False, index=True)
    author_user_id = Column(String(100), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, default='')
    note_url = Column(String(500), nullable=False)
    cover_image = Column(String(500), default='')
    publish_time = Column(String(100))
    likes_count = Column(Integer, default=0)
    collected = Column(Boolean, default=False)
    synced_to_feishu = Column(Boolean, default=False)
    feishu_record_id = Column(String(100), default='')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class CollectionTaskDB(Base):
    """采集任务表"""
    __tablename__ = 'collection_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_type = Column(String(20), nullable=False)  # auto/manual
    status = Column(String(20), default='pending')  # pending/running/completed/failed
    total_authors = Column(Integer, default=0)
    total_notes = Column(Integer, default=0)
    new_notes = Column(Integer, default=0)
    synced_notes = Column(Integer, default=0)
    error_message = Column(Text, default='')
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)


# 创建数据库引擎
engine = create_engine(f'sqlite:///{config.DATABASE_PATH}', echo=False)

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_database():
    """初始化数据库"""
    config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
