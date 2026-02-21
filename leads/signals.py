from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from .tasks import update_lead_suggestions


@receiver(post_save, sender=Lead)
def lead_saved(sender, instance, **kwargs):
    update_lead_suggestions.delay()
