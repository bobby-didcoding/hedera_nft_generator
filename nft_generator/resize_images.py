# --------------------------------------------------------------
# Python imports
# --------------------------------------------------------------
from io import BytesIO
from random import randint
import json

# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.conf import settings
from django.core.files.uploadedfile import File
from django.core.files.storage import default_storage

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .import utils
from .models import NoneFungibleToken, Token

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from apis.hedera.utils import TokenManager
from apis.ipfs.utils import add_to_ipfs

# --------------------------------------------------------------
# 3rd party imports
# --------------------------------------------------------------
from PIL import Image
from celery import shared_task
from celery.utils.log import get_task_logger


def test():
    for l in range(4):
        key = l+1
        images = [['base',Image.open(f'{settings.STATIC_ROOT}/base/{key}.png')],
        ['body',Image.open(f'{settings.STATIC_ROOT}/body/{key}.png')],
        ['hair',Image.open(f'{settings.STATIC_ROOT}/hair/{key}.png')],
        ['top',Image.open(f'{settings.STATIC_ROOT}/top/{key}.png')],
        ['pants',Image.open(f'{settings.STATIC_ROOT}/pants/{key}.png')],
        ['prop',Image.open(f'{settings.STATIC_ROOT}/prop/{key}.png')],
        ['bling',Image.open(f'{settings.STATIC_ROOT}/bling/{key}.png')]
        ]

        for img in images:
            resized_img = img[1].resize((1080, 1080), resample=Image.NEAREST)
            image_io = BytesIO()
            resized_img.save(image_io, "PNG")
            file_name = f'{img[0]}_{l}.png'
            image = File(image_io, name=file_name)
            file = default_storage.save(image.name, image)
            print(image.name)
    
    return 'Done'
