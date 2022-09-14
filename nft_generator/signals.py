# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from . models import Token, Account
from .tasks import create_token

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from apis.hedera.utils import AccountManager
 
@receiver(post_save, sender=Token, weak=False)
def create_profile(sender, instance, created, **kwargs):
    '''
    Used to create a Token ID
    '''
    if created:
        create_token(instance)


@receiver(post_save, sender=Account, weak=False)
def create_account(sender, instance, created, **kwargs):
    '''
    Used to create a new account 
    '''
    if created:
        if instance.is_demo == False:
            manager = AccountManager(account_id = instance.account_id)
            info_response = manager.query_account_info()
            instance.account_public_key = info_response["key"]
            instance.nft_balance = int(info_response["nfts"])
            balance_response = manager.query_account_balance()
            instance.hbar_balance = balance_response["hbars"]
            instance.save()