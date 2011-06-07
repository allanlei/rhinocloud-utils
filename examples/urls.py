from django.conf.urls.defaults import *
from django.views import generic

from views import *


urlpatterns = patterns('',
     url(r'^pdf/1/$', ExamplePDFView.as_view()),
     url(r'^openoffice/spreadsheet\.ods$', ExampleOpenOfficeView.as_view()),
     url(r'^admin/$', include('rhinocloud.contrib.administration.urls')),
)
