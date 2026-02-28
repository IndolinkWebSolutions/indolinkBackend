from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'name',
            'email',
            'mobile_number',
            'age',
            'weekly_lead_limit',
            'created_at',
        ]




class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=15)
    age = serializers.IntegerField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_mobile_number(self, value):
        if UserProfile.objects.filter(mobile_number=value).exists():
            raise serializers.ValidationError("Mobile number already exists")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )

        profile = UserProfile.objects.create(
            user=user,
            name=validated_data['name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            age=validated_data.get('age'),
            weekly_lead_limit=0   # 👈 default NO access
        )

        return profile




class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist")
        return value
    


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=6)

    def validate(self, attrs):
        try:
            uid = urlsafe_base64_decode(attrs['uid']).decode()
            user = User.objects.get(id=uid)
        except Exception:
            raise serializers.ValidationError("Invalid user")

        if not PasswordResetTokenGenerator().check_token(user, attrs['token']):
            raise serializers.ValidationError("Invalid or expired token")

        attrs['user'] = user
        return attrs



from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import UserProfile


# 🔹 1. Email Check Serializer
class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email not registered")
        return value

# 🔹 2. Reset Password Serializer

from rest_framework import serializers
from .models import UserProfile


class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField()

    password = serializers.CharField(min_length=6)


    def validate(self, data):

        try:
            userprofile = UserProfile.objects.get(
                reset_token=data["token"]
            )

        except UserProfile.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid or expired token"
            )

        data["userprofile"] = userprofile

        return data


    def save(self):

        userprofile = self.validated_data["userprofile"]

        password = self.validated_data["password"]

        # 🔹 Django User model password update

        django_user = userprofile.user

        django_user.set_password(password)

        django_user.save()

        # 🔹 Token remove

        userprofile.reset_token = None

        userprofile.save()

        return userprofile