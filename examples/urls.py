from django.conf.urls.defaults import patterns, include, url
from views import *

urlpatterns = patterns('',
     url(r'^pdf/1/$', ExamplePDFView.as_view()),
     url(r'^openoffice/spreadsheet\.ods$', ExampleOpenOfficeView.as_view()),
)
