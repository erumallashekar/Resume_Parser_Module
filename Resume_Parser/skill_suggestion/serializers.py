from rest_framework import serializers
from .models import Skill
#Resume Match 
from .models import Skill, JobDescription, CandidateResume, ResumeMatchResult, JobRecommendation, ResumeDownloadHistory

class skillserializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ["id", "title", "description"]

class CandidateResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateResume
        fields = ["id", "name", "resume_file", "resume_text"]

class ResumeMatchResultSerializer(serializers.ModelSerializer):
    job = JobDescriptionSerializer()
    candidate = CandidateResumeSerializer()

    class Meta:
        model = ResumeMatchResult
        fields = [
            "id",
            "job",
            "candidate",
            "match_percentage",
            "matched_skills",
            "missing_skills",
            "summary",
            "created_at",
        ]

class JobRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRecommendation
        fields = ["id", "candidate", "job", "score", "created_at"]

#Resume Download History API 
class ResumeDownloadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeDownloadHistory
        fields = ["id", "resume", "download_date", "version"]
