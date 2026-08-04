from django.db import models
from Resume_Parser_App.models import Resume 

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Resume Match with Job Description Module.
class JobDescription(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

class CandidateResume(models.Model):
    name = models.CharField(max_length=255)
    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True)
    resume_text = models.TextField(blank=True, null=True)

class ResumeMatchResult(models.Model):
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    candidate = models.ForeignKey(CandidateResume, on_delete=models.CASCADE)
    match_percentage = models.FloatField()
    matched_skills = models.TextField()
    missing_skills = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class JobRecommendation(models.Model):
    candidate = models.ForeignKey(CandidateResume, on_delete=models.CASCADE, null=True)
    job = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)



#Resume Download History API 
class ResumeDownloadHistory(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="download_history")
    download_date = models.DateTimeField(auto_now_add=True)
    version = models.CharField(max_length=50, default="v1")

    def __str__(self):
        return f"{self.resume.file.name} downloaded on {self.download_date} (version {self.version})"
