"""
飞书多维表格集成模块
"""
from typing import List, Dict, Optional
from loguru import logger
import lark_oapi as lark
from lark_oapi.api.bitable.v1 import *
import config
from models import Note


class FeishuClient:
    """飞书客户端"""

    def __init__(self):
        """初始化飞书客户端"""
        self.app_id = config.FEISHU_APP_ID
        self.app_secret = config.FEISHU_APP_SECRET
        self.table_app_token = config.FEISHU_TABLE_APP_TOKEN
        self.table_id = config.FEISHU_TABLE_ID

        # 创建飞书客户端
        self.client = lark.Client.builder() \
            .app_id(self.app_id) \
            .app_secret(self.app_secret) \
            .build()

        logger.info("飞书客户端初始化成功")

    def add_note_to_table(self, note: Note) -> Optional[str]:
        """
        将笔记添加到飞书多维表格

        Args:
            note: 笔记对象

        Returns:
            飞书记录 ID，失败返回 None
        """
        try:
            # 构造记录数据
            fields = {
                "标题": note.title,
                "作者": note.author_user_id,
                "内容摘要": note.content[:500] if note.content else "",  # 限制长度
                "笔记链接": note.note_url,
                "封面图": note.cover_image,
                "发布时间": note.publish_time or "",
                "点赞数": note.likes_count,
                "笔记ID": note.note_id,
                "采集时间": note.created_at.strftime("%Y-%m-%d %H:%M:%S") if note.created_at else ""
            }

            # 创建记录请求
            request = CreateAppTableRecordRequest.builder() \
                .app_token(self.table_app_token) \
                .table_id(self.table_id) \
                .request_body(AppTableRecord.builder()
                              .fields(fields)
                              .build()) \
                .build()

            # 发送请求
            response = self.client.bitable.v1.app_table_record.create(request)

            # 检查响应
            if not response.success():
                logger.error(f"添加记录失败: {response.code} - {response.msg}")
                return None

            record_id = response.data.record.record_id
            logger.info(f"成功添加笔记到飞书: {note.title}, record_id={record_id}")
            return record_id

        except Exception as e:
            logger.error(f"添加笔记到飞书失败: {e}")
            return None

    def batch_add_notes(self, notes: List[Note]) -> Dict[str, int]:
        """
        批量添加笔记到飞书

        Args:
            notes: 笔记列表

        Returns:
            统计信息 {'success': 成功数, 'failed': 失败数}
        """
        stats = {'success': 0, 'failed': 0}

        for note in notes:
            record_id = self.add_note_to_table(note)
            if record_id:
                stats['success'] += 1
                note.synced_to_feishu = True
                note.feishu_record_id = record_id
            else:
                stats['failed'] += 1

        logger.info(f"批量添加完成: 成功 {stats['success']}, 失败 {stats['failed']}")
        return stats

    def check_record_exists(self, note_id: str) -> bool:
        """
        检查记录是否已存在

        Args:
            note_id: 笔记 ID

        Returns:
            是否存在
        """
        try:
            # 构造查询请求
            request = ListAppTableRecordRequest.builder() \
                .app_token(self.table_app_token) \
                .table_id(self.table_id) \
                .filter(f'"笔记ID" = "{note_id}"') \
                .build()

            # 发送请求
            response = self.client.bitable.v1.app_table_record.list(request)

            if not response.success():
                logger.warning(f"查询记录失败: {response.code} - {response.msg}")
                return False

            # 检查是否有记录
            exists = response.data.total > 0
            return exists

        except Exception as e:
            logger.error(f"检查记录是否存在失败: {e}")
            return False

    def update_table_schema(self):
        """
        更新或创建表格字段（仅首次使用时需要）
        """
        logger.info("注意: 需要手动在飞书多维表格中创建以下字段:")
        fields = [
            "标题 (Text)",
            "作者 (Text)",
            "内容摘要 (Text)",
            "笔记链接 (URL)",
            "封面图 (URL)",
            "发布时间 (Text)",
            "点赞数 (Number)",
            "笔记ID (Text)",
            "采集时间 (DateTime or Text)"
        ]
        for field in fields:
            logger.info(f"  - {field}")
