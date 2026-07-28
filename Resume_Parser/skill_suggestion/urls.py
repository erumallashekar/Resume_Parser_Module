from django.urls import path
from .views import SkillSuggestionAPI
from .views import ResumeMatchAPI

urlpatterns = [
    path('suggest/', SkillSuggestionAPI.as_view(), name='skill-suggest'),
    path("resume-match/", ResumeMatchAPI.as_view(), name="resume-match"),
]

