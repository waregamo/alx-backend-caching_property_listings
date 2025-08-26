from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Fetch all Property objects, using Redis low-level caching for 1 hour.
    """
    properties = cache.get('all_properties')

    if not properties:
        print("Cache miss - querying database")
        properties = list(Property.objects.all())
        cache.set('all_properties', properties, timeout=3600)  # cache for 1 hour
    else:
        print("Cache hit")

    return properties
