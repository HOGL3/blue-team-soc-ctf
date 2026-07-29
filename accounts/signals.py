from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, employee_id=f"EMP-{instance.pk}")
    else:
        # Check if profile exists, as superusers might not have it created yet if they were made before the signal
        if hasattr(instance, "profile"):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance, employee_id=f"EMP-{instance.pk}")
