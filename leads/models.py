from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
 

class Lead(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, blank=True)
    requirements = models.CharField(max_length=30)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['requirements']),
            models.Index(fields=['location']),
            models.Index(fields=['created_at']),

        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.requirements)   # 👈 group by requirement
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.mobile_number}"

class UserLeadAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    accessed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lead')