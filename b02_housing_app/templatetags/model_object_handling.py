from django import template
register = template.Library()

@register.filter
def getattribute (obj, attribute):
    try:
        return obj.__getattribute__(attribute)
    except:
        return "ERROR"

@register.filter
def hasattribute (obj, attribute):
    return hasattr(obj, attribute)

@register.filter
def get_valid_fields(obj):
    return obj.get_valid_fields()

@register.filter
def field_desc(obj,field_name):
    obj_class = obj.__class__
    return obj_class.field_desc(field_name)
