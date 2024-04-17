from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
        '''
        when ever a user is created, a profile is created
        in the database for that user
        '''
        if created:
            profile = Profile.objects.create(user=instance)
