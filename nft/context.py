from django.conf import settings
from nft_generator.models import Token, TRAITS, Account


def project_context(request):

    return {
        "tokens": Token.objects.filter(hedera_token_id__isnull = False),
        "traits": TRAITS,
        "accounts": Account.objects.all()
    }
        