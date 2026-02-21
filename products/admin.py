from django.contrib import admin
from .models import Category, SubCategory, Product, ProductDetail

# ========================
# Inline Admins
# ========================

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    fields = ('title', 'slug', 'image', 'is_active')
    prepopulated_fields = {"slug": ("title",)}


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ('name', 'slug', 'image', 'is_active')
    prepopulated_fields = {"slug": ("name",)}


# ========================
# Main Admins
# ========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'slug', 'category__name')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'subcategory', 'slug', 'is_active', 'created_at', 'updated_at')
    list_filter = ('subcategory', 'is_active')
    search_fields = ('name', 'slug', 'subcategory__title')
    prepopulated_fields = {"slug": ("name",)}
    # Show product details inline if exists
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ('product', 'created_at')
    search_fields = ('product__name',)
