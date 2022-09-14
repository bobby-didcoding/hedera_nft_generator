# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from functools import wraps

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.shortcuts import redirect, reverse

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from . models import Token

def redirect_if_no_token(function):
    """
    Redirects users away from view if token is not in DB
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        if not Token.objects.all().count():
            return redirect(reverse('nft_generator:token'))
        return function(request, *args, **kwargs)
    return wrap