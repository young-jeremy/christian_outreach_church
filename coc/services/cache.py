from django.core.cache import cache


def set_cache(key, value, timeout=300):  # 5 minutes default timeout
    """Set a value in Redis cache"""
    cache.set(key, value, timeout=timeout)


def get_cache(key):
    """Get a value from Redis cache"""
    return cache.get(key)


def delete_cache(key):
    """Delete a value from Redis cache"""
    cache.delete(key)


def clear_cache():
    """Clear all cache"""
    cache.clear()
