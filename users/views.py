from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from .serializers import UserSignupSerializer
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from .serializers import ForgotPasswordSerializer
from django.conf import settings
from django.utils.timezone import now


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    profile = UserProfile.objects.select_related('user').get(
        user=request.user
    )
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializer(
        profile,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)





@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        with transaction.atomic():
            profile = serializer.save()
            user = profile.user
            refresh = RefreshToken.for_user(user)
                                                                                 
        return Response(
            {
                "message": "Signup successful",
                "user_id": profile.user.id,
                "username": profile.user.username,
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            },
            status=status.HTTP_201_CREATED
        )
    except Exception:
        return Response({'error':'Signup failled. please try again !'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

  

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error":"please enter your username and password"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error":"Invalid Credential"}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh)

            }, 
            status=status.HTTP_200_OK
        )
    


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(email=serializer.validated_data['email'])

        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset password:\n{reset_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return Response(
            {"message": "Password reset link sent to your email"},
            status=status.HTTP_200_OK
        )
    


from .serializers import ResetPasswordSerializer

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"message": "Password reset successful"},
            status=status.HTTP_200_OK
        )
    

