from imagekit.specs import ImageSpec 
from imagekit import processors

from django.conf import settings

# thumbnail resize processor 
class ResizeThumb(processors.Resize): 
    width = settings.LOUPE_RESIZE_THUMB_WIDTH
    height = settings.LOUPE_RESIZE_THUMB_HEIGHT 
    crop = settings.LOUPE_RESIZE_THUMB_CROP

# display size resize processor
class ResizeDisplay(processors.Resize):
    width = settings.LOUPE_RESIZE_DISPLAY_WIDTH

# adjustment processor to enhance the image at small sizes 
class EnchanceThumb(processors.Adjustment): 
    contrast = 1.2 
    sharpness = 1.1 

# define our thumbnail spec 
class Thumbnail(ImageSpec): 
    access_as = 'thumbnail_image' 
    pre_cache = settings.LOUPE_PRE_CACHE_IMAGES 
    processors = [ResizeThumb, EnchanceThumb] 

# and our display spec
class Display(ImageSpec):
    access_as = 'display'
    pre_cache = settings.LOUPE_PRE_CACHE_IMAGES
    increment_count = settings.LOUPE_INCREMENT_COUNT
    processors = [ResizeDisplay]
