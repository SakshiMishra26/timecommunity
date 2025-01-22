from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone

from django.contrib.auth import get_user_model



class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Babysitting', 'Babysitting'),
        ('Gardening', 'Gardening'),
        ('Tutoring', 'Tutoring'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    name = models.CharField(max_length=255, default='Unnamed Service')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False) 
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_created')

    
    category = models.CharField(max_length=100, default='General')
    hours_offered = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='services_images/', null=True, blank=True)
    # image = models.ImageField(upload_to='services_images/')

    accepted = models.BooleanField(default=False)  # New field to track if the service is accepted

    def __str__(self):
        return self.title
    # service = models.ForeignKey('Service', on_delete=models.CASCADE)
    # shours_available = models.IntegerField()
    class Meta:
        ordering = ['-created_at']


class ServiceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('Babysitting', 'Babysitting'),
        ('Gardening', 'Gardening'),
        ('Tutoring', 'Tutoring'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    hours_requested = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    accepted_by = models.ForeignKey(User, related_name='accepted_requests', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp}"


class TimeCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

    hours_available = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Number of hours available for logging
    
    
    
    def __str__(self):
        return f"{self.user.username} - {self.balance} credits for {self.service.title if self.service else 'No service'}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.hours} hours"

class TimeTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('Earned', 'Earned'),
        ('Spent', 'Spent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.hours} hours"


class Booking(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=255, default='pending')


    def __str__(self):
        return f"{self.service.title} booked by {self.user.username} on {self.date} at {self.time}"

class Review(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])  # Rating system from 1 to 5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.service.name}"
    

class Request(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title