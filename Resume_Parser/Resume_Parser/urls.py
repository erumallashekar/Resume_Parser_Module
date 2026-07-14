"""
URL configuration for Resume_Parser project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from Resume_Parser_App.views import ResumeViewSet, PersonalInfoViewSet, SummaryViewSet, SkillViewSet, EducationViewSet, WorkExperienceViewSet, ProjectViewSet, CertificationViewSet, LanguageViewSet
from django.contrib import admin  

router = DefaultRouter()
router.register(r"resumes", ResumeViewSet)
router.register(r"personal-info", PersonalInfoViewSet)
router.register(r"summaries", SummaryViewSet)
router.register(r"skills", SkillViewSet)
router.register(r"education", EducationViewSet)
router.register(r"work-experience", WorkExperienceViewSet)
router.register(r"projects", ProjectViewSet)
router.register(r"certifications", CertificationViewSet)
router.register(r"languages", LanguageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path("", include(router.urls)),
]