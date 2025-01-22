from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TimeTransactionForm,LogHoursForm,ServiceForm,BookingForm,ReviewForm
from .models import Service, TimeCredit,TimeTransaction,Booking,Review,UserActivity
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from decimal import Decimal
from django.http import JsonResponse
from django.contrib import messages
from .models import ServiceRequest,Transaction,Request
from .forms import ServiceRequestForm







def about_us(request):
    return render(request, 'about_us.html')

# def home(request):
#     return render(request, 'home.html')

def home(request):
    # services = Service.objects.all() 
    services = Service.objects.all()[:4]  # Assuming you have a Service model for offers
    service_requests = ServiceRequest.objects.all()[:4]  # Fetch all service requests
    return render(request, 'home.html', {
        'services': services,
        'service_requests': service_requests
    })



def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
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








@login_required
def dashboard(request):
    user = request.user

    # Fetch the TimeCredit object for the logged-in user
    try:
        time_credit = TimeCredit.objects.get(user=user)
    except TimeCredit.DoesNotExist:
        time_credit = None

    # Fetch transactions for the user
    transactions = TimeTransaction.objects.filter(user=user)

    # Fetch services offered by the user
    services = Service.objects.filter(user=user)

    # Fetch service requests accepted by the user
    # accepted_requests = ServiceRequest.objects.filter(accepted_by=user)
    accepted_requests = ServiceRequest.objects.filter(accepted_by=None).exclude(user=user)


    return render(request, 'dashboard.html', {
        'user': user,
        'time_credit': time_credit,
        'transactions': transactions,
        'services': services,
        'accepted_requests': accepted_requests,  # Pass the accepted requests to the template
    })


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

 
def service_list(request):
    services = Service.objects.all()
    category = request.GET.get('category')
    # if request.is_ajax():
    #     data = list(services.values('id', 'name', 'description'))
    #     return JsonResponse({'services': data})
    if category:
        services = services.filter(category=category)
    return render(request, 'service_list.html', {'services': services})


from django.http import JsonResponse

def service_list(request):
    category = request.GET.get('category', 'All')
    services = Service.objects.filter(category=category) if category != 'All' else Service.objects.all()

    # Check for AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return JSON response for AJAX requests
        return JsonResponse({'services': list(services.values())})

    # Render normal response for non-AJAX requests
    return render(request, 'service_list.html', {'services': services})


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



@login_required
def add_service_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            return redirect('request_list')
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


# def accept_service_request(request, request_id):
#     service_request = get_object_or_404(ServiceRequest, id=request_id)

#     # Check if the logged-in user is trying to accept their own request
#     if service_request.user == request.user:
#         messages.error(request, "You cannot accept your own request.")
#         return redirect('request_list')

#     if service_request.accepted_by is None:
#         service_request.accepted_by = request.user
#         service_request.save()
#         messages.success(request, "Request accepted successfully.")
#     else:
#         messages.warning(request, "This request has already been accepted.")
#     return redirect('request_list')




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

    return redirect('request_detail', request_id=service_request.id)

   

   

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



# def request_detail(request, pk):
#     print(Request.objects.all())  # Debugging line
#     request_obj = get_object_or_404(Request, pk=pk)
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




def approve_service(request, id):
    service = get_object_or_404(Service, id=id)
    if service.user != request.user:  
        service.is_approved = True
    service.save()
    messages.success(request, f'Service "{service.title}" has been approved.')

    return redirect('home')  

def reject_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.is_approved = False
    service.save()
    messages.warning(request, f'Service "{service.title}" has been rejected.')

    return redirect('home')  # Red

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