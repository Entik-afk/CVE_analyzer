from apscheduler.schedulers.blocking import BlockingScheduler
import ingest



def run_ingest():
    try:
        ingest.main()
    except Exception as e:
        print(f"Chyba při spouštění ingest: {e}")


scheduler = BlockingScheduler()
scheduler.add_job(run_ingest, 'cron', hour=1)  # každý den v 1:00
print("Scheduler spuštěn - stahování CVEs každý den v 1:00")
scheduler.start()
