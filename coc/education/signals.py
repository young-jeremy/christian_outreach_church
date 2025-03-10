from django.core.cache import cache
from django.db.models.aggregates import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import ResourceReview


@receiver(post_save, sender=ResourceReview)
def update_resource_ratings(sender, instance, **kwargs):
    """Update average ratings when a review is saved or updated"""
    resource = instance.resource
    reviews = ResourceReview.objects.filter(
        resource=resource,
        is_approved=True
    )

    # Calculate averages
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    avg_accuracy = reviews.aggregate(Avg('theological_accuracy'))['theological_accuracy__avg'] or 0
    avg_clarity = reviews.aggregate(Avg('clarity'))['clarity__avg'] or 0
    avg_practicality = reviews.aggregate(Avg('practicality'))['practicality__avg'] or 0

    # Cache the results
    cache_key = f'resource_ratings_{resource.id}'
    cache_data = {
        'avg_rating': round(avg_rating, 1),
        'avg_accuracy': round(avg_accuracy, 1),
        'avg_clarity': round(avg_clarity, 1),
        'avg_practicality': round(avg_practicality, 1),
        'review_count': reviews.count()
    }
    cache.set(cache_key, cache_data, timeout=86400)  # Cache for 24 hours


@receiver(post_delete, sender=ResourceReview)
def clear_resource_ratings_cache(sender, instance, **kwargs):
    """Clear ratings cache when a review is deleted"""
    cache_key = f'resource_ratings_{instance.resource.id}'
    cache.delete(cache_key)
