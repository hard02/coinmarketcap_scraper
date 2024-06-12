# scraper/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ScrapeJob, ScrapeTask
import uuid

class ScraperViewTests(APITestCase):
    
    def test_start_scraping(self):
        url = reverse('start_scraping')
        data = {'coins': ['bitcoin', 'ethereum']}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('job_id', response.data)
        
        # Check if the job was created
        job_id = response.data['job_id']
        job = ScrapeJob.objects.get(job_id=job_id)
        self.assertIsNotNone(job)

    def test_start_scraping_invalid_input(self):
        url = reverse('start_scraping')
        data = {'coins': ['bitcoin', 123]}  # Invalid input, 123 is not a string
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_scraping_status(self):
        # Create a job and some tasks for testing
        job = ScrapeJob.objects.create()
        ScrapeTask.objects.create(job=job, coin='bitcoin', status='completed', data={'price': 30000})
        ScrapeTask.objects.create(job=job, coin='ethereum', status='pending', data={})

        url = reverse('scraping_status', args=[job.job_id])
        
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_id'], job.job_id)
        self.assertEqual(len(response.data['tasks']), 2)
        
    def test_scraping_status_not_found(self):
        url = reverse('scraping_status', args=[uuid.uuid4()])  # Use a random UUID that doesn't exist
        
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
