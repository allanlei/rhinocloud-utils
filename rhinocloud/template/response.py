from django.template.response import TemplateResponse

from rhinocloud.utils.pdf import convert_to_pdf

class PDFTemplateResponse(TemplateResponse):
    def __init__(self, pdf_kwargs={}, *args, **kwargs):
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        self.pdf_kwargs = pdf_kwargs
        
    @property
    def rendered_content(self):
        rendered_template = super(PDFTemplateResponse, self).rendered_content
        return convert_to_pdf(rendered_template, **self.pdf_kwargs)
