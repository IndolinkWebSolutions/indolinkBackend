from rest_framework import serializers
from .models import Contact, HomePagePopUp
class ContactSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Contact
        fields = '__all__'

class HomePopUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePagePopUp
        fields = '__all__'