import logging
import os
import time

from celery import Celery
from celery.schedules import crontab
from celery_once import QueueOnce
# from . import cron_task
from core.config import REDIS_PASSWORD, REDIS_HOST, REDIS_PORT
from urllib import parse
from utils import constant

celery_app = None

if not bool(os.getenv('DOCKER')):  # if running example without docker
    celery_app = Celery(
        "worker",
        broker=f"redis://:{parse.quote(REDIS_PASSWORD)}@{REDIS_HOST}:{REDIS_PORT}/1",
        backend=f"redis://:{parse.quote(REDIS_PASSWORD)}@{REDIS_HOST}:{REDIS_PORT}/1",
        # 设置结果的保存时间（秒数，或者一个 timedelta 对象）
        result_expires=300,
        # 设置默认不存结果
        task_ignore_result=True
    )
    celery_app.conf.task_routes = {
        "app.worker.celery_worker.test_celery": "test-queue"
    }

    celery_app.conf.ONCE = {
        'backend': 'celery_once.backends.Redis',
        'settings': {
            'url': f"redis://:{parse.quote(REDIS_PASSWORD)}@{REDIS_HOST}:{REDIS_PORT}/1",
            'default_timeout': 60 * 60,
            # 'blocking': True,
            # 'blocking_timeout': 30    # 在引发异常之前，计划任务会阻止最多30秒尝试获取锁定。
        }
    }


    @celery_app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        # every 5 seconds.
        # sender.add_periodic_task(10.0, update_analysis_result_and_report.s(), name='每隔10秒获取分析结果和报告')

        # # Calls test('world') every 30 seconds
        # sender.add_periodic_task(30.0, test.s('world'), expires=10)

        # # Executes every Monday morning at 7:30 a.m.
        # sender.add_periodic_task(
        #     crontab(hour=7, minute=30, day_of_week=1),
        #     test.s('Happy Mondays!'),
        # )


else:  # running example with docker
    celery_app = Celery(
        "worker",
        backend="redis://:password123@redis:6379/0",
        broker="amqp://user:bitnami@rabbitmq:5672//"
    )
    celery_app.conf.task_routes = {
        "app.app.worker.celery_worker.test_celery": "test-queue"}

celery_app.conf.update(task_track_started=False)
