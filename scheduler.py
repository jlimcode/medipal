from crontab import CronTab

TIME_INTERVAL = 10
cron = CronTab(user='root')
job = cron.new(command='python send_messages.py', comment='medipal_sendtexts')
job.minute.every(TIME_INTERVAL)
cron.write()
