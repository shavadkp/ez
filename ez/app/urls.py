# app/urls.py
from django.urls import path
from .views import (
    SubmitJobView, JobStatusView, JobResultView, CancelJobView
)

urlpatterns = [
    path("jobs/", SubmitJobView.as_view()),
    path("jobs/<uuid:pk>/", JobStatusView.as_view()),
    path("jobs/<uuid:pk>/result/", JobResultView.as_view()),
    path("jobs/<uuid:job_id>/cancel/", CancelJobView.as_view()),
]
