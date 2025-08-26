from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from .models import Property

# View-level caching for 15 minutes
@cache_page(60 * 15)
def property_list(request):
    # Low-level caching: cache queryset for 5 minutes
    properties = cache.get('all_properties')

    if not properties:
        print("Cache miss - querying database")
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, timeout=60*5)
    else:
        print("Cache hit")

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
