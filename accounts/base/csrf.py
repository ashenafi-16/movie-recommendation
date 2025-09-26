from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.views import APIView

class CSFRAPIView(APIView):
    def get(self,request):
        return Response({'token': get_token(request)})