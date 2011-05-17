from django.views import generic
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured

from rhinocloud.template.response import OpenOfficeTemplateResponse


class OpenOfficeDocumentView(generic.base.TemplateView):
    pass

class SpreadsheetView(OpenOfficeDocumentView):
    response_class = OpenOfficeTemplateResponse
    content_type = 'application/vnd.oasis.opendocument.spreadsheet'
    
    def get_content_type(self):
        if self.content_type:
            content_type = self.content_type
        else:
            raise ImproperlyConfigured('Provide content_type or override get_content_type().')
        return content_type
        
    def render_to_response(self, context, **kwargs):
        return super(SpreadsheetView, self).render_to_response(
            context, 
            content_type=self.get_content_type(), 
            **kwargs)
