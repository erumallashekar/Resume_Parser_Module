from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


from .models import Resume, PersonalInfo, Summary, Skill, Education, WorkExperience, Project, Certification, Language
from .serializers import (
    ResumeSerializer,
    PersonalInfoSerializer,
    SummarySerializer,
    SkillSerializer,
    EducationSerializer,
    WorkExperienceSerializer,
    ProjectSerializer,
    CertificationSerializer,
    LanguageSerializer,
)
from .utils import parse_resume

class PersonalInfoViewSet(viewsets.ModelViewSet):
    queryset = PersonalInfo.objects.all()
    serializer_class = PersonalInfoSerializer

class SummaryViewSet(viewsets.ModelViewSet):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        # Save the uploaded resume file first
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume = serializer.save()

        # Auto‑parse immediately after upload
        data = parse_resume(resume.file.path)

        # Save parsed data into models
        PersonalInfo.objects.create(
            resume=resume,
            name=data.get("name", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            address=data.get("address", "")
        )
        Summary.objects.create(resume=resume, text=data.get("summary", ""))

        for skill in data.get("skills", []):
            Skill.objects.create(resume=resume, name=skill)

        for edu in data.get("education", []):
            Education.objects.create(
                resume=resume,
                institution=edu.get("institution", ""),
                degree=edu.get("degree", ""),
                start_year=edu.get("start_year", ""),
                end_year=edu.get("end_year", "")
            )

        for exp in data.get("experience", []):
            WorkExperience.objects.create(
                resume=resume,
                company=exp.get("company", ""),
                role=exp.get("role", ""),
                start_date=exp.get("start_date", ""),
                end_date=exp.get("end_date", ""),
                description=exp.get("description", "")
            )

        for project in data.get("projects", []):
            Project.objects.create(
                resume=resume,
                title=project.get("title", ""),
                description=project.get("description", "")
            )

        for certification in data.get("certifications", []):
            Certification.objects.create(resume=resume, name=certification)

        for language in data.get("languages", []):
            Language.objects.create(resume=resume, name=language)

        return Response({
            "message": "Resume uploaded and parsed successfully",
            "resume_id": resume.id,
            "parsed_data": data,
        })

    @action(detail=False, methods=["post"])
    def debug_parse(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "Please upload a file under 'file'."}, status=status.HTTP_400_BAD_REQUEST)

        temp_path = Path("tmp_debug_resume")
        temp_path.write_bytes(file.read())
        parsed = parse_resume(str(temp_path))
        temp_path.unlink(missing_ok=True)

        return Response({"parsed_data": parsed})
