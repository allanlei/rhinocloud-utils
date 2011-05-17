from django.template import Template

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import zipfile


class OpenOfficeTemplate(Template):
    def __init__(self, *args, **kwargs):
        filepath = kwargs.pop('filepath', None)
        super(OpenOfficeTemplate, self).__init__(*args, **kwargs)
        self.filepath = filepath

    def render(self, *args, **kwargs):
        content = super(OpenOfficeTemplate, self).render(*args, **kwargs)
        file_out = StringIO()
        zin = zipfile.ZipFile(self.filepath, 'r')
        zout = zipfile.ZipFile(file_out, 'w', zipfile.ZIP_DEFLATED)
        for item in zin.infolist():
            if item.filename not in ['content.xml']:
                zout.writestr(item.filename, zin.read(item.filename))
        zout.writestr('content.xml', content)
        zout.close()
        zin.close()
        return file_out.getvalue()
