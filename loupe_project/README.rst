==============
Django-Loupe
==============

django-loupe is a simple image/screenshot review application to add to your django project to allow collaborative discussions about about a projects design processes.

Installation:
=============

1. Put ``loupe`` to your ``INSTALLED_APPS`` in your ``settings.py``
   within your django project.

2.  Add the following to your settings.py or local_settings.py and adjust it to your liking

LOUPE_RESIZE_THUMB_WIDTH = 100 # Width in pixels of the thumbnail
LOUPE_RESIZE_THUMB_HEIGHT  = 75 # Height in pixels of the thumbnail
LOUPE_RESIZE_THUMB_CROP = True # Crop thubmnails? True or False
LOUPE_RESIZE_DISPLAY_WIDTH = 800 # Width in pixels of the display size (not full size image)
LOUPE_PRE_CACHE_IMAGES = True # Pre-cache images on upload? True or False
LOUPE_INCREMENT_COUNT = True # Increment the view count on images? True or False


Features:
=========


Roadmap:
========
