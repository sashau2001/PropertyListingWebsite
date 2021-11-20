from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from .forms import ReviewForm, ApartmentForm



def insert_review(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login/')
    form = ReviewForm(request.POST or None, request.FILES or None)
    if form.is_valid():
            form_save = form.save(commit=False)
            form_save.apt_reviewer = request.user.username
            form_save.save()
    context = {'form': form, 'insertReview': True}
    return render(request, 'default_form.html', context)

def insert_apartment(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('/accounts/google/login/')
    form = ApartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form_save = form.save(commit=False)
        # change form data
        form_save.save()
    context = {'form': form, 'insertApartment': True}
    return render(request, 'default_form.html', context)

def reviews(request):
    review_list = Review.objects.all()
    context = {'review_list': review_list, 'reviews': True}
    return render(request, 'reviews.html', context)

def review(request,pk):
    this_review = Review.objects.get(pk=pk)
    context = {'review': this_review, 'reviews': True}
    return render(request,'review.html',context)

def apartments(request):
    apartment_list = Apartment.objects.all()
    context = {'apartment_list': apartment_list, 'apartments': True}
    return render(request, 'apartments.html', context)

def apartment(request,pk):
    apt= Apartment.objects.get(pk=pk)
    context = {'google_api_key': settings.GOOGLE_API_KEY,
               'apartment': apt,
               'field_list': Apartment._meta.local_fields,
               'apartments': True,
               'location': apt.apt_location}
    return render(request,'apartment.html', context)

#Filter by name for now
def search_results(request):
    query = request.GET.get('name_query')
    filtered_list  = Apartment.objects.filter(apt_name__icontains=query)
    context = {'filtered_list': filtered_list}
    return render(request, 'search_results.html', context)
