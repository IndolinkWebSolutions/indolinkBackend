from rest_framework import serializers
from .models import CompanyProfile, ClientProducts
from users.models import UserProfile


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields ="__all__"
        read_only_fields = ('user')

# class ClientProductsSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ClientProducts
#         fields = ["id", "pname", "category", "description"]

#     def create(self, validated_data):
#         request = self.context["request"]
#         user_profile = UserProfile.objects.get(user=request.user)

#         return ClientProducts.objects.create(
#             user_profile = user_profile,
#             **validated_data
#         )

class ClientProductsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientProducts
        fields = ["id", "products_name", "category", "description"]

    def create(self, validated_data):
        user = self.context["request"].user   # direct user le lo
        user_profile = UserProfile.objects.get(user=user)

        validated_data["user_profile"] = user_profile
        return super().create(validated_data)
