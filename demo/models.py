from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


# from django.contrib.auth import get_user_model



class Service(models.Model):
    CATEGORY_CHOICES = [
        ('Babysitting', 'Babysitting'),
        ('Gardening', 'Gardening'),
        ('Tutoring', 'Tutoring'),
        ('Other', 'Other'),
    ]
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_posted")  # Request creator
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_accepted", null=True, blank=True)  # User fulfilling the request
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=10)  # Credits for the task
    is_completed = models.BooleanField(default=False)  # Whether the task is marked as complete
    is_approved = models.BooleanField(default=False)  # Approval status by the requester
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=[('open', 'Open'), ('completed', 'Completed')], default='open', max_length=10)


    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    name = models.CharField(max_length=255, default='Unnamed Service')
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    # created_at = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(auto_now=True)
    # is_approved = models.BooleanField(default=False) 
    location = models.CharField(max_length=255, blank=True, null=True)  # Add location field

    
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services_created')

    
    category = models.CharField(max_length=100, default='General')
    hours_offered = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='services_images/', null=True, blank=True)
    # image = models.ImageField(upload_to='services_images/')

    accepted = models.BooleanField(default=False)  # New field to track if the service is accepted

    def __str__(self):
        # return self.title
        return f"{self.title} - {self.user.username}"
   
    class Meta:
        ordering = ['-created_at']


class ServiceRequest(models.Model):
    CATEGORY_CHOICES = [
        ('Babysitting', 'Babysitting'),
        ('Gardening', 'Gardening'),
        ('Tutoring', 'Tutoring'),
        ('Other', 'Other'),
    ]
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_requests")  # Requester

    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests_fulfilled", null=True, blank=True)
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # Credits for the task
    is_approved = models.BooleanField(default=False)
    # created_at = models.DateTimeField(default=now)

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    hours_requested = models.DecimalField(max_digits=5, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)  # Ensure this field exists
    is_completed = models.BooleanField(default=False)
    credit_requested = models.BooleanField(default=False)  # New field: whether worker requested credit
    
    created_at = models.DateTimeField(auto_now_add=True)

    work_completed = models.BooleanField(default=False)

    # accepted_by = models.ForeignKey(User, related_name='accepted_requests', on_delete=models.SET_NULL, null=True, blank=True)
    accepted_by = models.ForeignKey(User, related_name='accepted_service_requests', on_delete=models.SET_NULL, null=True, blank=True)
    


    def __str__(self):
        # return self.title
        # return f"{self.user.username} requests {self.credit_amount} TimeCredits from {self.provider.username}"
        return f"{self.user.username} requested {self.credit_amount} credits from {self.accepted_by.username if self.accepted_by else 'No One'}"



class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.action} at {self.timestamp}"


# class TimeCredit(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)

#     hours_available = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Number of hours available for logging
    
    
    
#     def __str__(self):
        # return f"{self.user.username} - {self.balance} credits for {self.service.title if self.service else 'No service'}"

# class TimeCredit(models.Model):
#     giver = models.ForeignKey(User, related_name="given_credits", on_delete=models.CASCADE,default=1)
#     receiver = models.ForeignKey(User, related_name="received_credits", on_delete=models.CASCADE,default=1)
#     amount = models.DecimalField(max_digits=5, decimal_places=2 ,default=0)  # Credits can be fractional
#     created_at = models.DateTimeField(auto_now_add=True )
#     description = models.TextField(null=True, blank=True)  # Optional description

#     def __str__(self):
#         return f"{self.giver.username} gave {self.amount} credits to {self.receiver.username}."


class TimeCredit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,unique=True)
    # balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('2.00'))

    def save(self, *args, **kwargs):
        if not self.user:
            raise ValueError("TimeCredit must be linked to a valid user.")
        if self._state.adding and self.balance == Decimal('0.00'):
            self.balance = Decimal('2.00')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.username} - {self.balance} credits"


# def create_time_credit(sender, instance, created, **kwargs):
#     if created:
#         TimeCredit.objects.create(user=instance, balance=Decimal('2.00'))  # ✅ Start with 2 credits

# @receiver(post_save, sender=User)
# def save_time_credit(sender, instance, **kwargs):
#     instance.timecredit.save()

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     time_credits = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
#     bio = models.TextField(blank=True)


#     def __str__(self):
#         return f"{self.user.username} profile"




class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transactions",default=None)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transactions",default=None)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    date = models.DateTimeField(auto_now_add=True)
    service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)  



    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.hours} hours"
    

# class Transaction(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_transactions")
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_transactions")
#     service = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
#     hours = models.DecimalField(max_digits=5, decimal_places=2)
#     date = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.sender.username} → {self.receiver.username}: {self.hours} hours"


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
    

# class Notification(models.Model):
#     recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
        # return f"Notification for {self.recipient.username}"
    
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.recipient.username}: {'Read' if self.is_read else 'Unread'}"


    
class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Location'
    
class ServiceLog(models.Model):
    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE,null=True, blank=True)
    provider = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    credits_earned = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Service Log - {self.provider.username}: {self.status}"
# class ServiceLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     service_type = models.CharField(max_length=255)
#     duration = models.DecimalField(max_digits=5, decimal_places=2)  # Duration in hours
#     service_date = models.DateField()
#     credits_earned = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # Credits earned after service completion

#     def save(self, *args, **kwargs):
#         # Calculate credits based on service duration
#         self.credits_earned = self.duration  # 1 hour = 1 credit
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} - {self.service_type} - {self.duration} hours"
    

# class ServiceLog(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs', null=True, blank=True, default=None)
#     request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='service_logs',null=True, blank=True, default=None)
#     duration = models.DecimalField(max_digits=5, decimal_places=2)
#     service_date = models.DateField()
#     credits_earned = models.DecimalField(max_digits=5, decimal_places=2, default=0)
#     status = models.CharField(
#         choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
#         default='pending',
#         max_length=10
#     )
#     service_type = models.CharField(max_length=255)  # Add this field

#     def save(self, *args, **kwargs):
#         # Calculate credits based on service duration
#         self.credits_earned = self.duration  # 1 hour = 1 credit
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.username} - {self.service_type} - {self.duration} hours"