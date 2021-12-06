from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from .forms import *
from django.contrib import messages
import requests,json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView




def insert_review(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login/')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.apt_reviewer = request.user.username
            form_save.save()
            messages.success(request, 'Submitted successfully')
            return redirect('/reviews/')
    else:
        form = ReviewForm()
    context = {'form': form, 'insertReview': True}
    return render(request, 'review_form.html', context)

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login/')
    instance = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/my_profile/')
    context = {'form': form, 'myProfile': True}
    return render(request, 'profile_form.html', context)

def create_profile(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/google/login/')
    form = ProfileForm(request.POST or None)
    if form.is_valid():
        form.instance.user=request.user
        form.save()
        return redirect('/my_profile/')
    context = {'form': form, 'myProfile': True}
    return render(request, 'profile_form.html', context)

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

def homepage(request):
    return render(request, 'homepage.html')



def apartments(request):
    apt_list = Apartment.objects.all()
    p = Paginator(apt_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'apt_list': apt_list, 'apartments': True, 'page_obj': page_obj, 'p': p}
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
    context = {'myProfile': True, 'editable': True}
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

#Filter by name for now
def search_results(request):
    name_query = request.GET.get('name')
    price_query = request.GET.get('price')
    if price_query is None:
        price_query = 'apt_price'
    # Name filtering and price
    if name_query is None:
        apt_list = list(Apartment.objects.all().order_by(price_query))
    else:
        apt_list = list(Apartment.objects.filter(apt_name__icontains=name_query).order_by(price_query))

    # Distance sorting (w/r to location)
    location_query = request.GET.get('location')
    if location_query is not None and location_query!='':
        for apt in apt_list:
            apt.dist = get_distance(location_query, apt.apt_location)
        apt_list.sort(key=lambda k: k.dist)
        apt_list = [apt for apt in apt_list if apt.dist>=0] # remove apts with dist -1

    # Distance filtering
    maxdist_query = request.GET.get('maxdist')
    if location_query is not None and location_query!='' and maxdist_query is not None and maxdist_query!='':
        maxdist = float(maxdist_query)*1000 # convert from km to m
        apt_list = [apt for apt in apt_list if apt.dist<maxdist]

    p = Paginator(apt_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'apt_list': apt_list, 'name_query': name_query, 'page_obj': page_obj, 'p': p}
    return render(request, 'search_results.html', context)



def get_distance(source,dest):
    try:
        url = 'https://api.distancematrix.ai/maps/api/distancematrix/json?'
        req = requests.get(url + 'origins=' + source +
                         '&destinations=' + dest +
                         '&key=' + settings.DISTANCEMATRIX_API_KEY)
        return req.json()['rows'][0]['elements'][0]['distance']['value']
    except:
        return -1 # invaid address?



class ApartmentListView(ListView):
    model = Apartment
    paginate_by = 5
