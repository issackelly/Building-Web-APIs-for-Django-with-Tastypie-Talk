from django.conf.urls.defaults import url, patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from loupe.api import UserResource, ProjectResource, CorkboardResource, NoteResource, ImageResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(ProjectResource())
v1_api.register(CorkboardResource())
v1_api.register(NoteResource())
v1_api.register(ImageResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1_api.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^notices/', include('notification.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('loupe.urls')),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    (r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
)
