from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
     url(r'^pdf/1/$', ExamplePDFView.as_view()),
)
