from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile

# Create your models here.
class CompanyProfile(models.Model):
    name= models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    address = models.TextField()
    company_logo = models.ImageField(upload_to='companiesLogo/', blank=True)
    company_gst = models.CharField(max_length=15, blank=True)
    company_iec = models.CharField(max_length=10, blank=True)
    business_type= models.CharField(max_length=50)

class ClientProducts(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    products_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return f"{self.user_profile.name}-{self.products_name}"
