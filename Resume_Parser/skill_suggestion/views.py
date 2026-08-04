from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill
from .serializers import skillserializer, JobRecommendationSerializer
# Resume Match libraries
from .utils import extract_text_from_pdf, match_resume_with_job, recommend_jobs
from .models import CandidateResume, JobDescription, ResumeMatchResult, JobDescription, JobRecommendation
from .serializers import ResumeMatchResultSerializer
# ResumeDownloadAPI
from .models import ResumeDownloadHistory
from .serializers import ResumeDownloadHistorySerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse


class SkillSuggestionAPI(APIView):
    def get(self, request):
        """
        Simple GET handler so you can test in browser.
        """
        return Response(
            {"message": "Use POST with JSON body {'input': '...'} to get skill suggestions."},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
        Actual skill suggestion logic.
        """
        candidate_input = request.data.get('input')
        if not candidate_input:
            return Response(
                {"error": "Input (job title, resume, or skills) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Basic keyword matching
        suggestions = Skill.objects.filter(name__icontains=candidate_input[:3])[:5]
        serializer = skillserializer(suggestions, many=True)

        return Response({"suggested_skills": serializer.data}, status=status.HTTP_200_OK)


# Resume Match process
class ResumeMatchAPI(APIView):
    def post(self, request):
        # Collect inputs safely
        job_description_text = request.data.get("job_description")
        resume_file = request.FILES.get("resume")
        candidate_name = request.data.get("name", "Unknown Candidate")

        # Validate required fields
        if not job_description_text or not resume_file:
            return Response(
                {"error": "Job description and resume file are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Create job record
            job = JobDescription.objects.create(
                title="Uploaded Job",
                description=job_description_text
            )

            # Extract resume text safely (utils.py handles OCR lock)
            resume_text = extract_text_from_pdf(resume_file)

            # Create candidate record
            candidate = CandidateResume.objects.create(
                name=candidate_name,
                resume_file=resume_file,
                resume_text=resume_text
            )

            # Perform matching
            match_percentage, matched, missing, summary = match_resume_with_job(
                resume_text, job_description_text
            )

            # Save result
            result = ResumeMatchResult.objects.create(
                job=job,
                candidate=candidate,
                match_percentage=match_percentage,
                matched_skills=", ".join(matched),
                missing_skills=", ".join(missing),
                summary=summary
            )

            # Serialize and return
            serializer = ResumeMatchResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Catch OCR / parsing / DB errors gracefully
            return Response(
                {"error": f"Failed to process resume match: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Job Recommendation API
class JobRecommendationAPI(APIView):
    def post(self, request):
        candidate_id = request.data.get("candidate_id")
        resume_text = request.data.get("resume_text")

        if not candidate_id and not resume_text:
            return Response(
                {"error": "Either candidate_id or resume_text is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # If candidate_id is provided, fetch candidate resume
            candidate = None
            if candidate_id:
                candidate = CandidateResume.objects.get(id=candidate_id)
                resume_text = candidate.resume_text

            # Run recommendation logic
            recommended_jobs = recommend_jobs(resume_text)

            # Save recommendations (optional)
            results = []
            for job, score in recommended_jobs:
                rec = JobRecommendation.objects.create(
                    candidate=candidate,
                    job=job,
                    score=score
                )
                results.append(rec)

            serializer = JobRecommendationSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except CandidateResume.DoesNotExist:
            return Response(
                {"error": "Candidate not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to generate recommendations: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


#Resume Download History API 
class ResumeDownloadHistoryViewSet(viewsets.ModelViewSet):
    queryset = ResumeDownloadHistory.objects.all().order_by("-download_date")
    serializer_class = ResumeDownloadHistorySerializer

    @action(detail=True, methods=["get"], url_path="download")
    def download_resume(self, request, pk=None):
        resume = self.get_object()

        # ✅ Record download history automatically
        ResumeDownloadHistory.objects.create(
            resume=resume,
            version="v1"   # you can adjust versioning logic here
        )

        # ✅ Return the actual file as a download
        response = FileResponse(open(resume.file.path, "rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{resume.file.name}"'
        return response
