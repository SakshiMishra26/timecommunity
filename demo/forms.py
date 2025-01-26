from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Service,Booking,Review,TimeTransaction
from .models import ServiceRequest,UserLocation

# from django.core.exceptions import ValidationError




class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'category', 'hours_offered','price','image','location']

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['title', 'description', 'category', 'hours_requested','location']

        

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# class CustomRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')

#         if password != confirm_password:
#             raise ValidationError("Passwords do not match")

#         return cleaned_data

class UserLocationForm(forms.ModelForm):
    class Meta:
        model = UserLocation
        fields = ['city', 'state', 'country', 'zip_code']


class TimeTransactionForm(forms.ModelForm):
    class Meta:
        model = TimeTransaction
        fields = ['transaction_type', 'hours']

class LogHoursForm(forms.Form):
    hours = forms.IntegerField(min_value=1, required=True)
    hours_worked = forms.DecimalField(max_digits=5, decimal_places=2)

# class TimeCreditForm(forms.Form):
#     amount = forms.DecimalField(max_digits=5, decimal_places=2, min_value=0.01, label="Amount of Time Credits")
#     description = forms.CharField(max_length=500, widget=forms.Textarea, required=False, label="Description")


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