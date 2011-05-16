from django.http import HttpResponse
import ho.pisa as pisa
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import cgi


class PDFRenderError(Exception):
    pass

def convert_to_pdf(rendered_template, **kwargs):
    result = StringIO()
    pdf = pisa.CreatePDF(StringIO(rendered_template.encode('UTF-8')), result, **kwargs)
    if not pdf.err:
        return result.getvalue()
    raise PDFRenderError()

def render_to_pdf_response(rendered_template):
    return HttpResponse(convert_to_pdf(rendered_template), mimetype='application/pdf')
