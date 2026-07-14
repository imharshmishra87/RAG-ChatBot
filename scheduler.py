from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from Services.cleanup import cleanup_inactive_chats



scheduler=BackgroundScheduler(timezone="Asia/Kolkata")

scheduler.add_job(
    cleanup_inactive_chats,
    trigger="interval",
    minutes=5,
    id="CLIC_01"
)