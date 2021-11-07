from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin

from .models import *

admin.site.register(Apartment)
admin.site.register(Review)
