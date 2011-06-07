from django.conf.urls.defaults import *
from django.views import generic

import views

item_patterns = ('',
#    url(r'^detail/$', views.DetailView.as_view(), name='detail'),
#    url(r'^update/$', views.UpdateView.as_view(), name='update'),
#    url(r'^delete/$', views.DeleteView.as_view(), name='delete'),
)

download_patterns = ('',
#    url(r'^mail_list/$', views.DownloadView.as_view(), name='mailing_list'),
)

urlpatterns = patterns('',
    url(r'^$', views.ListView.as_view(), name='list'),
    url(r'^mail_list.txt$', views.DownloadView.as_view(), name='mailing_list'),
#    url(r'^create/$', views.CreateView.as_view(), name='create'),
#    url(r'^(?P<pk>\d+)/', include(item_patterns)),
)
