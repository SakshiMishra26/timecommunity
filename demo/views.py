from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TimeTransactionForm,LogHoursForm,ServiceForm,BookingForm,ReviewForm
from .models import Service, TimeCredit,TimeTransaction,Booking,Review,UserActivity,Notification
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from .models import ServiceRequest,Transaction,Request
from .forms import ServiceRequestForm
from django.conf import settings



# @login_required
# def give_time_credit(request, worker_id):
#     # Fetch the worker user (the one who did the work)
#     worker = get_object_or_404(User, id=worker_id)

#     # Fetch the user who is giving the credit (the logged-in user)
#     giver = request.user
#     giver_profile = giver.userprofile

#     if request.method == 'POST':
#         form = TimeCreditForm(request.POST)
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             description = form.cleaned_data['description']

#             # Check if giver has enough time credits
#             if giver_profile.time_credits >= amount:
#                 # Deduct credits from the giver
#                 giver_profile.time_credits -= amount
#                 giver_profile.save()

#                 # Add credits to the receiver (worker)
#                 receiver_profile = worker.userprofile
#                 receiver_profile.time_credits += amount
#                 receiver_profile.save()

#                 # Record the transaction
#                 transaction = TimeCredit.objects.create(
#                     giver=giver,
#                     receiver=worker,
#                     amount=amount,
#                     description=description
#                 )

#                 return redirect('dashboard')  # Redirect to the dashboard or another page
#             else:
#                 return HttpResponse("You do not have enough time credits.", status=400)

#     else:
#         form = TimeCreditForm()

#     return render(request, 'give_time_credit.html', {'form': form, 'worker': worker})





def about_us(request):
    return render(request, 'about_us.html')



def home(request):
    # services = Service.objects.all() 
    services = Service.objects.filter(is_approved=True)[:4]
    # pending_services = Service.objects.filter(is_approved=False)
    # approved_services = Service.objects.filter(is_approved=True)  # To be used elsewhere on the page if needed

  
    service_requests = ServiceRequest.objects.all()[:4]  # Fetch all service requests
    return render(request, 'home.html', {
        'services': services,
        'service_requests': service_requests
    })



def index(request):
    return render(request, 'index.html')

# def register(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home.html')
#     else:
#         form = RegisterForm()
#     return render(request, 'register.html', {'form': form})

from django.contrib.auth.models import User
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')

            # ✅ Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered. Please use a different one.")
                return render(request, 'register.html', {'form': form})

            # ✅ Check if the username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken. Please choose another one.")
                return render(request, 'register.html', {'form': form})

            # ✅ Create user
            user = form.save()

            # ✅ Ensure TimeCredit is created for the user
            time_credit, created = TimeCredit.objects.get_or_create(user=user, defaults={'balance': Decimal('2.00')})
            if created:
                time_credit.save()

            # ✅ Authenticate and log in the user
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # ✅ Send welcome notification
            Notification.objects.create(
                recipient=user,
                message="Welcome to Time Credit! You have received 2 free credits to start."
            )

            # ✅ Send welcome email
            send_mail(
                "Welcome to Time Credit",
                f"Hello {user.username},\n\nYou have successfully registered and received 2 time credits to start.",
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "Registration successful! You received 2 free credits.")
            return redirect('dashboard')  # ✅ Redirect to dashboard
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    # user = request.user

    # profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')






from .models import ServiceLog
from django.db import models  

# @login_required
# def dashboard(request):
#     user = request.user

    
#     try:
        
#         time_credit, _ = TimeCredit.objects.get_or_create(user=user)

#     except TimeCredit.DoesNotExist:
#         time_credit = None

    
#     accepted_requests = ServiceRequest.objects.filter(accepted=True, accepted_by=user)

#     pending_credit_requests = ServiceRequest.objects.filter(user=user, credit_requested=True, is_approved=False)
#     completed_services = ServiceRequest.objects.filter(accepted_by=user, is_completed=True, credit_requested=False)

#     transactions = Transaction.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('-date')

#     service_logs = ServiceLog.objects.filter(request__user=request.user)

#     request_list = ServiceRequest.objects.filter(user=user)

