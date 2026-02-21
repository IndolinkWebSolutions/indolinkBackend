# products/urls.py
from django.urls import path
from .views import category_detail, product_search, product_detail, categories_listing
urlpatterns = [
    path('categories/<slug:slug>/', category_detail),
    path('search/', product_search),
    path('products/<slug:slug>/', product_detail),
    path("categories/", categories_listing)


] 
 