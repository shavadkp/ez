# app/serializers.py
from rest_framework import serializers
from .models import Job, JobResult


class JobSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id", "source_type", "source_text", "source_file", "source_url",
            "target_languages", "priority", "callback_url", "metadata"
        ]

    def validate(self, data):
        if data["source_type"] == "text" and not data.get("source_text"):
            raise serializers.ValidationError("source_text is required.")
        if data["source_type"] == "file" and not data.get("source_file"):
            raise serializers.ValidationError("source_file is required.")
        return data


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id", "status", "progress", "priority",
            "submitted_at", "started_at", "finished_at",
            "target_languages", "error_message"
        ]


class JobResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobResult
        fields = ["job", "result_data", "created_at"]
