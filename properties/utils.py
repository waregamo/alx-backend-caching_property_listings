from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger(__name__)

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


def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    # Get raw Redis client from django-redis
    client = cache.client.get_client()
    info = client.info('stats')  # Redis INFO stats

    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    hit_ratio = hits / total if total > 0 else 0.0

    metrics = {
        'keyspace_hits': hits,
        'keyspace_misses': misses,
        'hit_ratio': hit_ratio
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    print(f"Redis Cache Metrics: {metrics}")

    return metrics

