# In your app's signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from demo.models import TimeCredit

@receiver(post_save, sender=User)
def create_user_time_credit(sender, instance, created, **kwargs):
    if created:
        # Create TimeCredit for the new user
        TimeCredit.objects.create(user=instance, balance=0.00)

