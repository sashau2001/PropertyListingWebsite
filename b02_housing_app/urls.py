"""b02_housing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('submitreview/', views.insert_review, name='insert_review'),
    path('submitapartment/', views.insert_apartment, name='insert_apartment'),
    path('review/<int:pk>/', views.review, name='review'),
    path('reviews/', views.reviews, name='reviews'),
    path('apartment/<int:pk>/', views.apartment, name='apartment'),
    path('apartments/', views.apartments, name='apartments'),
    path('my_profile/',views.my_profile, name='my_profile'),
    path('my_profile/edit/',views.edit_profile, name='edit_profile'),
    path('my_profile/create/',views.create_profile, name='create_profile'),
]
