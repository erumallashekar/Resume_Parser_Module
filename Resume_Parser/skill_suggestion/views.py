from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill
from .serializers import skillserializer

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
