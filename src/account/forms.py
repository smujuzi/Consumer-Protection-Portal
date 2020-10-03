from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from protect.config import *
from material import Layout, Row, Fieldset
import logging

log = logging.getLogger(__name__)
# convert the errors to text
from django.utils.encoding import force_text


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    full_names = forms.CharField(
        label='Full Names',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. James Lukwago'}))

    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={
        'required': 'A valid phone number is required'
    },
                                   help_text='If in another country, specify the country code e.g. +254',
                                   widget=forms.TextInput(attrs={'placeholder': '0772123456'}))
    address = forms.CharField(
        label='Physical Address',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))

    password1 = forms.CharField(max_length=254, label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter a password'}))
    password2 = forms.CharField(max_length=254, label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = Account
        fields = ('full_names', 'address', 'phone_number', 'image', 'email', 'password1', 'password2')

    layout = Layout('full_names', 'address', 'phone_number', 'image', 'email', 'password1', 'password2')


STAFF_ROLE_CHOICES = (
    ("Director Legal", 'Director Legal'),
    ("Manager", 'Manager'),
    ("I.T. Officer", 'I.T. Officer'),
    ("Service Desk", 'Service Desk'),
)


class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    full_names = forms.CharField(
        label='Full Names',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. James Lukwago'}))

    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={
        'required': 'A valid phone number is required'
    },
                                   help_text='If in another country, specify the country code e.g. +254',
                                   widget=forms.TextInput(attrs={'placeholder': '0772123456'}))
    address = forms.CharField(
        label='Physical Address',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))

    role = forms.ChoiceField( label='Role', choices=STAFF_ROLE_CHOICES)

    password1 = forms.CharField(max_length=254, label='Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Enter a password'}))
    password2 = forms.CharField(max_length=254, label='Confirm Password',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = Account
        fields = ('full_names', 'address', 'phone_number', 'image', 'email', 'role', 'password1', 'password2')

    layout = Layout('full_names', 'address', 'phone_number', 'image',  'email', 'role', 'password1', 'password2')


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    password = forms.CharField(max_length=254, label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

    layout = Layout('email', 'password')


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', help_text='We will communicate to you via email',
                             widget=forms.EmailInput(attrs={'placeholder': 'example@gou.go.ug'}))
    full_names = forms.CharField(
        label='Full_Names',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. National IT Authority - Uganda'}))
    phone_number = forms.CharField(min_length=10, max_length=15, error_messages={
        'required': 'A valid phone number is required'
    },
                                   help_text='If in another country, specify the country code e.g. +254',
                                   widget=forms.TextInput(attrs={'placeholder': '0772123456'}))
    address = forms.CharField(
        label='Physical Address',
        widget=forms.TextInput(
            attrs={'placeholder': 'e.g. Mackinon Road, Plot 4, Kampala-Uganda'}))

    class Meta:
        model = Account
        fields = ('full_names', 'address', 'phone_number', 'image', 'email')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(phone_number=phone_number)
        except Account.DoesNotExist:
            return phone_number
        raise forms.ValidationError('Phone number "%s" is already in use.' % account)

    layout = Layout('full_names', 'address', 'phone_number', 'image', 'email')
