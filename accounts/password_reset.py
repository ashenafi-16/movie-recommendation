from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .tasks import password_reset
from django.contrib.auth import password_validation

User = get_user_model()

class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'email': 'Email field is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail': 'If your email exists, a reset Link will be sent'}, status=status.HTTP_200_OK)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://yourfrontend.com/reset-password/{uid}/{token}/"

        password_reset.delay(reset_link, user.email)

        return Response({'detail':"If your email exists, a reset link will be sent"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get('new_password')
        if not password:
            return Response({'new_password': 'password field is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'detail': "Invalid link"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user,token):
            return Response({'detail': 'Invalid token'}, status= status.HTTP_400_BAD_REQUEST)
        
        password_validation.validate_password(password)
        user.set_password(password)
        user.save()
        return Response({'detail': 'Password has been reset successfully'})
    