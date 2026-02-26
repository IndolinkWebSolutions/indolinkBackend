from django.urls import path
from .views import lead_search, unlock_lead, leads_history, leads_by_slug

urlpatterns = [
    path('search/', lead_search),
    path("group/<slug:slug>/", leads_by_slug),
    path('unlock/<int:lead_id>/', unlock_lead),
    path('history/', leads_history),
]