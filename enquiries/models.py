from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(50)
    email = models.EmailField(100)
    phoneNo = models.CharField(max_length=15)
    msg = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.phoneNo

class HomePagePopUp(models.Model):
    company_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phoneNo = models.CharField(max_length=15)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name