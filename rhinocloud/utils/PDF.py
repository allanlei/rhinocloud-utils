import ho.pisa as pisa
import cgi

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class PDF(object):
    @classmethod
    def render(cls, html, encoding='UTF-8'):
        result = StringIO()
        pdf = pisa.CreatePDF(StringIO(html.encode(encoding)), result, **kwargs)
        if not pdf.err:
            return result.getvalue()
        raise Exception(pdf.err)
