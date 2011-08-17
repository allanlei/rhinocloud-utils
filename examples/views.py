from django.views import generic

from rhinocloud.views.generic import pdf, openoffice
from rhinocloud.views.generic.pdf import PDFResponseMixin, WebkitPDFResponseMixin

import datetime


class OpenOfficeView(openoffice.SpreadsheetView):
    template_name = 'FundTemplate.ods'
    
    def get_context_data(self, **kwargs):
        context = super(OpenOfficeView, self).get_context_data(**kwargs)
        context.update({
            'timestamp': datetime.datetime.now(),
        })
        return context

class PDFView(PDFResponseMixin, generic.base.TemplateView):
    template_name = 'pdf.html'
    
    def get_context_data(self, **kwargs):
        context = super(PDFView, self).get_context_data(**kwargs)
        context.update({
            'timestamp': datetime.datetime.now(),
        })
        return context

class WebkitPDFView(WebkitPDFResponseMixin, generic.base.TemplateView):
    template_name = 'pdf.html'
    
    def get_context_data(self, **kwargs):
        context = super(WebkitPDFView, self).get_context_data(**kwargs)
        context.update({
            'timestamp': datetime.datetime.now(),
        })
        return context
