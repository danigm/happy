from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('happyapp.views',
    url(r'^ad/?$', 'advise', name='advise'),
    url(r'^why/(\d+)$', 'why', name='why'),
    url(r'^vote/(\d+)$', 'vote', name='vote'),
    url(r'^good/for/you/$', 'good_for_you', name='good_for_you'),
    url(r'^$', 'index', name='index'),
)
