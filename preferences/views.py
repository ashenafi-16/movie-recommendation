from rest_framework import viewsets, permissions
from .models import UserPreferenceProfile, UserTagPreference
from .serializers import UserPreferenceProfileSerializer, UserTagPreferenceSerializer

class UserPreferenceProfileViewSet(viewsets.ModelViewSet):
    queryset = UserPreferenceProfile.objects.all()
    serializer_class = UserPreferenceProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UserTagPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserTagPreference.objects.all()
    serializer_class = UserTagPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    