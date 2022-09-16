# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from io import BytesIO
from random import randint
import json
import time
import random

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings
from django.core.files.uploadedfile import File
from django.db.models import Max

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .import utils
from .models import NoneFungibleToken, Token, Account, Category, Trait

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from apis.hedera.utils import TokenManager, AccountManager
from apis.ipfs.utils import add_to_ipfs

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from PIL import Image
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

def get_random_trait(category):
    traits = Trait.objects.filter(category=category)
    trait_quantity = settings.TRAIT_QUANTITY
    rand = randint(0,trait_quantity-1)
    return traits[rand]


@shared_task(bind=True)
def create_nft(self, quantity, token_id):
    '''
    This allows us to create NFT artwork locally.
    This also calls the IPFS api in apis/ipfs/utils
    '''
    categories = Category.objects.all().order_by('ordering')
    token = Token.objects.get(id = token_id)
    for nft in range(int(quantity)):
        time.sleep(2)

        new_nft = NoneFungibleToken.objects.create(token=token)
        
        blank_image = Image.open(f'{settings.MEDIA_ROOT}/blank.png').convert('RGBA')
        for category in categories:
            trait = get_random_trait(category)
            img = Image.open(trait.image.path).convert('RGBA')
            blank_image.paste(img, (0, 0), img)
            new_nft.traits.add(trait)
            new_nft.save()
   
        #Resize image to OpenSea market recommended size - "Resample Nearest" to retain resolution
        resized_img = blank_image.resize((1500, 1500), resample=Image.NEAREST)
        image_io = BytesIO()

        token_name = new_nft.token.name

        resized_img.save(image_io, "PNG")
        name = f'{token_name}_{new_nft.id}'
        file_name = f'{name}.png'
        image = File(image_io, name=file_name)

        new_nft.image = image
        new_nft.name = name
        new_nft.slug = name
        new_nft.save()

        #Send new image to IFPS and 
        ipfs_image_uri = add_to_ipfs(new_nft.image.path, new_nft.get_image_name)
        new_nft.ipfs_image_uri = ipfs_image_uri
        new_nft.save()
        prop_list = [{"trait_type":t.category.name.lower(),"value": t.name} for t in new_nft.traits.all()]

        meta = {
            "name":new_nft.name,
            "creator":new_nft.get_creator,
            "description":new_nft.get_description,
            "type":"image/png",
            "format":"none",
            "properties": prop_list,
            "image":new_nft.ipfs_image_uri.split('?')[0].replace('https://ipfs.io/ipfs/', 'ipfs://')
        }

        blank_filename = f'media/blank.json'
        new_filename = f'{new_nft.name}.json'

        with open(blank_filename, 'w') as f:
            json.dump(meta ,f, indent=4, sort_keys=True, default=str)

        with open(blank_filename, "r") as f:
            new_nft.file.save(new_filename, f)

        new_nft.save()

        #Send new json to IFPS and 
        ipfs_file_uri = add_to_ipfs(new_nft.file.path, new_nft.get_file_name)
        new_nft.ipfs_file_uri = ipfs_file_uri
        new_nft.save()

        print('NFT created')
    return('Done')


@shared_task(bind=True)
def create_new_from_traits(self, nft_id):
    '''
    This allows us to create NFT artwork locally from the admin page
    This also calls the IPFS api in apis/ipfs/utils
    '''
    new_nft = NoneFungibleToken.objects.get(id=nft_id)
    
    blank_image = Image.open(f'{settings.MEDIA_ROOT}/blank.png').convert('RGBA')
    for trait in new_nft.traits.all():
        img = Image.open(trait.image.path).convert('RGBA')
        blank_image.paste(img, (0, 0), img)

    #Resize image to OpenSea market recommended size - "Resample Nearest" to retain resolution
    resized_img = blank_image.resize((1500, 1500), resample=Image.NEAREST)
    image_io = BytesIO()

    token_name = new_nft.token.name

    resized_img.save(image_io, "PNG")
    name = f'{token_name}_{new_nft.id}'
    file_name = f'{name}.png'
    image = File(image_io, name=file_name)

    new_nft.image = image
    new_nft.save()

    #Send new image to IFPS and 
    ipfs_image_uri = add_to_ipfs(new_nft.image.path, new_nft.get_image_name)
    new_nft.ipfs_image_uri = ipfs_image_uri
    new_nft.save()
    prop_list = [{"trait_type":t.category.name.lower(),"value": t.name} for t in new_nft.traits.all()]

    meta = {
        "name":new_nft.name,
        "creator":new_nft.get_creator,
        "description":new_nft.get_description,
        "type":"image/png",
        "format":"none",
        "properties": prop_list,
        "image":new_nft.ipfs_image_uri.split('?')[0].replace('https://ipfs.io/ipfs/', 'ipfs://')
    }

    blank_filename = f'media/blank.json'
    new_filename = f'{new_nft.name}.json'

    with open(blank_filename, 'w') as f:
        json.dump(meta ,f, indent=4, sort_keys=True, default=str)

    with open(blank_filename, "r") as f:
        new_nft.file.save(new_filename, f)

    new_nft.save()

    #Send new json to IFPS and 
    ipfs_file_uri = add_to_ipfs(new_nft.file.path, new_nft.get_file_name)
    new_nft.ipfs_file_uri = ipfs_file_uri
    new_nft.save()

    print('NFT created')
    return('Done')


