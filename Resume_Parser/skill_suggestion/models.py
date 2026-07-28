from django.db import models

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
