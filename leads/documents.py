from django_elasticsearch_dsl import Document, Index, fields
from .models import Lead

# Define Elasticsearch index
lead_index = Index('leads')

# Index settings
lead_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@lead_index.document
class LeadDocument(Document):
    # Fields to index
    name = fields.TextField(
        fields={'suggest': fields.CompletionField()}
    )
    requirements = fields.TextField()
    location = fields.TextField()
    company = fields.TextField()
    created_at = fields.DateField()

    class Django:
        model = Lead
        fields = ['email', 'mobile_number']
