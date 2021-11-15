from django import template
from b02_housing_app.models import *
register = template.Library()

@register.filter
def getattr (obj, attribute):
    try:
        return obj.__getattribute__(attribute)
    except:
        return "ERROR"

@register.filter
def get_valid_fields(obj):
    return obj.get_valid_fields()

@register.filter
def field_desc(field_name):
    return Apartment.field_desc(field_name)
