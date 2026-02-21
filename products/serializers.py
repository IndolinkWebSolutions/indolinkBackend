from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductDetail


# ---------------------------
# Mini Product Serializer (For Search / Lists)
# ---------------------------
class ProductMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug']   # 👈 id added


# ---------------------------
# SubCategory Serializer
# ---------------------------
class SubCategorySerializer(serializers.ModelSerializer):
    products = ProductMiniSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = SubCategory
        fields = ['title', 'slug', 'image', 'products']

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ---------------------------
# Category Detail Serializer
# ---------------------------
class CategoryDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'image', 'subcategories']

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ---------------------------
# Product Detail Serializer
# ---------------------------
class ProductDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'image',
            'description',
            'details'
        ]

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


# ---------------------------
# Extra Product Detail Serializer
# ---------------------------
class ProductExtraDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductDetail
        fields = ['full_description', 'specifications', 'features']