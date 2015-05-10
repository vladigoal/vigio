# -*- coding: utf-8 -*-
import os
from sorl.thumbnail.shortcuts import get_thumbnail
from django.conf import settings

def get_resized_thumb(image, size, image_folder='', crop='center'):
    try:
        res_image = get_thumbnail(os.path.join(settings.MEDIA_ROOT, image_folder, image.image.name), size, crop=crop)
        return res_image.url
    except:
        return ''