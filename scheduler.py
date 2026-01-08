"""
定时任务调度器
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from loguru import logger
import config


class CollectorScheduler:
    """采集调度器"""

    def __init__(self, collector_job):
        """
        初始化调度器

        Args:
            collector_job: 采集任务函数
        """
        self.scheduler = BackgroundScheduler(timezone=config.TIMEZONE)
        self.collector_job = collector_job
        logger.info(f"调度器初始化成功，时区: {config.TIMEZONE}")

    def start(self):
        """启动调度器"""
        # 解析定时时间
        hour, minute = map(int, config.SCHEDULE_TIME.split(':'))

        # 添加定时任务
        trigger = CronTrigger(hour=hour, minute=minute, timezone=config.TIMEZONE)
        self.scheduler.add_job(
            self.collector_job,
            trigger=trigger,
            id='daily_collection',
            name='每日采集任务',
            replace_existing=True
        )

        # 启动调度器
        self.scheduler.start()

        logger.info(f"✅ 调度器已启动，每天 {config.SCHEDULE_TIME} 自动执行采集任务")

        # 显示下次执行时间
        job = self.scheduler.get_job('daily_collection')
        if job:
            next_run = job.next_run_time
            logger.info(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

    def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        logger.info("调度器已停止")

    def run_now(self):
        """立即执行一次采集任务"""
        logger.info("手动触发采集任务...")
        self.collector_job()

    def get_status(self):
        """获取调度器状态"""
        if not self.scheduler.running:
            return {
                'running': False,
                'message': '调度器未运行'
            }

        job = self.scheduler.get_job('daily_collection')
        if not job:
            return {
                'running': True,
                'message': '调度器运行中，但未找到任务'
            }

        return {
            'running': True,
            'job_id': job.id,
            'job_name': job.name,
            'next_run_time': job.next_run_time.strftime('%Y-%m-%d %H:%M:%S') if job.next_run_time else None,
            'schedule_time': config.SCHEDULE_TIME,
            'timezone': config.TIMEZONE
        }
