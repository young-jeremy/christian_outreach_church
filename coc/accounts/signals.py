from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import *
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Generate username from email if not set
        if not instance.username and instance.email:
            base_username = instance.email.split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            instance.username = username
            instance.save()

        # Create profile
        UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update profile when user is updated"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
