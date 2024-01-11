from django import template

register = template.Library()

@register.filter
def set(value):
    return value

@register.filter
def multiply(value, arg):
    return value * arg