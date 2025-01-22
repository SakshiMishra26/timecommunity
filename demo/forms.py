from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Service,Booking,Review,TimeTransaction
from .models import ServiceRequest




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'hours_offered','price','image']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'category', 'hours_requested']

        

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TimeTransactionForm(forms.ModelForm):
    class Meta:
        model = TimeTransaction
        fields = ['transaction_type', 'hours']

class LogHoursForm(forms.Form):
    hours = forms.IntegerField(min_value=1, required=True)
    hours_worked = forms.DecimalField(max_digits=5, decimal_places=2)


# class LogHoursForm(forms.Form):
#     hours_worked = forms.DecimalField(max_digits=5, decimal_places=2)

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'date', 'time']
        widgets = {
            'date': forms.SelectDateWidget(),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['service', 'rating', 'comment']
        widgets = {
            'service': forms.HiddenInput(),  # Service should be preselected from the view
            'rating': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }