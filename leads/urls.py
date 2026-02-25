from django.urls import path
from .views import lead_search, unlock_lead, unlocked_leads, leads_by_slug

urlpatterns = [
    path('search/', lead_search),
    path("leads/group/<slug:slug>/", leads_by_slug),
    path('unlock/<int:lead_id>/', unlock_lead),
    path('unlocked/', unlocked_leads),
]