from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import connection
from django.db.models import F, ExpressionWrapper, DateTimeField
from django.db.models.functions import Now
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events
from django_apscheduler.models import DjangoJobExecution
from . import models
from user.models import User

scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "interval", seconds=5,id='job1', replace_existing=True)
def unban_task():
    with connection.cursor() as cursor:
        # 解封用户
        cursor.execute("""
            UPDATE `user`
            SET status = 0
            WHERE user_id IN (
                SELECT cr.target_id
                FROM complaint_review cr
                WHERE cr.target_type = 1
                  AND DATE_ADD(cr.created_at, INTERVAL cr.ban_time DAY) <= NOW()
                  AND cr.ban_time!=0
            );
        """)

        # 删除已处理的封禁记录
        cursor.execute("""
            DELETE FROM complaint_review
            WHERE target_type = 1
              AND DATE_ADD(created_at, INTERVAL ban_time DAY) <= NOW()
              AND ban_time!=0;
        """)

# 实例化调度器

scheduler.remove_all_jobs()
scheduler.add_job(unban_task, "interval", minutes=1,id='job2', replace_existing=True)
# scheduler.start()
