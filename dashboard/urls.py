from django.urls import path
from .views import dashboard, CompanyProfileAPIView, LogoutView, ClientProductView

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('company-profile/', CompanyProfileAPIView.as_view(), name='company-profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('addproducts/', ClientProductView.as_view())
]
