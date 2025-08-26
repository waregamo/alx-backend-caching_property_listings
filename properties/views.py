from django.http import HttpResponse
from django.core.cache import cache
from .models import Property

def property_list(request):
    # Low-level caching: cache query result
    properties = cache.get('all_properties')

    if not properties:
        print("Cache miss - querying database")
        # Query the database only if cache is empty
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, timeout=60*5)  # cache for 5 minutes
    else:
        print("Cache hit")

    response_text = "\n".join([f"{p.title} - ${p.price}" for p in properties])
    if not response_text:
        response_text = "No properties found."

    return HttpResponse(response_text, content_type="text/plain")
