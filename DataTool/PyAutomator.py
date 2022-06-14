
import time
import datetime
import schedule
import ScriptAutomation


def job():
    
    current_time = datetime.datetime.now() 
    print("Automated Execution")
    print(current_time)
    
    # Main.run_my_main()
    ScriptAutomation.run()
    print("Execution Complete")

# Run job every day at specific HH:MM 
interval = schedule.every().day.at("11:45").do(job)
# Cancel a job
#schedule.cancel_job(interval)

while True:
    schedule.run_pending()
    time.sleep(1)
