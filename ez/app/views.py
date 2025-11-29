from django.shortcuts import render

# Create your views here.
# app/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Job, JobResult
from .serializers import (
    JobSubmitSerializer, JobStatusSerializer, JobResultSerializer
)

from .tasks import process_translation_task


class SubmitJobView(generics.CreateAPIView):
    serializer_class = JobSubmitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        job = serializer.save(user=self.request.user)
        process_translation_task.delay(str(job.id))   # Enqueue Celery task


class JobStatusView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobStatusSerializer
    permission_classes = [IsAuthenticated]


class JobResultView(generics.RetrieveAPIView):
    queryset = JobResult.objects.all()
    serializer_class = JobResultSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        job_id = self.kwargs["pk"]
        return JobResult.objects.get(job_id=job_id)

class CancelJobView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
        except Job.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        if job.status in ("completed", "failed"):
            return Response({"error": "Cannot cancel"}, status=400)

        job.status = "cancelled"
        job.save()
        return Response({"status": "cancelled"})
