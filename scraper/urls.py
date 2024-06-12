# scraper/urls.py

from django.urls import path
from .views import StartScraping, ScrapingStatus

urlpatterns = [
    path('api/taskmanager/start_scraping', StartScraping.as_view(), name='start_scraping'),
    path('api/taskmanager/scraping_status/<uuid:job_id>', ScrapingStatus.as_view(), name='scraping_status'),
]
