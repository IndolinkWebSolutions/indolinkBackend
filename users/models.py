# users/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    LEAD_ACCESS_CHOICES = (
        (0, 'No Access'),
        (2, '2 Leads per Week'),
        (4, '4 Leads per Week'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)

    weekly_lead_limit = models.PositiveIntegerField(
        choices=LEAD_ACCESS_CHOICES,
        default=0   # 👈 signup ke time ZERO
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


