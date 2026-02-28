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
    

import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CheckEmailSerializer, ResetPasswordSerializer
from .models import UserProfile


class CheckEmailAPIView(APIView):
    def post(self, request):
        serializer = CheckEmailSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = UserProfile.objects.get(email=email)

            token = str(uuid.uuid4())
            user.reset_token = token
            user.save()

            return Response({
                "message": "Email verified",
                "token": token
            })

        return Response(serializer.errors, status=400)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset successful"})

        return Response(serializer.errors, status=400)