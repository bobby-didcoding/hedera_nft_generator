# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os
from decimal import *

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from nft_generator.models import Account, Trait, Category

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from apis.hedera.utils import AccountManager

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

User = get_user_model()
def get_model(model_name):
    app_name, model_name = model_name.split(".")
    Model = apps.get_model(app_name, model_name)
    return Model

def make_super_user(email, password):
    super_user, created = User.objects.get_or_create(
        username=email,
        password=make_password(password),
    )
    if created:
        print (f"*****Created {email}*****")
    super_user.is_staff=True
    super_user.is_superuser=True
    super_user.save()
    return super_user

def run():
    if not User.objects.filter(username=os.environ.get("DEFAULT_EMAIL")):
        print ("*****Creating users*****")
        #create a new super user for the app  
        main = make_super_user(
            os.environ.get("DEFAULT_EMAIL"),
            os.environ.get("PASSWORD"))
        main.first_name = os.environ.get("FIRST_NAME")
        main.last_name = os.environ.get("LAST_NAME")
        main.email = os.environ.get("DEFAULT_EMAIL")
        main.save()
        print ("*****finished creating users*****")

    print ("*****Updating Site model*****")
    site = Site.objects.first()
    site.name = "Main"
    site.domain = "localhost:8000"
    site.save()
    print ("*****Done*****")

    print ("*****Creating dummy users*****")
    acc, created = Account.objects.get_or_create(name=os.environ.get("DEMO_USER_1", 'Bill'), is_demo=True)
    if created:
        new_acc = AccountManager().create_new_account()
        acc.account_id = new_acc["acc_id"]
        acc.account_public_key = new_acc["public_key"]
        acc.account_private_key = new_acc["private_key"]
        acc.save()

    acc, created = Account.objects.get_or_create(name=os.environ.get("DEMO_USER_2", 'Ben'), is_demo=True)
    if created:
        new_acc = AccountManager().create_new_account()
        acc.account_id = new_acc["acc_id"]
        acc.account_public_key = new_acc["public_key"]
        acc.account_private_key = new_acc["private_key"]
        acc.save()

        print ("*****Done*****")

    print ("*****Creating project traits*****")
    traits = settings.TRAITS
    trait_quantity = settings.TRAIT_QUANTITY
    for t in traits:
        category, created = Category.objects.get_or_create(name = t)
        if created:
            for i in range(trait_quantity):
                trait = Trait.objects.create(category = category)
    print ("*****Done*****")


                   