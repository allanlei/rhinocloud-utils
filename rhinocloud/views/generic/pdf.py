from django.views import generic
from rhinocloud.template import PDFTemplateResponse



class PDFView(generic.base.TemplateView):
    response_class = PDFTemplateResponse
    
    def get_pdf_kwargs(self):
        return {
            'encoding': 'UTF-8',
        }
        
    def render_to_response(self, context, content_type='application/pdf', **kwargs):
        return super(PDFView, self).render_to_response(
            context, 
            content_type=content_type, 
            pdf_kwargs=self.get_pdf_kwargs(), 
            **kwargs)
