from datetime import timedelta
from django.utils.timezone import now
from .models import UserLeadAccess


def weekly_lead_count(user):
    start_week = now() - timedelta(days=7)
    return UserLeadAccess.objects.filter(
        user=user,
        accessed_at__gte=start_week
    ).count()
