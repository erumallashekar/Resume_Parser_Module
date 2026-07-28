from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill
from .serializers import skillserializer
# Resume Match libraries
from .utils import extract_text_from_pdf, match_resume_with_job
from .models import CandidateResume, JobDescription, ResumeMatchResult
from .serializers import ResumeMatchResultSerializer

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

#Resume Match Views 
# class ResumeMatchAPI(APIView):
#     def post(self, request):
#         job_description_text = request.data.get("job_description")
#         resume_file = request.FILES.get("resume")
#         candidate_name = request.data.get("name", "Unknown Candidate")

#         if not job_description_text or not resume_file:
#             return Response({"error": "Job description and resume file are required."},
#                             status=status.HTTP_400_BAD_REQUEST)

#         job = JobDescription.objects.create(title="Uploaded Job", description=job_description_text)

#         resume_file = request.FILES.get("resume")
#         resume_text = extract_text_from_pdf(resume_file)

#         candidate = CandidateResume.objects.create(
#             name=candidate_name,
#             resume_file=resume_file,
#             resume_text=resume_text
#         )

#         match_percentage, matched, missing, summary = match_resume_with_job(resume_text, job_description_text)

#         result = ResumeMatchResult.objects.create(
#             job=job,
#             candidate=candidate,
#             match_percentage=match_percentage,
#             matched_skills=", ".join(matched),
#             missing_skills=", ".join(missing),
#             summary=summary
#         )

#         serializer = ResumeMatchResultSerializer(result)
#         return Response(serializer.data, status=status.HTTP_200_OK)


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
