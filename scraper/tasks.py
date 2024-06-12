from celery import shared_task
from .coinmarketcap import CoinMarketCap
from .models import ScrapeJob, ScrapeTask

@shared_task
def scrape_coin_data(coin, task_id):
    scraper = CoinMarketCap()
    data = scraper.fetch_coin_data(coin)
    task = ScrapeTask.objects.get(id=task_id)
    task.data = data
    task.status = 'COMPLETED'
    task.save()

@shared_task
def start_scraping_job(job_id, coins):
    job = ScrapeJob.objects.get(id=job_id)
    for coin in coins:
        task = ScrapeTask.objects.create(job=job, coin=coin)
        scrape_coin_data.delay(coin, task.id)
    job.status = 'IN_PROGRESS'
    job.save()