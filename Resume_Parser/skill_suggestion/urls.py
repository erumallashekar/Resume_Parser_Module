from django.urls import path
from .views import SkillSuggestionAPI

urlpatterns = [
    path('suggest/', SkillSuggestionAPI.as_view(), name='skill-suggest'),
]
