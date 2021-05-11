from crontab import CronTab

cron = CronTab(user='root')

iter = cron.find_comment('medipal_sendtexts')

for job in iter:
    cron.remove(job)

cron.write()