from django.urls import path
from .views import ContactAPIView, HomePagePopUpAPIView 

urlpatterns = [
    path("contact/", ContactAPIView.as_view(), name="contact"),
    path('home-enquiry/', HomePagePopUpAPIView.as_view(), name='pop-up-enquiries' )
]
