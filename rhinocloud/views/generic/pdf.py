from django.views import generic
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.template import loader
from django.core.servers.basehttp import FileWrapper

from rhinocloud.template.response import PDFTemplateResponse, WebkitPDFTemplateResponse


class PDFResponseMixin(object):
    response_class = PDFTemplateResponse
    
    def get_pdf_kwargs(self):
        return {
            'encoding': 'UTF-8',
        }
        
    def render_to_response(self, context, content_type='application/pdf', **kwargs):
        return super(PDFResponseMixin, self).render_to_response(
            context, 
            content_type=content_type, 
            pdf_kwargs=self.get_pdf_kwargs(), 
            **kwargs)

class PDFView(PDFResponseMixin, generic.base.TemplateView):
    pass
    
    
class WebkitPDFResponseMixin(object):
    response_class = WebkitPDFTemplateResponse
    pdf_css_file = None
    pdf_title = None
    
    def get_pdf_css_file(self):
        return self.pdf_css_file

    def get_pdf_title(self):
        return self.pdf_title
        
    def get_pdf_kwargs(self):
        kwargs = {
            'encoding': 'UTF-8',
            'quiet': '',
        }
        
        if self.get_pdf_css_file():
            kwargs.update({
                'user-style-sheet': self.get_pdf_css_file(),
            })
            
        if self.get_pdf_title():
            kwargs.update({
                'title': self.get_pdf_title(),
            })
        return kwargs
        
    def render_to_response(self, context, content_type='application/pdf', **kwargs):
        return super(WebkitPDFResponseMixin, self).render_to_response(
            context, 
            content_type=content_type, 
            pdf_kwargs=self.get_pdf_kwargs(), 
            **kwargs)

class WebkitPDFView(WebkitPDFResponseMixin, generic.base.TemplateView):
    pass
