
from django.db import models
from django.contrib.auth.models import User
from leads.models import Lead

class UserDecryptedLead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    decrypted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lead')
 