from django import forms
from localflavor.us.forms import USZipCodeField
from django.contrib.auth.models import User


from .models import Location, Profile

class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True) #this will make the user not be able to change the username once set
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name')


class ProfileForm(forms.ModelForm):
     
     class Meta:
        model = Profile
        fields = ('photo', 'bio', 'phone')

       
       

class LocationForm(forms.ModelForm):
    address_1 = forms.CharField( required=True)
    zip_code =  USZipCodeField(required=True)
    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zip_code'}