from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Skill
from .serializers import skillserializer

# Create your views here.

class SkillSuggestionAPI(APIView):
    def post(self, request):
        # Validate input
        candidate_input = request.data.get('input')
        if not candidate_input:
            return Response(
                {"error": "Input (job title, resume, or skills) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simple suggestion logic (you can expand with NLP later)
        suggestions = Skill.objects.filter(name__icontains=candidate_input[:3])[:5]

        serializer = skillserializer(suggestions, many=True)
        return Response({"suggested_skills": serializer.data}, status=status.HTTP_200_OK)
