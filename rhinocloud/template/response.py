from django.template.response import TemplateResponse
from django.template import loader

from rhinocloud.utils.pdf import convert_to_pdf
from rhinocloud.template import openoffice

class PDFTemplateResponse(TemplateResponse):
    def __init__(self, pdf_kwargs={}, *args, **kwargs):
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        self.pdf_kwargs = pdf_kwargs
        
    @property
    def rendered_content(self):
        rendered_template = super(PDFTemplateResponse, self).rendered_content
        return convert_to_pdf(rendered_template, **self.pdf_kwargs)


class OpenOfficeTemplateResponse(TemplateResponse):
    pass
