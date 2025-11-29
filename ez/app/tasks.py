# app/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Job, JobResult
import time
import random


@shared_task(bind=True, max_retries=3)
def process_translation_task(self, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return

    if job.status == "cancelled":
        return

    job.status = "in_progress"
    job.started_at = timezone.now()
    job.save()

    try:
        # Simple mock processing (simulate chunks)
        chunks = ["part1", "part2", "part3"]
        results = {}

        for lang in job.target_languages:
            translated = []
            for i, chunk in enumerate(chunks):
                time.sleep(1)  # simulate work
                translated.append(f"{chunk} -> translated({lang})")

                job.progress = int((i + 1) / len(chunks) * 100)
                job.save()

            results[lang] = " ".join(translated)

        JobResult.objects.create(job=job, result_data=results)

        job.status = "completed"
        job.progress = 100
        job.finished_at = timezone.now()
        job.save()

    except Exception as e:
        job.status = "failed"
        job.error_message = str(e)
        job.save()
        raise self.retry(exc=e, countdown=5)
