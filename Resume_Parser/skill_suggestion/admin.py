from django.contrib import admin
from .models import JobDescription, CandidateResume, ResumeMatchResult

# Register your models here.
admin.site.register(JobDescription)
admin.site.register(CandidateResume)
admin.site.register(ResumeMatchResult)
