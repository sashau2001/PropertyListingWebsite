from django import forms
from .models import *

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["apt_name","apt_review","apt_stars"]
        widgets = {
            'apt_name': forms.Select(attrs={
                'class': "form-control",
            }),
            'apt_stars': forms.Select(attrs={
                'class': "form-control",
            }),
            'apt_review': forms.Textarea(attrs={
                'class': "form-control",
            }),
        }


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["apt_name","apt_location"]
        fields += list(Apartment.field_dict.keys())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = list(Profile.field_dict.keys())
        widgets = {
            'public_username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
            }),
            'bio': forms.Textarea(attrs={
                'class': "form-control",
                'placeholder': 'Bio'
            }),
            'searching_for_apt': forms.CheckboxInput(),
            'price_range_max': forms.NumberInput(attrs={
                'class': "form-control",
                'step': 100
            }),
            'desired_movein_min': forms.DateInput(attrs={
                'class': "form-control",
                'placeholder': "yyyy-mm-dd"
            }),
            'desired_movein_max': forms.DateInput(attrs={
                'class': "form-control",
                'placeholder': "yyyy-mm-dd"
            }),
            'desired_beds_min': forms.NumberInput(attrs={
                'class': "form-control",
            }),
            'desired_beds_max': forms.NumberInput(attrs={
                'class': "form-control",
            }),
        }
