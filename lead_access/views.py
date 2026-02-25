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
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrypt_lead(request, lead_id):

    user = request.user
    profile = user.userprofile

    # 1️⃣ Admin Access Check
    if profile.weekly_lead_limit == 0:
        return Response(
            {"error": "Access not granted by admin"},
            status=403
        )

    # 2️⃣ Weekly Count Check
    week_start = timezone.now() - timedelta(days=7)

    decrypted_count = UserDecryptedLead.objects.filter(
        user=user,
        decrypted_at__gte=week_start
    ).count()

    if decrypted_count >= profile.weekly_lead_limit:
        return Response(
            {"error": "Weekly limit exceeded"},
            status=403
        )

    lead = get_object_or_404(Lead, id=lead_id)

    # 3️⃣ Prevent Duplicate Count
    obj, created = UserDecryptedLead.objects.get_or_create(
        user=user,
        lead=lead
    )

    # Agar pehle se decrypt hai to count increase nahi karega

    return Response({
        "id": lead.id,
        "name": lead.name,
        "requirements": lead.requirements,
        "company": lead.company,
        "location": lead.location,
        "email": lead.email,
        "mobile_number": lead.mobile_number,
        "created_at": lead.created_at,
    })