@shared_task(bind=True)
def create_ipfs_cid(self, nft_id):
    '''
    This allows us to create NFT artwork from the admin page
    '''

    new_nft = NoneFungibleToken.objects.get(id=nft_id)

    #Send new image to IFPS and 
    ipfs_image_uri = add_to_ipfs(new_nft.image.path, new_nft.get_image_name)
    new_nft.ipfs_image_uri = ipfs_image_uri
    new_nft.save()
    prop_list = [{"trait_type":t.category.name.lower(),"value": t.name} for t in new_nft.traits.all()]

    meta = {
        "name":new_nft.name,
        "creator":new_nft.get_creator,
        "description":new_nft.get_description,
        "type":"image/png",
        "format":"none",
        "properties": prop_list,
        "image":new_nft.ipfs_image_uri.split('?')[0].replace('https://ipfs.io/ipfs/', 'ipfs://')
    }

    blank_filename = f'media/blank.json'
    new_filename = f'{new_nft.name}.json'

    with open(blank_filename, 'w') as f:
        json.dump(meta ,f, indent=4, sort_keys=True, default=str)

    with open(blank_filename, "r") as f:
        new_nft.file.save(new_filename, f)

    new_nft.save()

    #Send new json to IFPS and 
    ipfs_file_uri = add_to_ipfs(new_nft.file.path, new_nft.get_file_name)
    new_nft.ipfs_file_uri = ipfs_file_uri
    new_nft.save()

    print('NFT created')
    return('Done')



@shared_task(bind=True)
def create_token(self, token):
    '''
    Used to invoke the TokenManager in apis/hedera/api
    This allows us to create a Token - this is the first step.
    '''
    manager = TokenManager()
    hedera_token_id = manager.create_token(
        max_supply = token.max_supply,
        token_name = token.name,
        token_symbol = token.symbol
        )
    
    token.hedera_token_id = hedera_token_id
    token.save()
    return 'Token created'



@shared_task(bind=True)
def mint_nft(self, token):
    '''
    Used to invoke the TokenManager in apis/hedera/api
    This allows us to mint NFT's that have been generated locally
    '''
    nfts = NoneFungibleToken.objects.filter(minted=False, token = token)
    for nft in nfts:
        manager = TokenManager()
        nft_id = manager.mint_new_nft(
            nft = nft
            )
        nft.hedera_serials = nft_id
        nft.minted = True
        nft.save()
    return "NFT creation complete"


@shared_task(bind=True)
def associate_account(self, token_id, account_id):
    '''
    Used to invoke the TokenManager in apis/hedera/api
    This allows us to associate an account/wallet to a Token
    '''
    account = Account.objects.get(account_id = account_id)
    token = Token.objects.get(id=token_id)
    TokenManager().associate(account=account,token=token)
    return f'Account {account.account_id} has been associated to token {token.hedera_token_id}'


@shared_task(bind=True)
def transfer_nft(self, nft_id, account_id):
    '''
    Used to invoke the TokenManager in apis/hedera/api
    This allows us to transfer a minted NFT to an associated account/wallet
    '''
    account = Account.objects.get(id = account_id)
    nft = NoneFungibleToken.objects.get(id=nft_id)
    TokenManager().transfer(account=account, nft=nft)
    return f'NFT {nft.name} has been transferred to Account {account.account_id}'