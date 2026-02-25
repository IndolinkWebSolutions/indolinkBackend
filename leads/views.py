from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import timedelta
from django.db.models import Q
from .utils import weekly_lead_count
from .models import Lead, UserLeadAccess
from users.models import UserProfile
from .serializers import (
    LeadPublicSerializer,
    LeadPrivateSerializer
)
from core.pagination import StandardResultsSetPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elasticsearch.exceptions import ConnectionError
from core.pagination import StandardResultsSetPagination
from .documents import LeadDocument
from core.autocomplete import autocomplete
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q 
from .models import Lead, UserLeadAccess
from .serializers import LeadPublicSerializer, LeadPrivateSerializer
from core.autocomplete import autocomplete
import logging


@api_view(['GET'])
def lead_autocomplete(request):
    q = request.GET.get("q", "").lower()

    if not q or len(q) < 2:
        return Response([])

    redis = get_redis_connection("default")
    words = redis.smembers("lead:suggestions")

    suggestions = [
        word.decode("utf-8")
        for word in words
        if word.decode("utf-8").startswith(q)
    ]

    return Response(suggestions[:10])




logger = logging.getLogger(__name__)


@api_view(['GET'])
def lead_search(request):
    q = request.GET.get("q", "").strip().lower()
    page_size = int(request.GET.get("page_size", 20))

    qs = Lead.objects.all()

    suggestions = []

    # ---------- Redis Safe Block ----------
    if q:
        try:
            suggestions = autocomplete("lead_autocomplete", q, limit=10)
        except Exception as e:
            logger.warning(f"Redis failed, using DB fallback: {e}")
            suggestions = []

    # ---------- If Redis returned suggestions ----------
    if suggestions:
        qs = qs.filter(
            Q(name__in=suggestions) |
            Q(requirements__in=suggestions) |
            Q(location__in=suggestions)
        )

    # ---------- ORM Fallback ----------
    elif q:
        qs = qs.filter(
            Q(name__icontains=q) |
            Q(requirements__icontains=q) |
            Q(location__icontains=q)
        )

    qs = qs.order_by("-created_at")

    # ---------- Pagination ----------
    paginator = StandardResultsSetPagination()
    paginator.page_size = page_size
    page = paginator.paginate_queryset(qs, request)

    # ---------- Check unlocked ----------
    unlocked_ids = set()
    if request.user.is_authenticated:
        unlocked_ids = set(
            UserLeadAccess.objects.filter(
                user=request.user,
                lead__in=page
            ).values_list("lead_id", flat=True)
        )

    # ---------- Serialize Based On Unlock ----------
    data = []

    for lead in page:
        if lead.id in unlocked_ids:
            serializer = LeadPrivateSerializer(lead)
        else:
            serializer = LeadPublicSerializer(lead)

        serialized = serializer.data
        serialized["is_unlocked"] = lead.id in unlocked_ids
        data.append(serialized)

    return paginator.get_paginated_response(data)

@api_view(['GET'])
def leads_by_slug(request, slug):
    leads = Lead.objects.filter(slug=slug).order_by("-created_at")

    unlocked_ids = set()

    if request.user.is_authenticated:
        unlocked_ids = set(
            UserLeadAccess.objects.filter(
                user=request.user,
                lead__in=leads
            ).values_list("lead_id", flat=True)
        )

    data = []

    for lead in leads:
        if lead.id in unlocked_ids:
            serializer = LeadPrivateSerializer(lead)
        else:
            serializer = LeadPublicSerializer(lead)

        serialized = serializer.data
        serialized["is_unlocked"] = lead.id in unlocked_ids
        data.append(serialized)

    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlock_lead(request, lead_id):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)

    if profile.weekly_lead_limit == 0:
        return Response(
            {"detail": "Lead access not allowed by admin"},
            status=403
        )

    lead = get_object_or_404(Lead, id=lead_id)

    # Already unlocked
    if UserLeadAccess.objects.filter(user=user, lead=lead).exists():
        serializer = LeadPrivateSerializer(lead)
        return Response(serializer.data)

    used = weekly_lead_count(user)
    if used >= profile.weekly_lead_limit:
        return Response(
            {"detail": "Weekly lead limit exceeded"},
            status=403
        )
 
    UserLeadAccess.objects.create(user=user, lead=lead)

    serializer = LeadPrivateSerializer(lead)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unlocked_leads(request):
    leads = Lead.objects.filter(
        userleadaccess__user=request.user
    ).order_by('-userleadaccess__accessed_at')

    serializer = LeadPrivateSerializer(leads, many=True)
    return Response(serializer.data)
