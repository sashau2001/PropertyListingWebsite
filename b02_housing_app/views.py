# from django.http import HttpResponseRedirect
# from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
# from django.urls import reverse
# from django.views import generic
from .models import Apartment,Review
# from django.utils import timezone
from .forms import ReviewForm


def insert_review(request):
    context = {}
    form = ReviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
    context['form'] = form
    return render(request, 'reviewform.html', {'form': form})


def reviews(request):
    review_list = Review.objects.all()
    context = {'review_list': review_list}
    return render(request, 'reviews.html', context)

def apartments(request):
    apartment_list = Apartment.objects.all()
    context = {'apartment_list': apartment_list}
    return render(request, 'apartments.html', context)

def apartment(request,pk):
    apartment = Apartment.objects.all()[pk-1] # since database ID starts at 1
    context = {'apartment': apartment, 'field_list': Apartment._meta.local_fields}
    return render(request,'apartment.html', context)
