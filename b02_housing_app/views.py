from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from .forms import *
from django.contrib import messages
import requests,json

def insert_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            context = {'form': ReviewForm(request.GET), 'insertReview': True}
            form_save = form.save(commit=False)
            form_save.apt_reviewer = request.user.username
            form_save.save()
            messages.success(request, 'Submitted successfully')
            return render(request, 'default_form.html', context)
    else:
        form = ReviewForm()
    context = {'form': form, 'insertReview': True}
    return render(request, 'default_form.html', context)

def insert_apartment(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('/accounts/google/login/')
    form = ApartmentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form_save = form.save(commit=False)
        # set ID
        form_save.id = get_new_id()
        form_save.save()
    context = {'form': form, 'insertApartment': True}
    return render(request, 'default_form.html', context)

def get_new_id():
    id_list = sorted(Apartment.objects.values_list('id', flat=True))
    new_id = 1
    for value in id_list:
        if new_id<value:
            break
        if new_id==value:
            new_id+=1
    return new_id

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
               'apartments': True,
               'location': apt.apt_location}
    return render(request,'apartment.html', context)

def my_profile(request):
    # not logged in
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login/')
    context = {'profiles': True, 'editable': True}
    prof_list = Profile.objects.filter(user=request.user)
    # no user profile exists yet
    if not prof_list.exists():
        form = ProfileForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form_save = form.save(commit=False)
            # set user
            form_save.user = request.user
            form_save.save()
        context = {'form': form, 'profile': True}
        return render(request, 'default_form.html', context)
    # user profile already exists
    prof = prof_list[0]
    context['profile'] = prof
    return render(request, 'profile.html', context)

def search_results(request):
    
    price_query = request.GET.get('price')    
    name_query = request.GET.get('name')
    # Name filtering
    if price_query is not None:
        apt_list  = list(Apartment.objects.filter(apt_name__icontains=name_query).order_by(price_query))
    else:
        apt_list  = list(Apartment.objects.filter(apt_name__icontains=name_query))


    context = {'apt_list': apt_list}
    return render(request, 'search_results.html', context)
