from rhinocloud.views.generic import pdf, openoffice

import datetime

class ExamplePDFView(pdf.PDFView):
    template_name = 'pdf.html'
    
    def get_context_data(self, **kwargs):
        context = super(ExamplePDFView, self).get_context_data()
        context.update({
            'content': 'sdfsdfsdf',
        })
        return context



class ExampleOpenOfficeView(openoffice.SpreadsheetView):
    template_name = 'FundTemplate.ods'
    
    def get_context_data(self, **kwargs):
        context = super(ExampleOpenOfficeView, self).get_context_data(**kwargs)
        context.update({
            'timestamp': datetime.datetime.now(),
        })
        return context
