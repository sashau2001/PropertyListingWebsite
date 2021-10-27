from django import template
register = template.Library()

@register.filter
def getattr (obj, attribute):
    try:
        return obj.__getattribute__(attribute)
    except:
        return "ERROR"
