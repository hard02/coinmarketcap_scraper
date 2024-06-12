# scraper/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapeJob, ScrapeTask
from .tasks import start_scraping_job
import uuid

class StartScraping(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        if not all(isinstance(coin, str) for coin in coins):
            return Response({'error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)
        
        job = ScrapeJob.objects.create()
        start_scraping_job.delay(job.id, coins)
        return Response({'job_id': job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapeJob.objects.get(job_id=job_id)
        except ScrapeJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        tasks = ScrapeTask.objects.filter(job=job)
        return Response({
            'job_id': job.job_id,
            'status': job.status,
            'tasks': [
                {
                    'coin': task.coin,
                    'data': task.data,
                    'status': task.status
                }
                for task in tasks
            ]
        })

