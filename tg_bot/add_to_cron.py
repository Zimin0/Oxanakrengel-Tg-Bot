from crontab import CronTab
import os

cron = CronTab(user=True)

path = os.path.abspath("./json_file.py")
products_json_path = os.path.abspath("./products_json")

job_upload_json = cron.new(command="python " + "'" + path + "'")
job_upload_json.minute.every(1)

job_clear_products = cron.new(command=f"rm -rf {products_json_path}/*")
job_clear_products.minute.every(1) 

cron.write()
