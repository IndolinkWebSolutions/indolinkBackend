from core.autocomplete import autocomplete
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def leads_autocomplete(request):
    q= request.GET.get("q", "").strip().lower()
    suggestion = autocomplete("lead_autocompleted", q, limit=10)
    return Response(suggestion)
 