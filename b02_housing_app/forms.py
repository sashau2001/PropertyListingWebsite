from django import forms
from .models import Apartment,Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["apt_name","apt_review","apt_stars"]

class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["apt_name","apt_location"]
        fields += list(Apartment.field_dict.keys())
