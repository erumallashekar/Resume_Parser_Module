from django.urls import path
from .views import SkillSuggestionAPI
from .views import ResumeMatchAPI, JobRecommendationAPI

urlpatterns = [
    path('suggest/', SkillSuggestionAPI.as_view(), name='skill-suggest'),
    path("resume-match/", ResumeMatchAPI.as_view(), name="resume-match"),
    path("job-recommendations/", JobRecommendationAPI.as_view(), name="job-recommendations"),

]

