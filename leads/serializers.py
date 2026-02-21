from rest_framework import serializers
from .models import Lead


# -------------------------
# Masking Helper Functions
# -------------------------

def mask_mobile(mobile):
    if not mobile or len(mobile) < 4:
        return "****"
    return f"{mobile[:2]}{'*' * (len(mobile) - 4)}{mobile[-2:]}"


def mask_email(email):
    if not email or "@" not in email:
        return "****"
    
    name, domain = email.split("@")
    
    if len(name) <= 1:
        masked_name = "*"
    else:
        masked_name = name[0] + "***"
    
    return f"{masked_name}@{domain}"


def mask_text(text):
    if not text:
        return None
    return text[0] + "*" * (len(text) - 1)


# -------------------------
# Public Serializer (Masked)
# -------------------------

class LeadPublicSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    mobile_number = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = [
            'id',
            'name',          # ✅ visible
            'requirements',  # ✅ visible
            'location',      # 🔒 masked
            'company',       # 🔒 masked
            'email',         # 🔒 masked
            'mobile_number', # 🔒 masked
            'created_at'
        ]

    def get_location(self, obj):
        return mask_text(obj.location)

    def get_company(self, obj):
        return mask_text(obj.company)

    def get_email(self, obj):
        return mask_email(obj.email)

    def get_mobile_number(self, obj):
        return mask_mobile(obj.mobile_number)


# -------------------------
# Private Serializer (Unlocked)
# -------------------------

class LeadPrivateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'requirements',
            'location',
            'company',
            'email',
            'mobile_number',
            'created_at'
        ]