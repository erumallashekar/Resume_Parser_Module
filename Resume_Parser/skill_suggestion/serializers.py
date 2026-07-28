from rest_framework import serializers
from .models import Skill
#Resume Match 
from .models import Skill, JobDescription, CandidateResume, ResumeMatchResult

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
