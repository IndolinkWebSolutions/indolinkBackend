from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Product
from .serializers import CategoryDetailSerializer
from core.pagination import StandardResultsSetPagination
from core.encryption import encrypt
from .documents import ProductDocument
from django.db.models import Q as DJ_Q
from core.autocomplete import autocomplete
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductMiniSerializer
from core.autocomplete import autocomplete 


 
@api_view(['GET'])
def category_detail(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related(
            'subcategories__products'
        ),
        slug=slug,
        is_active=True
    )

    serializer = CategoryDetailSerializer(category, context={"request":request})
    return Response(serializer.data)

 
 # adjust path if needed


@api_view(['GET'])
def product_search(request):
    q = request.GET.get("q", "").strip().lower()
    subcategory = request.GET.get("subcategory")

    qs = Product.objects.select_related(
        "subcategory__category"
    ).filter(is_active=True)

    names = []

    # -------- Redis Safe Block --------
    if q:
        try:
            names = autocomplete("product_autocomplete", q, limit=10)
        except Exception as e:
            print("Redis not working, fallback to DB search:", e)
            names = []

    # -------- If Redis returns results --------
    if names:
        qs = qs.filter(name__in=names)

    # -------- Fallback ORM Search --------
    elif q:
        qs = qs.filter(name__icontains=q)

    # -------- Subcategory filter --------
    if subcategory:
        qs = qs.filter(subcategory__slug=subcategory)

    qs = qs.order_by("name")[:10]

    serializer = ProductMiniSerializer(
        qs,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)
                

from .models import Product
from .serializers import ProductDetailSerializer

@api_view(['GET'])
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('subcategory')
                       .prefetch_related('details'),
        slug=slug,
        is_active=True
    )

    serializer = ProductDetailSerializer(product, context = {"request":request})
    return Response(serializer.data)



@api_view(["GET"])
def categories_listing(request):
    categories = Category.objects.filter(
        is_active=True
    ).order_by("created_at").prefetch_related(
        "subcategories__products"
    )

    response = []

    for category in categories:
        response.append({
            "name": category.name,
            "slug": category.slug,
            "image": request.build_absolute_uri(category.image.url)
                     if category.image else None,
            "subcategories": [
                {
                    "title": sub.title,
                    "slug": sub.slug,
                    "image": request.build_absolute_uri(sub.image.url)
                             if sub.image else None,
                    "products": [
                        {
                            "name": p.name,
                            "slug": p.slug
                        }
                        for p in sub.products.filter(is_active=True)
                    ]
                }
                for sub in category.subcategories.filter(is_active=True)
            ]
        })

    return Response(response)
