from django.conf.urls import patterns, url

from lookouts.views import DetailLookout, CreateLookout, DeleteLookout

urlpatterns = patterns('',

    url(r'^new/$',
        CreateLookout.as_view(), name='create_lookout'),

    url(r'^(?P<slug>[\w-]+)/$',
        DetailLookout.as_view(), name='detail_lookout'),

    url(r'^(?P<slug>[\w-]+)/delete/$',
        DeleteLookout.as_view(), name='delete_lookout'),
)
