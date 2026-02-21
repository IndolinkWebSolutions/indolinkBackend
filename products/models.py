from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    

class SubCategory(models.Model):
    category = models.ForeignKey(
        Category,
        related_name="subcategories",
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    image = models.ImageField(
        upload_to="subcategories/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('category', 'slug')

    def __str__(self):
        return self.title
    

 

class Product(models.Model):
    subcategory = models.ForeignKey(
        SubCategory,
        related_name='products',
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    product = models.OneToOneField(
        Product,
        related_name='details',
        on_delete=models.CASCADE
    )

    full_description = models.TextField()
    specifications = models.JSONField(blank=True, null=True)
    features = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Details of {self.product.name}"
