from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse


urlpatterns = patterns('loupe.views',
    url (r'^$', 
        view='dashboard',
        name='dashboard',
    ),

    url (r'^project/(?P<slug>[-_\w]+)/$', 
        view='project_detail',
        name='project_detail',
    ),

    url (r'^image/(\d+)/$', 
        view='image_detail',
        name='image_detail',
    ),

    url (r'^corkboard/(?P<slug>[-_\w]+)/$', 
        view='corkboard_detail',
        name='corkboard_detail',
    ),

    url(r'^corkboard/destroy/(\d+)/$',
        view='corkboard_destroy',
        name='corkboard_destroy'
    ),

    url(r'^image/destroy/(\d+)/$',
        view='image_destroy',
        name='image_destroy'
    ),
                       
    (r'^comments/', include('django.contrib.comments.urls')),
)
