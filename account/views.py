from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .tasks import email_verification_message
from .base.store_token import set_token_cookies
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import rotate_token
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        email_verification_message.delay(user.email)
        
        return Response(
            {'message': "User registered successfully. Please verify your email."},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)
        
        if not user:
            raise AuthenticationFailed
        
        response = Response({"Email": {user.email}, 'Name': {user.name}}, status=status.HTTP_200_OK)

        # set auth cookies
        refresh = RefreshToken.for_user(user)
        set_token_cookies(response,str(refresh.access_token), str(refresh))

        # for security reasons, CSRF tokens are rotated each time a user logs in.
        rotate_token(request)

        return response