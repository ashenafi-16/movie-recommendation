from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2', 'email', 'name')
        extra_kwargs = {
            "email": {"required": True},
            "name": {"required": True},
        }

    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "password fields didn't match."})
        return attrs
      
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User.objects.create(
            email = validated_data['email'],
            name=validated_data['name'],
            is_active=False # keep inactive until email verification
        )
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "name", "oauth_provider", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "is_active", "created_at", "updated_at")

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    print("serializer start ", email, password)
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        print("check validation now ----", email, password,data)

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        return data