#     services = Service.objects.filter(user=user)
#     unread_notifications = user.notifications.filter(is_read=False)


   

#     return render(request, 'dashboard.html', {
#         'user': user,
#         'time_credit': time_credit,
#         'request_list': request_list,

#         'transactions': transactions,
#         'services': services,
#         'accepted_requests': accepted_requests, 
#         'unread_notifications': unread_notifications,
#         'service_logs': service_logs,
#         'pending_credit_requests': pending_credit_requests,
#         'completed_services': completed_services,

 
#     })
@login_required
def dashboard(request):
    user = request.user

    # ✅ Ensure the user has a TimeCredit account (Starts with 2 credits if new)
    time_credit, created = TimeCredit.objects.get_or_create(user=user, defaults={'balance': Decimal('2.00')})

    # ✅ If the user was created before this feature, update balance if it's missing
    if created or time_credit.balance is None:
        time_credit.balance = Decimal('2.00')
        time_credit.save()

    # ✅ Fetch all necessary data for the dashboard
    accepted_requests = ServiceRequest.objects.filter(accepted=True, accepted_by=user)
    pending_credit_requests = ServiceRequest.objects.filter(user=user, credit_requested=True, is_approved=False)
    completed_services = ServiceRequest.objects.filter(accepted_by=user, is_completed=True, credit_requested=False)
    transactions = Transaction.objects.filter(models.Q(sender=user) | models.Q(receiver=user)).order_by('-date')
    service_logs = ServiceLog.objects.filter(request__user=request.user)
    request_list = ServiceRequest.objects.filter(user=user)
    services = Service.objects.filter(user=user)
    unread_notifications = Notification.objects.filter(recipient=user, is_read=False)

    # ✅ Pass data to the dashboard template
    return render(request, 'dashboard.html', {
        'user': user,
        'time_credit': time_credit,  # ✅ Ensure balance is displayed
        'request_list': request_list,
        'transactions': transactions,
        'services': services,
        'accepted_requests': accepted_requests, 
        'unread_notifications': unread_notifications,
        'service_logs': service_logs,
        'pending_credit_requests': pending_credit_requests,
        'completed_services': completed_services,
    })

