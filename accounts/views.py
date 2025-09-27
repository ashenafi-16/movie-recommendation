from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, PasswordChangeSerializer, ProfileSerializer
from .tasks import email_verification_message
from .base.store_token import set_token_cookies,delete_token_cookies
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.middleware.csrf import rotate_token
from .models import Profile
from django.contrib.auth import logout

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

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
    
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Remove Django session
        
        logout(request)

        # Remove JWT cookies if you use them
        response = Response({'detail': 'Logged out successfully'}, status=200)
        delete_token_cookies(response)

        return response

# class LogoutView(APIView):
#     def post(self,request):
#         response = Response({'detail': 'Logged out successfully'},status=status.HTTP_200_OK)
#         delete_token_cookies(response)
#         print("yes-------")
#         return response
    
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'wrong password'}, status=400)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'password changed successfully'})


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile
    
    
















# import requests
# from django.http import JsonResponse

# def fetch_movie(request):
#     url = "https://api.themoviedb.org/3/movie/popular"
#     params = {
#         'api_key': "2a8564a8cddfad3a7f01f71fffc82c53",
#         'language': 'en_US',
#         'page': 1

#     }
#     response = requests.get(url,params=params)
#     if response.status_code == 200:
#         data = response.json()
#         return JsonResponse(data)
#     else: 
#         return JsonResponse({'error':'faild to fetch data'}, status=500)
