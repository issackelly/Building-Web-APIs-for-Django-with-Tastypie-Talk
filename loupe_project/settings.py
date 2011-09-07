# Django settings for example project.
import os, os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)
LOCAL_DEV = True

ADMINS = (
    ('Issac Kelly', 'issac@kellycreativetech.com')
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'dev,db'),
    }
}

MANAGERS = ADMINS
TIME_ZONE = 'America/New_York'

LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'site_media', 'media')
MEDIA_URL = '/site_media/media/'

ADMIN_MEDIA_PREFIX = '/site_media/static/admin/'

STATIC_URL = '/site_media/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'site_media', 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'x!1-h(xebm)y(w^j(#6mif#g57us^p+9g(e!$q342m7og4p_fb'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)

ROOT_URLCONF = 'loupe_project.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    [os.path.join(PROJECT_DIR, "templates")]
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.static',
    "django.core.context_processors.request",
    'django.core.context_processors.csrf',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.comments',
    'django_extensions',
    'django.contrib.sites',
    'loupe',
    'imagekit',
    'notification',
    'registration',
    'registration_defaults',

    'tastypie',
)


# Loupe Settings for images
LOUPE_RESIZE_THUMB_WIDTH = 100 # Width in pixels of the thumbnail
LOUPE_RESIZE_THUMB_HEIGHT  = 75 # Height in pixels of the thumbnail
LOUPE_RESIZE_THUMB_CROP = True # Crop thubmnails? True or False
LOUPE_RESIZE_DISPLAY_WIDTH = 800 # Width in pixels of the display size (not full size image)
LOUPE_PRE_CACHE_IMAGES = True # Pre-cache images on upload? True or False
LOUPE_INCREMENT_COUNT = True # Increment the view count on images? True or False

LOGIN_REDIRECT_URL = "/"

ACCOUNT_ACTIVATION_DAYS = 7

try:
    from local_settings import *
except:
    pass
