from elasticsearch_dsl import Document, Text, Keyword, Date, Object
from .models import Product


class ProductDocument(Document):

    subcategory = Object(
        properties={
            "title": Text(),
            "slug": Keyword(),
            "category": Object(
                properties={
                    "name": Text(),
                    "slug": Keyword()
                }
            )
        }
    )

    name = Text()
    created_at = Date()

    class Index:
        name = "products"

    class Django:
        model = Product
        fields = ["id"]
