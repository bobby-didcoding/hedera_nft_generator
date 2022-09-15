# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django import template

register = template.Library()

@register.simple_tag
def get_rarity(obj, trait):
    return obj.get_rarity(trait=trait)