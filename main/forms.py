from django import forms
from main import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget = forms.PasswordInput)

class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = '__all__'

