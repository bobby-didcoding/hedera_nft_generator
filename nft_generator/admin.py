# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .models import NoneFungibleToken, Token, Account, Category, Trait

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = (
        'id','name', 'ordering'
        )

@admin.register(Trait)
class Trait(admin.ModelAdmin):
    list_display = (
        'id','name'
        )
@admin.register(Account)
class Account(admin.ModelAdmin):
    list_display = (
        'id','name', 'account_id'
        )

@admin.register(Token)
class Token(admin.ModelAdmin):
    list_display = (
        'id','hedera_token_id','name',
        'symbol', 'max_supply','get_remaining_supply',
        'get_minted','get_awaiting_mint'
        )

@admin.register(NoneFungibleToken)
class NoneFungibleToken(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'minted',
        'send_to_ipfs',
        'create_new_image_from_traits'
        )

    def send_to_ipfs(self, obj):
        if obj.minted:
            return format_html('')
        else:
            url = (
                reverse("nft_generator:send-to-ipfs" ,kwargs={'id':obj.id})
                + "?"
                + urlencode({"url": reverse("admin:nft_generator_nonefungibletoken_changelist")}) 
            )
            return format_html('<a href="{}">Send</a>', url)

    send_to_ipfs.short_description = "Send to IPFS"

    def create_new_image_from_traits(self, obj):
        if obj.minted or obj.traits.all().count() == 0:
            return format_html('')
        else:
            url = (
                reverse("nft_generator:create_from_traits" ,kwargs={'id':obj.id})
                + "?"
                + urlencode({"url": reverse("admin:nft_generator_nonefungibletoken_changelist")}) 
            )
            return format_html('<a href="{}">Create new artwork</a>', url)

    create_new_image_from_traits.short_description = "Create new artwork from traits"




