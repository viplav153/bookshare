# core django imports
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
# third party imports
from haystack.views import SearchView
from cas.views import login, logout
# imports from your apps
from .views import HomepageView, ChartsView
from trades.forms import ListingSearchForm


admin.autodiscover()

handle403 = TemplateView.as_view(template_name="403.html")
handle404 = TemplateView.as_view(template_name="404.html")
handle500 = TemplateView.as_view(template_name="500.html")

urlpatterns = [
    # app-level urls
    url(r'^share/', include('trades.urls')),
    url(r'^student/', include('core.urls')),
    url(r'^lookouts/', include('lookouts.urls')),
    url(r'^mod/', include('mod.urls')),

    # search
    url(r'^search/', login_required(SearchView(form_class=ListingSearchForm),
                                    login_url='login'), name='search'),

    # site-wide pages
    # homepage is weird for cacheing... no special url, but different content
    # for each user
    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^charts/?$', ChartsView.as_view(), name='charts'),

    # static pages
    url(r'^about/?$',
        cache_page(60 * 15)(TemplateView.as_view(template_name='about.html')),
        name='about'),
    url(r'^privacy/?$',
        cache_page(60 * 15)(TemplateView.as_view(template_name='privacy.html')),
        name='privacy'),

    # user authentication
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),

    # admin pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # api
    url(r'^api/v1/', include('api.urls')),
    # establishing versioning already so we easily can move to another API release
    # without specific version redirects to latest version
    url(r'^api/$', RedirectView.as_view(url="v1/")),

    # location of user-uploaded media files from settings.py (for local)
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
