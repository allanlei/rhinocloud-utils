from django.template.response import TemplateResponse
from django.template import loader

from rhinocloud.utils.pdf import convert_to_pdf
from rhinocloud.template import openoffice

from subprocess import Popen, PIPE

class PDFTemplateResponse(TemplateResponse):
    def __init__(self, pdf_kwargs={}, *args, **kwargs):
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        self.pdf_kwargs = pdf_kwargs
        
    @property
    def rendered_content(self):
        rendered_template = super(PDFTemplateResponse, self).rendered_content
        return convert_to_pdf(rendered_template, **self.pdf_kwargs)


class WebkitPDFTemplateResponse(TemplateResponse):
    def __init__(self, pdf_kwargs={}, *args, **kwargs):
        super(WebkitPDFTemplateResponse, self).__init__(*args, **kwargs)
        self.pdf_kwargs = pdf_kwargs
    
    def get_pdf_kwargs_string(self):
        return ' '.join([' '.join('--%s %s'.split(' ')) % (key, value) for key, value in self.pdf_kwargs.items()])
        
    @property
    def rendered_content(self):
        rendered_template = super(WebkitPDFTemplateResponse, self).rendered_content
        p = Popen('wkhtmltopdf - - %s' % self.get_pdf_kwargs_string(), shell=True, stdin=PIPE, stdout=PIPE)
        return p.communicate(rendered_template)[0]
        
class OpenOfficeTemplateResponse(TemplateResponse):
    pass
