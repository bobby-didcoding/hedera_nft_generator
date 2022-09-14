# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from io import BytesIO
from random import randint
import json
import time

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings
from django.core.files.uploadedfile import File

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .import utils
from .models import NoneFungibleToken, Token, Account

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

def randomise():
    return str(randint(1,10))

@shared_task(bind=True)
def create_nft(self, quantity):
    base_dict = utils.createBaseDict()
    body_dict = utils.createBodyDict()
    hair_dict = utils.createHairDict()
    top_dict = utils.createTopDict()
    pants_dict = utils.createPantsDict()
    prop_dict = utils.createPropDict()
    bling_dict = utils.createBlingDict()
    tattoo_dict = utils.createTattooDict()
    shades_dict = utils.createShadesDict()
    coin_dict = utils.createCoinDict()


    for nft in range(int(quantity)):
        time.sleep(2)
        nft_attributes = {}
        
        base_key = randomise()
        base = Image.open(f'{settings.STATIC_ROOT}/base/base_{base_key}.png')
        nft_attributes["base"] = base_dict[int(base_key)]

        body_key = randomise()
        body = Image.open(f'{settings.STATIC_ROOT}/body/body_{body_key}.png')
        nft_attributes["body"] = body_dict[int(body_key)]

        hair_key = randomise()
        hair = Image.open(f'{settings.STATIC_ROOT}/hair/hair_{hair_key}.png')
        nft_attributes["hair"] = hair_dict[int(hair_key)]

        top_key = randomise()
        top = Image.open(f'{settings.STATIC_ROOT}/top/top_{top_key}.png')
        nft_attributes["top"] = top_dict[int(top_key)]

        pants_key = randomise()
        pants = Image.open(f'{settings.STATIC_ROOT}/pants/pants_{pants_key}.png')
        nft_attributes["pants"] = pants_dict[int(pants_key)]

        prop_key = randomise()
        prop = Image.open(f'{settings.STATIC_ROOT}/prop/prop_{prop_key}.png')
        nft_attributes["prop"] = prop_dict[int(prop_key)]

        bling_key = randomise()
        bling = Image.open(f'{settings.STATIC_ROOT}/bling/bling_{bling_key}.png')
        nft_attributes["bling"] = bling_dict[int(bling_key)]

        tattoo_key = randomise()
        tattoo = Image.open(f'{settings.STATIC_ROOT}/tattoo/tattoo_{tattoo_key}.png')
        nft_attributes["tattoo"] = tattoo_dict[int(tattoo_key)]

        shades_key = randomise()
        shades = Image.open(f'{settings.STATIC_ROOT}/shades/shades_{shades_key}.png')
        nft_attributes["shades"] = shades_dict[int(shades_key)]

        coin_key = randomise()
        coin = Image.open(f'{settings.STATIC_ROOT}/coin/coin_{shades_key}.png')
        nft_attributes["coin"] = coin_dict[int(coin_key)]

        # Paste/Merge Required PNGs, as layers on base
        base.paste(body, (0, 0), body)
        base.paste(hair, (0, 0), hair)
        base.paste(top, (0, 0), top)
        base.paste(pants, (0, 0), pants)
        base.paste(prop, (0, 0), prop)
        base.paste(bling, (0, 0), bling)
        base.paste(tattoo, (0, 0), tattoo)
        base.paste(shades, (0, 0), shades)
        base.paste(coin, (0, 0), coin)

        #create a new NFT object in db - with json attributes
        new_nft = NoneFungibleToken(token=Token.objects.last())
        new_nft.nft_attributes = nft_attributes
        new_nft.save()

        #Resize image to OpenSea market recommended size - "Resample Nearest" to retain resolution
        resized_img = base.resize((1500, 1500), resample=Image.NEAREST)
        image_io = BytesIO()

        token = Token.objects.last()
        token_name = token.name

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
        ipfs_image_uri_internal = ipfs_image_uri.replace('https://ipfs.io/ipfs/', 'ipfs://')
        ipfs_image_uri_hedera = ipfs_image_uri.split('?')[0].replace('https://ipfs.io/ipfs/', 'ipfs://')
        ipfs_image_cid = ipfs_image_uri.split('?')[0].replace('https://ipfs.io/ipfs/', '')

        new_nft.ipfs_image_uri = ipfs_image_uri
        new_nft.ipfs_image_uri_internal = ipfs_image_uri_internal
        new_nft.ipfs_image_uri_hedera = ipfs_image_uri_hedera
        new_nft.ipfs_image_cid = ipfs_image_cid
        new_nft.save()

        meta = {
            "name":new_nft.name,
            "creator":new_nft.get_creator,
            "description":new_nft.get_description,
            "type":"image/png",
            "format":"none",
            "properties":[
                {
                    "trait_type":"base",
                    "value": new_nft.nft_attributes["base"]
                },
                {
                    "trait_type":"body",
                    "value": new_nft.nft_attributes["body"]
                },
                {
                    "trait_type":"hair",
                    "value": new_nft.nft_attributes["hair"]
                },
                {
                    "trait_type":"top",
                    "value": new_nft.nft_attributes["top"]
                },
                {
                    "trait_type":"pants",
                    "value": new_nft.nft_attributes["pants"]
                },
                {
                    "trait_type":"prop",
                    "value": new_nft.nft_attributes["prop"]
                },
                {
                    "trait_type":"bling",
                    "value": new_nft.nft_attributes["bling"]
                },
                {
                    "trait_type":"tattoo",
                    "value": new_nft.nft_attributes["tattoo"]
                },
                {
                    "trait_type":"shades",
                    "value": new_nft.nft_attributes["shades"]
                },
                {
                    "trait_type":"coin",
                    "value": new_nft.nft_attributes["coin"]
                },
            ],
            "image":new_nft.ipfs_image_uri_hedera
        }
        new_nft.metadata = dict(meta)

        blank_filename = f'media/blank.json'
        new_filename = f'{new_nft.name}.json'

        with open(blank_filename, 'w') as f:
            json.dump(meta ,f, indent=4, sort_keys=True, default=str)

        with open(blank_filename, "r") as f:
            new_nft.file.save(new_filename, f)

        new_nft.save()

        #Send new json to IFPS and 
        ipfs_file_uri = add_to_ipfs(new_nft.file.path, new_nft.get_file_name)
        ipfs_file_uri_internal = ipfs_file_uri.replace('https://ipfs.io/ipfs/', 'ipfs://')
        ipfs_file_uri_hedera = ipfs_file_uri.split('?')[0].replace('https://ipfs.io/ipfs/', 'ipfs://')
        ipfs_file_cid = ipfs_file_uri.split('?')[0].replace('https://ipfs.io/ipfs/', '')
        new_nft.ipfs_file_uri = ipfs_file_uri
        new_nft.ipfs_file_uri_internal = ipfs_file_uri_internal
        new_nft.ipfs_file_uri_hedera = ipfs_file_uri_hedera
        new_nft.ipfs_file_cid = ipfs_file_cid
        new_nft.save()

        print('NFT created')
    return('Done')



@shared_task(bind=True)
def create_token(self, token):
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
def associate_account(self, token_name, account_id):
    acc = Account.objects.get(account_id = account_id)
    token_obj = Token.objects.get(name=token_name)
    manager = TokenManager().associate(acc=acc.account_id, key = acc.account_private_key, token=token_obj.hedera_token_id)
  

    return f'Account {account_id} has been associated to token {token_obj.hedera_token_id}'


@shared_task(bind=True)
def transfer_nft(self, nft, account_id):
    acc = Account.objects.get(account_id = account_id)
    nft_obj = NoneFungibleToken.objects.get(slug=nft)
    manager = TokenManager().transfer(account_id=acc.account_id, nft=int(nft_obj.hedera_serials), token = nft_obj.token.hedera_token_id)
  
    return f'NFT {nft_obj.slug} has been transferred to Account {account_id}'