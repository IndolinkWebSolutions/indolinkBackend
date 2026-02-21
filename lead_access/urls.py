from django.urls import path
from .views import decrypt_lead   # 👈 THIS WAS MISSING

urlpatterns = [
    path('decrypt/<int:lead_id>/', decrypt_lead, name='decrypt-lead'),
]
