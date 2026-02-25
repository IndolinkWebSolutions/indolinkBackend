# dashboard/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from users.models import UserProfile
from leads.models import UserLeadAccess
from leads.serializers import LeadPrivateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import CompanyProfile, ClientProducts
from .serializers import CompanySerializers, ClientProductsSerializers

from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user

    profile = UserProfile.objects.filter(user=user).first()

    profile_data = {
        "name": user.get_full_name() or user.username,
        "email": user.email,
        "weekly_lead_limit": profile.weekly_lead_limit if profile else 0,
    }

    unlocked_leads_qs = UserLeadAccess.objects.filter(
        user=user
    ).select_related("lead").order_by("-accessed_at")

    unlocked_leads = [
        {
            "lead": LeadPrivateSerializer(ula.lead).data,
            "accessed_at": ula.accessed_at
        }
        for ula in unlocked_leads_qs
    ]

    return Response({
        "profile": profile_data,
        "unlocked_leads": unlocked_leads
    })


class CompanyProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        profile = CompanyProfile.objects.filter(
            name=request.user
        ).first()

        if not profile:

            return Response({}, status=200)

        return Response(CompanySerializers(profile).data)


    def post(self, request):

        serializer = CompanySerializers(data=request.data)

        if serializer.is_valid():

            serializer.save(name=request.user)

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


    def put(self, request):

        profile = CompanyProfile.objects.get(
            name=request.user
        )

        serializer = CompanySerializers(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save(name=request.user)

            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"})
        except Exception:
            return Response({"error": "Invalid token"}, status=400)

# class ClientProductView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         products = ClientProductsSerializers(data=request.data)
#         print("bina save kiye", products)
#         if products.is_valid():
#             products.save()
#             print("ye save ho gya")
#             return Response({'Your product is successfully submitted !'}, status= status.HTTP_201_CREATED)
#         print(products.errors)
#         return Response(products.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def get(self, request):
#         products = ClientProducts.objects.select_related('user_profile__user').filter(user_profile__user=request.user)
#         serializer = ClientProductsSerializers(products, many=True)
#         return Response(serializer.data)

class ClientProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        products = ClientProductsSerializers(data = request.data, context = {'request':request})

        if products.is_valid():
            products.save()
            return Response({'msg':'Your product is added !'}, status = status.HTTP_201_CREATED )
        

        return Response(products.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        products = ClientProducts.objects.select_related('user_profile__user').filter(user_profile__user = request.user)

        serializers = ClientProductsSerializers(products, many=True, context = {'request':request})

        return Response(serializers.data)

