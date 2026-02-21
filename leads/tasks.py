from celery import shared_task
from django_redis import get_redis_connection
from .models import Lead


@shared_task
def update_lead_suggestions():
    redis = get_redis_connection("default")
    key = "lead:suggestions"
    redis.delete(key)

    for lead in Lead.objects.all():
        values = [
            lead.name,
            lead.requirements,
            lead.location,
            lead.company,
        ]

        for value in values:
            if value:
                redis.sadd(key, value.lower())
