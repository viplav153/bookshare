# core django imports
from django.conf.urls import url
from django.views.decorators.cache import cache_page
# imports from your apps
from .views import DetailStudent, StudentRatings, UpdateStudent

urlpatterns = [
    url(r'^name-change/$',
        UpdateStudent.as_view(), name='name_change'),

    url(r'^(?P<slug>[\w-]+)/$',
        cache_page(6)(DetailStudent.as_view()), name='profile'),

    url(r'^(?P<slug>[\w-]+)/ratings/$',
        cache_page(6)(StudentRatings.as_view()), name='ratings'),
]
