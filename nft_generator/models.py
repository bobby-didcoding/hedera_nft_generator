# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
import os
import json
from tabnanny import verbose
from unicodedata import category
from unittest.util import _MAX_LENGTH

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from PIL import Image

TRAITS = settings.TRAITS


class Category(TimeStampedModel,models.Model):
    """
    nft_generator.Category
    Stores a single category type
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    ordering = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural="Categories"


class Trait(TimeStampedModel,models.Model):
    """
    nft_generator.Trait
    Stores a single trait
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(default='blank.png', upload_to='traits')

    def __str__(self):
        return f'{self.name}'



class Account(TimeStampedModel,models.Model):
    """
    nft_generator.Account
    Stores a single account entry
    """
    name = models.CharField(max_length=100, null=True, blank=True)
    account_id = models.CharField(max_length=100, null=True, blank=True)
    account_public_key = models.CharField(max_length=100, null=True, blank=True)
    account_private_key = models.CharField(max_length=100, null=True, blank=True)
    nft_balance = models.IntegerField(default=0, null=True, blank=True)
    hbar_balance = models.CharField(max_length=100, null=True, blank=True)
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f"/account/{self.account_id}"


class Token(TimeStampedModel,models.Model):
    """
    nft_generator.Token
    Stores a single Token entry
    """
    company_name = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    symbol = models.CharField(max_length=3, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    max_supply = models.IntegerField(default=1000)
    hedera_token_id = models.CharField(max_length=100, null=True, blank=True)
    associated_accounts = models.ManyToManyField(Account, blank=True)

    def __str__(self):
        return f'{self.name}'

    @property
    def get_remaining_supply(self):
        return self.max_supply - NoneFungibleToken.objects.filter(token = self).count()

    @property
    def get_minted(self):
        return NoneFungibleToken.objects.filter(token = self, minted=True).count()

    @property
    def get_awaiting_mint(self):
        return NoneFungibleToken.objects.filter(token = self, minted=False).count()

    @property
    def get_associated(self):
        return self.associated_accounts.all().count()

    @property
    def get_transferred(self):
        return NoneFungibleToken.objects.filter(token = self, minted=True, account__isnull=False).count()


class NoneFungibleToken(TimeStampedModel,models.Model):
    """
    nft_generator.NoneFungibleToken
    Stores a single nft entry, related to :model:`nft_generator.Token` and
    :model:`nft_generator.Account`.
    """
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    token = models.ForeignKey(Token, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='blank.png', upload_to='nfts')
    traits = models.ManyToManyField(Trait, blank=True)

    file = models.FileField(default='blank.json', upload_to='json')
    hedera_serials = models.CharField(max_length=100, null=True, blank=True)
    minted = models.BooleanField(default=False)

    @property
    def get_image_name(self):
        return os.path.basename(self.image.name)
    @property
    def get_file_name(self):
        return os.path.basename(self.file.name)

    @property
    def get_ipfs_file_cid(self):
        return self.ipfs_file_uri.split('?')[0].replace('https://ipfs.io/ipfs/', '')
    
    @property
    def get_description(self):
        return self.token.description

    @property
    def get_creator(self):
        return self.token.company_name

    @property
    def get_file_name(self):
        return os.path.basename(self.file.name)

    ipfs_image_uri = models.URLField(max_length=200, blank=True, null=True)
    ipfs_file_uri = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f"/nft/{self.id}"

    def all_nfts(self):
        all_nfts = NoneFungibleToken.objects.all()
        return all_nfts.count()


    def get_rarity(self, **kwargs):
        trait = kwargs.get("trait")
        nft_qty = NoneFungibleToken.objects.filter(traits__name=trait.name).count()
        return format(1-(nft_qty / self.all_nfts()), '.2%')

    @property
    def overall_rarity(self):
        trait_list = []
        for t in TRAITS:
            # kwargs = {
            #     f'nft_attributes__{t.lower()}':self.nft_attributes[t.lower()]
            # }
            trait = NoneFungibleToken.objects.filter(traits__category__name=t.lower()).count()
            trait_list.append(trait)

        total_traits = 0
        for t in trait_list:
            total_traits += t
        total_nfts = self.all_nfts() * len(trait_list)
        return format(total_traits /total_nfts, '.2%')

