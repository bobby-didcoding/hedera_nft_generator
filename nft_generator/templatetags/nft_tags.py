# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django import template

register = template.Library()

@register.simple_tag
def get_rarity(obj, name):
    return obj.get_rarity(name=name)