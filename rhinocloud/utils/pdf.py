from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

import PDF

class PDFRenderError(Exception):
    pass

def convert_to_pdf(html, **kwargs):
    print 'rhinocloud.utils.pdf.convert_to_pdf() is deprecated! Please use rhinocloud.utils.PDF.render()'
    return PDF.render(html.encode('UTF-8'))

def render_to_pdf_response(html):
    print 'rhinocloud.utils.pdf.render_to_pdf_response() is deprecated! Please remove'
    return HttpResponse(convert_to_pdf(html), mimetype='application/pdf')

def render_to_string(template_name, context={}):
    print 'rhinocloud.utils.pdf.render_to_string() is deprecated! Please remove'
    template = get_template(template_src)
    html  = template.render(Context(context_dict))
    return convert_to_pdf(html)
    
    

