from django.contrib import admin
from django.db.models import get_model

admin.site.register(get_model('loupe', 'project'))
admin.site.register(get_model('loupe', 'image'))
admin.site.register(get_model('loupe', 'corkboard'))
admin.site.register(get_model('loupe', 'note'))
