from django import forms
from .models import Review


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


