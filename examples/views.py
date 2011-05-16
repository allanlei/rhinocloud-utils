from rhinocloud.views import generic


class ExamplePDFView(generic.pdf.PDFView):
    template_name = 'pdf.html'
    
    def get_context_data(self, **kwargs):
        context = super(ExamplePDFView, self).get_context_data()
        context.update({
            'content': 'sdfsdfsdf',
        })
        return context
