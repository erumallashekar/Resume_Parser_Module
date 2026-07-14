from django.db import models

# Create your models here.

class Resume(models.Model):
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class PersonalInfo(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="personal_info")
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)

class Summary(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="summary")
    text = models.TextField(blank=True)

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=255)

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="education")
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255, blank=True)
    start_year = models.CharField(max_length=10, blank=True)
    end_year = models.CharField(max_length=10, blank=True)

class WorkExperience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="work_experience")
    company = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.CharField(max_length=20, blank=True)
    end_date = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

class Certification(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="certifications")
    name = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255, blank=True)

class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="languages")
    name = models.CharField(max_length=255)
    proficiency = models.CharField(max_length=50, blank=True)
