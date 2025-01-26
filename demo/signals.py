# In your app's signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from demo.models import TimeCredit
# from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_time_credit(sender, instance, created, **kwargs):
    if created:
        # Create TimeCredit for the new user
        TimeCredit.objects.create(user=instance, balance=0.00)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()



