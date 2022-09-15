# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.contrib import admin

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
        'id','name'
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
        'overall_rarity',
        )




