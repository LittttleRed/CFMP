from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job, register_events
from django_apscheduler.models import DjangoJobExecution
from . import models


scheduler = BackgroundScheduler()
# 调度器使用DjangoJobStore()
scheduler.add_jobstore(DjangoJobStore(), "default")

# @register_job(scheduler, "interval", seconds=5,id='job1', replace_existing=True)
def unban_task():
    """
    查询所有complaint review记录,查找created_at+ban_time<current并且target_type=1的条目,
    将target_id对应的user的status设置为0
    """
    print("unban_task")
    # for review in models.ComplaintReview.objects.filter(
    #     created_at__lt=datetime.now() + timedelta(days=models.ComplaintReview.objects.values('ban_time')),
    #     target_type=1
    # ):
    #     models.User.objects.filter(user_id=review.target_id).update(status=0)
# 实例化调度器

scheduler.remove_all_jobs()
scheduler.add_job(unban_task, "interval", minutes=1,id='job2', replace_existing=True)
# scheduler.start()
