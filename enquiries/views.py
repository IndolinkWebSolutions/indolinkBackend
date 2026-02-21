from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils.timezone import now
from .models import Contact, HomePagePopUp
from .serializers import ContactSerializer, HomePopUpSerializer

class ContactAPIView(APIView):
    permission_classes = [AllowAny]  

    def post(self, request):
        today = now().date()
        email = request.data.get("email")

        if Contact.objects.filter(email=email, date=today).exists():
            return Response(
                {"detail": "You can submit the contact form only once per day."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Contact form submitted successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class HomePagePopUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        today = now().date()
        email = request.data.get("email")

        # ✅ Correct filtering
        if HomePagePopUp.objects.filter(
            email=email,
            create_at__date=today
        ).exists():
            return Response(
                {"message": "You can't submit the contact form more than once per day"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = HomePopUpSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Your Form successfully submitted!'},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

