import schedule
import time
import subprocess

print("eseguito schedule")

def job(saluto = "ciao"):
    bashCommand = "python /home/user/DDL-CRF/linux-tools/cron.py {}".format(saluto)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("eseguito!")
    

job(saluto = "inizializza ")

#schedule.every(0.1).minutes.do(job)
#schedule.every().hour.do(job)
schedule.every().day.at("10:00").do(job)
schedule.every().day.at("15:00").do(job)
schedule.every().day.at("22:00").do(job)
schedule.every().day.at("23:59").do(job)
#schedule.every(5).to(10).minutes.do(job)
#schedule.every().monday.do(job)
#schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
