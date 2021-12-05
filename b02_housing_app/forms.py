from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["apt_name","apt_review","apt_stars"]

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["apt_name","apt_location"]
        fields += list(Apartment.field_dict.keys())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = list(Profile.field_dict.keys())
