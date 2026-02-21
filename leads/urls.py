from django.urls import path
from .views import lead_search, unlock_lead, unlocked_leads

urlpatterns = [
    path('search/', lead_search),
    path('unlock/<int:lead_id>/', unlock_lead),
    path('unlocked/', unlocked_leads),
]