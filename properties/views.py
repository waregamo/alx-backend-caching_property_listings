from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

# View-level caching for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    # Fetch properties using low-level caching
    properties = get_all_properties()

    # Convert queryset to list of dicts for JSON response
    properties_data = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "price": float(p.price),
            "location": p.location,
            "created_at": p.created_at.isoformat(),
        }
        for p in properties
    ]

    return JsonResponse({"properties": properties_data})

