import time
import schedule

def job():
    timeStr = time.strftime("%Y-%m-%d %H:%M:%S")
    print("Job run time:", timeStr)
    
job()

schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()