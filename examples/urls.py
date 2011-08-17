from django.conf.urls.defaults import *
from django.views import generic

from views import *


urlpatterns = patterns('',
    url(r'^pdf/test/$', PDFView.as_view()),
    url(r'^pdf/test/webkit/$', WebkitPDFView.as_view()),
    url(r'^openoffice/spreadsheet\.ods$', OpenOfficeView.as_view()),
    
    
    url(r'^admin/$', include('rhinocloud.contrib.administration.urls')),
)
