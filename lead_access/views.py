from django.shortcuts import render

# Create your views here.
# lead_access/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from users.models import UserProfile
from .models import UserDecryptedLead
from leads.models import Lead
from core.encryption import decrypt, encrypt

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrypt_lead(request, lead_id):

    user = request.user
    profile = user.userprofile
    limit = profile.weekly_decrypt_limit

    if limit == 0:
        return Response({"error": "Access not allowed"}, status=403)

    week_start = timezone.now() - timedelta(days=7)

    decrypted_count = UserDecryptedLead.objects.filter(
        user=user,
        decrypted_at__gte=week_start
    ).count()

    if decrypted_count >= limit:
        return Response({"error": "Weekly limit exceeded"}, status=403)

    lead = Lead.objects.get(id=lead_id)

    UserDecryptedLead.objects.create(user=user, lead=lead)

    return Response({
        "company_name": decrypt(encrypt(lead.company_name)),
        "country": decrypt(encrypt(lead.country)),
        "email": decrypt(encrypt(lead.email)),
        "phone": decrypt(encrypt(lead.phone)),
    })