@login_required
def request_time_credit(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    # Ensure only the worker can request credit
    if service_request.accepted_by != request.user:
        messages.error(request, "You can only request time credits for services you completed.")
        return redirect('dashboard')

    if service_request.credit_requested:
        messages.warning(request, "You have already requested time credits for this service.")
        return redirect('dashboard')

    # Mark the request as "credit requested"
    service_request.credit_requested = True
    service_request.save()

    # Notify the requester
    Notification.objects.create(
        recipient=service_request.user,
        message=f"{request.user.username} has requested {service_request.credit_amount} time credits for completing '{service_request.title}'."
    )

    # Send email notification
    send_mail(
        "Time Credit Request",
        f"Hello {service_request.user.username},\n\n{request.user.username} has requested {service_request.credit_amount} time credits for completing '{service_request.title}'. Please approve it from your dashboard.\n\nTime Community Bank",
        settings.EMAIL_HOST_USER,
        [service_request.user.email],
        fail_silently=False,
    )

    messages.success(request, "Your time credit request has been sent.")
    return redirect('dashboard')

@login_required
def approve_time_credit(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if service_request.user != request.user:
        messages.error(request, "You can only approve credits for services you requested.")
        return redirect('dashboard')

    if not service_request.credit_requested:
        messages.warning(request, "The worker has not requested time credits for this service yet.")
        return redirect('dashboard')

    if service_request.is_approved:
        messages.warning(request, "This request has already been approved.")
        return redirect('dashboard')

    sender = request.user  # The one giving the credit
    receiver = service_request.accepted_by  # The one receiving the credit
    hours = service_request.credit_amount

    sender_credit = TimeCredit.objects.get(user=sender)
    receiver_credit = TimeCredit.objects.get(user=receiver)

    # ✅ Ensure the sender has enough balance
    if sender_credit.balance < hours:
        messages.error(request, "Insufficient balance to complete this transaction.")
        return redirect('dashboard')

    # ✅ Deduct and add credits
    sender_credit.balance -= hours
    receiver_credit.balance += hours
    sender_credit.save()
    receiver_credit.save()

    # ✅ Mark request as approved
    service_request.is_approved = True
    service_request.save()

    # ✅ Notify the receiver
    Notification.objects.create(
        recipient=receiver,
        message=f"You received {hours} time credits from {sender.username} for '{service_request.title}'."
    )

    # ✅ Send email notifications
    send_mail(
        "Time Credit Received",
        f"Hello {receiver.username},\n\nYou received {hours} time credits from {sender.username}.",
        settings.EMAIL_HOST_USER,
        [receiver.email],
        fail_silently=False,
    )

    send_mail(
        "Time Credit Sent",
        f"Hello {sender.username},\n\nYou sent {hours} time credits to {receiver.username}.",
        settings.EMAIL_HOST_USER,
        [sender.email],
        fail_silently=False,
    )

    messages.success(request, f"{hours} hours transferred to {receiver.username}.")
    return redirect('dashboard')


# @login_required
# def approve_time_credit(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    # Ensure only the original requester can approve the credit transfer
    if service_request.user != request.user:
        messages.error(request, "You can only approve credits for services you requested.")
        return redirect('dashboard')

    if not service_request.credit_requested:
        messages.warning(request, "The worker has not requested time credits for this service yet.")
        return redirect('dashboard')

    if service_request.is_approved:
        messages.warning(request, "This request has already been approved.")
        return redirect('dashboard')

    sender = request.user  # The one giving the credit
    receiver = service_request.accepted_by  # The one receiving the credit

    # ✅ Debugging - Check the stored credit amount
    print(f"Approving Credit for ServiceRequest ID: {service_request.id}")
    print(f"Stored Credit Amount Before Transfer: {service_request.credit_amount}")

    # Ensure correct decimal format
    if service_request.credit_amount is None or service_request.credit_amount <= 0:
        messages.error(request, "Invalid credit amount. Please check the request.")
        return redirect('dashboard')

    hours = Decimal(service_request.credit_amount)  # Ensure proper Decimal conversion

    sender_credit, _ = TimeCredit.objects.get_or_create(user=sender)
    receiver_credit, _ = TimeCredit.objects.get_or_create(user=receiver)

    print(f"Sender Balance Before: {sender_credit.balance}")
    print(f"Receiver Balance Before: {receiver_credit.balance}")

    if sender_credit.balance < hours:
        messages.error(request, "Insufficient balance to complete this transaction.")
        return redirect('dashboard')

    # Transfer credits
    sender_credit.balance -= hours
    receiver_credit.balance += hours
    sender_credit.save()
    receiver_credit.save()

    print(f"Sender Balance After: {sender_credit.balance}")
    print(f"Receiver Balance After: {receiver_credit.balance}")

    # Create Transaction Record
    Transaction.objects.create(sender=sender, receiver=receiver, service=service_request, hours=hours)

    # Mark request as approved
    service_request.is_approved = True
    service_request.save()

    # Notify the worker
    Notification.objects.create(
        recipient=receiver,
        message=f"You have received {hours} hours from {sender.username} for '{service_request.title}'."
    )

    # Send email notifications
    send_mail(
        "Time Credit Received",
        f"Hello {receiver.username},\n\nYou have received {hours} hours from {sender.username} for completing '{service_request.title}'.",
        settings.EMAIL_HOST_USER,
        [receiver.email],
        fail_silently=False,
    )

    send_mail(
        "Time Credit Sent",
        f"Hello {sender.username},\n\nYou have successfully transferred {hours} hours to {receiver.username} for completing '{service_request.title}'.",
        settings.EMAIL_HOST_USER,
        [sender.email],
        fail_silently=False,
    )

    messages.success(request, f"{hours} hours transferred to {receiver.username}.")
    return redirect('dashboard')





@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('dashboard')


def manage_credits(request):
    time_credit = None  # Initialize time_credit variable
    
    if request.method == 'POST':
        form = TimeTransactionForm(request.POST)
        
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            # Try to get the user's TimeCredit object or create it if it doesn't exist
            try:
                time_credit = TimeCredit.objects.get(user=request.user)
            except TimeCredit.DoesNotExist:
                time_credit = TimeCredit.objects.create(user=request.user, balance=Decimal('0.00'))

            # Update the balance based on the transaction type
            if transaction.transaction_type == 'Earned':
                time_credit.balance += Decimal(transaction.hours)  # Ensure it's a Decimal
            elif transaction.transaction_type == 'Spent':
                time_credit.balance -= Decimal(transaction.hours)  # Ensure it's a Decimal
            time_credit.save()

            return redirect('dashboard')  # Redirect after processing the transaction

    else:
        form = TimeTransactionForm()

    return render(request, 'manage_credits.html', {'form': form, 'time_credit': time_credit})





@login_required
def log_hours(request, service_id):
    # Try to get the TimeCredit object for the current user
    try:
        time_credit = TimeCredit.objects.get(user=request.user)
    except TimeCredit.DoesNotExist:
        # If TimeCredit doesn't exist, show an error page
        return render(request, 'error.html', {'message': 'TimeCredit not found for this user.'})

    # Get the service based on service_id
    service = Service.objects.get(id=service_id)

    # Get the available hours for the user
    hours_available = time_credit.hours_available

    if request.method == 'POST':
        form = LogHoursForm(request.POST)
        if form.is_valid():
            hours_logged = form.cleaned_data['hours_worked']
            
            # Check if the user has enough hours available
            if hours_logged > hours_available:
                return render(request, 'log_hours.html', {'form': form, 'service': service, 'error': 'Not enough hours available.'})

            # Create a new transaction to log the hours worked
            Transaction.objects.create(
                user=request.user,
                service=service,
                hours=hours_logged,
                transaction_type='credit',  # Assuming this is adding time credits
            )

            # Update TimeCredit balance and available hours
            time_credit.balance += hours_logged
            time_credit.hours_available -= hours_logged
            time_credit.save()

            return redirect('dashboard')  # Redirect to the dashboard after logging hours
    else:
        form = LogHoursForm()

    # Return the log_hours template with necessary data
    return render(request, 'log_hours.html', {
        'form': form,
        'service': service,
        'time_credit': time_credit,
        'hours_available': hours_available,
    })


# Example view where you create a TimeCredit instance and associate it with a Service
def create_time_credit(request):
    service = Service.objects.get(id=1)  # Assuming you fetch a specific Service instance
    user = request.user  # Assuming user is logged in
    
    # Create TimeCredit instance with a service link
    time_credit = TimeCredit.objects.create(user=user, service=service, hours_available=10.0)
    return redirect('dashboard')


def contact_success(request):
    return render(request, 'contact_success.html') 




@login_required
def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            # Save the service but don't commit to the database yet
            service = form.save(commit=False)
            # Assign the current user to the service
            service.user = request.user
            service.save()  # Save the service

            # Log the user activity
            activity = UserActivity(user=request.user, action="Added a new service")
            activity.save()

            # Redirect to the dashboard (or another appropriate page)
            return redirect('dashboard')
    else:
        # If it's a GET request, display an empty form
        form = ServiceForm()

    # Render the form in the template
    return render(request, 'add_service.html', {'form': form})




@login_required
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if service.user != request.user:
        messages.error(request, "You are not allowed to edit this offer.")
        return redirect('service_detail', service_id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Offer updated successfully.")

            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

 
from django.shortcuts import render
from .models import Service

def service_list(request):
    # Fetching services for superusers
    if request.user.is_superuser:
        # Pending services (is_approved=False)
        pending_services = Service.objects.filter(is_approved=False)
        # Approved services (is_approved=True)
        services = Service.objects.all()
        approved_services = Service.objects.filter(is_approved=True)
    else:
        # Non-admin users will only see approved services
        approved_services = Service.objects.filter(is_approved=True)
        pending_services = []  # No pending services for non-admin users
        services = Service.objects.filter(is_approved=True)

    # Optional: Filter by category if provided
    category = request.GET.get('category')
    if category:
        approved_services = approved_services.filter(category=category)
        pending_services = pending_services.filter(category=category)
        services = services.filter(category=category)

    # Pass both pending and approved services to the template
    return render(request, 'service_list.html', {
        'pending_services': pending_services,
        'approved_services': approved_services,
        'services': services
    })




@login_required
def accept_offer(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    # Check if the current user is the one offering the service, or if the service has already been accepted
    if service.accepted:
        return render(request, 'error.html', {'message': 'This service has already been accepted.'})
    
    if service.user == request.user:
        return render(request, 'error.html', {'message': 'You cannot accept your own offer.'})

    # Mark the service as accepted
    service.accepted = True
    service.save()

    send_mail(
        'Your Offer Has Been Accepted!',
        f'Hello {service.user.username},\n\nYour offer for the service "{service.title}" has been accepted by {request.user.username}.',
        'your_email@example.com',  # Sender's email
        [service.user.email],  # Recipient's email
        fail_silently=False,
    )


    # Redirect to a page confirming the service has been accepted
    return redirect('service_detail', service_id=service.id)




@login_required
def delete_service(request, service_id):
    try:
        service = get_object_or_404(Service, id=service_id)

        # Check if the logged-in user is the owner of the offer
        if service.user != request.user:
            messages.error(request, "You are not allowed to delete this offer.")
            return redirect('service_detail', service_id=service_id)

        # If the user is the owner, allow deletion
        service.delete()
        messages.success(request, "Offer deleted successfully.")
    except Service.DoesNotExist:
        # If the service doesn't exist, redirect to service list with an error
        messages.error(request, "Service does not exist.")
    
    return redirect('service_list')



from decimal import Decimal  # Import Decimal to avoid float conversion issues

@login_required
def add_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user

            # ✅ Ensure credit_amount is correctly assigned
            if 'credit_amount' in form.cleaned_data and form.cleaned_data['credit_amount']:
                service_request.credit_amount = Decimal(form.cleaned_data['credit_amount'])
            elif 'hours_requested' in form.cleaned_data and form.cleaned_data['hours_requested']:
                service_request.credit_amount = Decimal(form.cleaned_data['hours_requested'])
            else:
                service_request.credit_amount = Decimal('0.00')

            service_request.save()

            print(f"✅ Service Request Created: {service_request}")  # Debugging
            print(f"✅ Credit Amount Stored: {service_request.credit_amount}")  # Debugging

            return redirect('dashboard')
    else:
        form = ServiceRequestForm()

    return render(request, 'add_service_request.html', {'form': form})



def request_list(request):
    service_requests = ServiceRequest.objects.all()
    category = request.GET.get('category')
    if category:
        service_requests = service_requests.filter(category=category)
    return render(request, 'request_list.html', {'service_requests': service_requests})

@login_required
def accept_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    # Prevent users from accepting their own request
    if service_request.user == request.user:
        messages.error(request, "You cannot accept your own request.")
        return redirect('request_list')

    # Check if the request has already been accepted
    if not service_request.accepted:
        service_request.accepted = True  # Mark the request as accepted
        service_request.accepted_by = request.user  # Set the user who accepted it
        service_request.save()
        messages.success(request, "Request accepted successfully.")
    else:
        messages.warning(request, "This request has already been accepted.")

    # Create a notification for the user who posted the request
    notification_message = f"Your request '{service_request.title}' has been accepted by {request.user.username}."
    Notification.objects.create(
        recipient=service_request.user,
        message=notification_message
    )
         # Send an email notification to the user
    subject = "Your Service Request Has Been Accepted"
    message = f"Hi {service_request.user.username},\n\nYour request '{service_request.title}' has been accepted by {request.user.username}. Please check your dashboard for more details.\n\nThank you for using Time Community Bank."
    recipient_email = service_request.user.email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        fail_silently=False,
    )

    messages.success(request, f"You have successfully accepted the request '{service_request.title}'.")
    return redirect('request_detail', request_id=service_request.id)




@login_required
def complete_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    
    print(f"Completing Service: {service_request}")  # Debugging

    if service_request.user != request.user:
        messages.error(request, "Only the request owner can mark this as completed.")
        return redirect('dashboard')

    if not service_request.accepted_by:
        messages.error(request, "This request has not been accepted yet.")
        return redirect('dashboard')

    if service_request.is_completed:
        messages.warning(request, "This request has already been completed.")
        return redirect('dashboard')

    # Mark request as completed
    service_request.is_completed = True
    service_request.save()

    print(f"Updated is_completed: {service_request.is_completed}")  # Debugging

    messages.success(request, "The service request has been marked as completed.")
    return redirect('dashboard')



@login_required
def accepted_requests_view(request):
    # Get requests accepted by the current user
    accepted_requests = ServiceRequest.objects.filter(accepted=True, accepted_by=request.user)
    # return render(request, 'dashboard.html', {'accepted_requests': accepted_requests})
    return render(request, 'accepted_requests.html', {'accepted_requests': accepted_requests})



import logging

logger = logging.getLogger(__name__)



@login_required
def request_detail(request, request_id):
    service_request = get_object_or_404(Request, id=request_id)

    # Check if the current user owns the request
    if request.method == 'POST':
        # Marking the request as completed
        if 'mark_completed' in request.POST and service_request.user == request.user:
            # Ensure the request has been accepted by a provider
            if not service_request.accepted_by:
                messages.error(request, "This request has not been accepted yet.")
                return redirect('request_detail', request_id=request_id)

            sender = service_request.user  # requester
            receiver = service_request.accepted_by  # service provider
            hours = service_request.hours_requested

            # Ensure the requester has enough credits
            sender_credit, _ = TimeCredit.objects.get_or_create(user=sender)
            receiver_credit, _ = TimeCredit.objects.get_or_create(user=receiver)

            if sender_credit.balance < hours:
                messages.error(request, "Insufficient balance to complete this transaction.")
                return redirect('request_detail', request_id=request_id)

            # Transfer credits
            sender_credit.balance -= hours
            receiver_credit.balance += hours
            sender_credit.save()
            receiver_credit.save()

            # Create Transaction Record
            Transaction.objects.create(sender=sender, receiver=receiver, service=service_request, hours=hours)

            # Mark the service request as completed
            service_request.is_completed = True
            service_request.save()

            # Notify the provider
            Notification.objects.create(
                recipient=receiver,
                message=f"You have received {hours} hours from {sender.username} for '{service_request.title}'."
            )

            # Send email to provider
            send_mail(
                "Service Request Completed",
                f"Hello {receiver.username},\n\nYou have received {hours} hours from {sender.username} for completing '{service_request.title}'.",
                "noreply@timecommunitybank.com",
                [receiver.email],
                fail_silently=False,
            )

            messages.success(request, f"{hours} hours transferred to {receiver.username}.")
            return redirect('request_detail', request_id=request_id)

        # Handling location update logic (if needed)
        location = request.POST.get('location')
        if location:
            service_request.location = location
            service_request.save()
            logger.info(f"Updating location for request ID {request_id}: {location}")
            return redirect('request_detail', request_id=request_id)

    return render(request, 'request_detail.html', {'request': service_request})



@login_required
def edit_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            return redirect('request_list')
    else:
        form = ServiceRequestForm(instance=service_request)
#
    # return render(request, 'edit_service_request.html', {'form': form})
    return render(request, 'edit_service_request.html', {'form': form,'service_request': service_request})

@login_required

def delete_service_request(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        service_request.delete()
        return redirect('request_list')  # Adjust this to the appropriate URL
    return render(request, 'confirm_delete.html', {'request': service_request})

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        # Send email logic here
        send_mail(
            f'Message from {name}',
            message,
            email,
            ['your_email@example.com'],  # Replace with your email
        )
        return render(request, 'contact_success.html')
    return render(request, 'contact.html')





@login_required
def book_service(request, service_id):
    # service = get_object_or_404(Service, id=service_id)
    service = Service.objects.filter(id=service_id).first()
    services = Service.objects.exclude(id=service_id)  # Get all other services excluding the deleted one
    context = {
        'services': services,
        'deleted_service_message': 'The service you requested is no longer available.'
    }
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 'Pending'
            booking.save()
            # You can add a notification mechanism here
            return redirect('booking_confirmation', booking.id)
    else:
        form = BookingForm(initial={'service': service})
    return render(request, 'book_service.html', {'form': form, 'service': service})

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def manage_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'manage_bookings.html', {'bookings': bookings})

def calendar_events(request):
    bookings = Booking.objects.filter(user=request.user)
    events = [{
        'title': booking.service.title,
        'start': f"{booking.date}T{booking.time}",
        'end': f"{booking.date}T{booking.time}",
    } for booking in bookings]
    return JsonResponse(events, safe=False)

from django.shortcuts import render

def calendar(request):
    return render(request, 'calendar.html')  # Replace with your calendar template path


def add_review(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        form.instance.user = request.user  # Set the user to the currently logged-in user
        form.instance.service = service  # Set the service for the review

        if form.is_valid():
            form.save()
            return redirect('service_detail', service_id=service.id)  # Redirect to the service detail page
    else:
        form = ReviewForm(initial={'service': service.id})

    return render(request, 'add_review.html', {'form': form, 'service': service})

# def service_detail(request, service_id):
#     service = get_object_or_404(Service, id=service_id)
#     reviews = service.reviews.all()  # Get all reviews for the service
#     return render(request, 'service_detail.html', {'service': service, 'reviews': reviews})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    reviews = Review.objects.filter(service=service)
   
    return render(request, 'service_detail.html', {'service': service, 'reviews': reviews})



# def request_detail(request, request_id):
#     print(Request.objects.all())  # Debugging line
#     request_obj = get_object_or_404(Request, request_id=request_id)
#     return render(request, 'request_detail.html', {'request': request_obj})

def request_detail(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    return render(request, 'request_detail.html', {'request': service_request})

def all_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'all_reviews.html', {'reviews': reviews})

def accept_service(request, service_id):
    # Logic to accept the service (e.g., update status, notify the user)
    # For now, redirect back to the service detail page
    return redirect('service_detail', service_id=service_id)

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)

def approve_service(request, id):
    service = get_object_or_404(Service, id=id)
    # if service.user != request.user:  
    #     service.is_approved = True
    service.is_approved = True

    service.save()
    messages.success(request, f'Service "{service.title}" has been approved.')

    return redirect('service_list')  

@user_passes_test(lambda u: u.is_superuser)
def reject_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.is_approved = False
    service.delete()
    messages.warning(request, f'Service "{service.title}" has been rejected.')

    return redirect('service_list')  # Red

def service_moderation(request):
    # Fetch the services (you can filter them based on approval status or other conditions)
    services = Service.objects.all()  # Adjust as needed
    return render(request, 'your_template.html', {'services': services})



def create_service(request):
    if request.method == 'POST':
        # Assuming you have a ServiceForm for handling service creation
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created_by = request.user
            service.save()
            return redirect('service_detail', service_id=service.id)
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})

from .forms import UserLocationForm
from .models import UserLocation



def update_location(request,request_id):
    # Check if the user already has a location
    try:
        user_location = request.user.userlocation
    except UserLocation.DoesNotExist:
        user_location = None

    # If POST request, update location
    if request.method == 'POST':
        form = UserLocationForm(request.POST)
        if form.is_valid():
            # If user does not have a location, create one
            if not user_location:
                user_location = UserLocation(user=request.user)  # Ensure user is assigned

            # Update user location fields
            user_location.city = form.cleaned_data['city']
            user_location.state = form.cleaned_data['state']
            user_location.country = form.cleaned_data['country']
            user_location.save()

            messages.success(request, "Location updated successfully!")
            return redirect('request_detail', request_id=request_id)  # Redirect to profile page or any other page
    else:
        # If GET request, use current location data (if exists) to pre-populate the form
        form = UserLocationForm(instance=user_location)

    return render(request, 'update_location.html', {'form': form})


@login_required
def profile(request):
    # Get the user's location if available
    try:
        user_location = request.user.userlocation
    except UserLocation.DoesNotExist:
        user_location = None

    return render(request, 'profile.html', {'user_location': user_location})


@login_required
def mark_as_completed(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if service_request.user != request.user:
        messages.error(request, "You can only mark tasks you are fulfilling as completed.")
        return redirect('dashboard')

    if service_request.is_completed:
        messages.warning(request, "This task is already marked as completed.")
        return redirect('dashboard')
    service_request.is_completed = True
    service_request.save()

    messages.success(request, "The service request has been marked as completed.")
    return redirect('dashboard')
        

# @login_required
# def complete_service_request(request, request_id):
#     service_request = get_object_or_404(ServiceRequest, id=request_id)

#     # Prevent unauthorized completion
#     if service_request.user != request.user:
#         messages.error(request, "Only the request owner can mark this as completed.")
#         return redirect('dashboard')

#     if service_request.is_completed:
#         messages.warning(request, "This request has already been completed.")
#         return redirect('dashboard')

#     # Mark request as completed
#     service_request.is_completed = True
#     service_request.save()

#     messages.success(request, "The service request has been marked as completed.")
#     return redirect('dashboard')


@login_required
def approve_task(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id)

    if service_request.user != request.user:
        messages.error(request, "You can only approve tasks you requested.")
        return redirect('dashboard')

    if not service_request.is_completed:
        messages.warning(request, "The task is not marked as completed yet.")
        return redirect('dashboard')

    if service_request.is_approved:
        messages.warning(request, "This task has already been approved.")
    else:
        # Transfer TimeCredits
        provider_credit, _ = TimeCredit.objects.get_or_create(user=service_request.provider)
        requester_credit = get_object_or_404(TimeCredit, user=service_request.user)

        if requester_credit.balance >= service_request.credit_amount:
            # Deduct from requester and add to provider
            requester_credit.balance -= service_request.credit_amount
            provider_credit.balance += service_request.credit_amount
            requester_credit.save()
            provider_credit.save()

            service_request.is_approved = True
            service_request.save()

            messages.success(request, f"You have approved the task. {service_request.credit_amount} TimeCredits transferred to {service_request.provider.username}.")
        else:
            messages.error(request, "You do not have enough balance to approve this task.")

    return redirect('dashboard')







from .forms import ServiceLogForm

@login_required
def log_service(request):
    if request.method == 'POST':
        form = ServiceLogForm(request.POST)
        if form.is_valid():
            # Automatically associate the logged-in user with the service log
            service_log = form.save(commit=False)
            service_log.user = request.user  # Set the user who provided the service
            service_log.save()
            # Optionally: Update user's time credits here
            messages.success(request, "Your service hours have been successfully logged.")
            return redirect('dashboard')  # Redirect to the dashboard or any relevant page
    else:
        form = ServiceLogForm()

    return render(request, 'log_service.html', {'form': form})

@login_required
# def approve_service_log(request, log_id):
#     log = get_object_or_404(ServiceLog, id=log_id)
    
#     # Ensure that the logged-in user is the client who made the request
#     if log.request.user != request.user:
#         messages.error(request, "You are not authorized to approve this service log.")
#         return redirect('dashboard')  # or another relevant page

#     # Mark the service log as approved
#     if log.status == 'pending':
#         log.status = 'approved'
#         log.save()

#         # Award credits to the provider
#         log.provider.timecredit.balance += log.credits_earned
#         log.provider.timecredit.save()

#         messages.success(request, "You have successfully approved the service log.")
#     else:
#         messages.warning(request, "This service log is already approved or rejected.")

#     return redirect('service_request_detail', request_id=log.request.id)

def approve_service_log(request, log_id):
    log = get_object_or_404(ServiceLog, id=log_id)

    if log.request.user != request.user:
        messages.error(request, "You are not authorized to approve this service log.")
        return redirect('dashboard')

    if log.status == 'pending':
        log.status = 'approved'  # FIXED BUG
        log.save()

        log.provider.timecredit.balance += log.credits_earned
        log.provider.timecredit.save()

        messages.success(request, "You have successfully approved the service log.")
    else:
        messages.warning(request, "This service log is already approved or rejected.")

    return redirect('request_detail', request_id=log.request.id)


@login_required
def reject_service_log(request, log_id):
    log = get_object_or_404(ServiceLog, id=log_id)
    
    # Ensure that the logged-in user is the client who made the request
    if log.request.user != request.user:
        messages.error(request, "You are not authorized to reject this service log.")
        return redirect('dashboard')  # or another relevant page

    # Mark the service log as rejected
    if log.status == 'pending':
        log.status = 'rejected'
        log.save()

        messages.success(request, "You have successfully rejected the service log.")
    else:
        messages.warning(request, "This service log is already approved or rejected.")

    return redirect('request_detail', request_id=log.request.id)
