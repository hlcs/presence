'''
    Url resolver di django (non ha altri urls.py nelle altre apps)
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin



admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'presence.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url per l' accesso all' area di amministrazione
    url(r'^admin', include(admin.site.urls)),

    # url per l' accesso all' area di login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    # url per l' accesso all' area di logout
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    # url della pagina di informazioni
    url(r'^about/$', 'hlcs.views.about', name='about'),

    # url di default (va alla homepage)
    url(r'^$', 'hlcs.views.homepage', name='home'),
)
