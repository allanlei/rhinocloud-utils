from django.views import generic
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured

from rhinocloud.template.response import OpenOfficeTemplateResponse


class OpenOfficeDocumentView(generic.base.TemplateView):
    content_type = None
    
    def get_content_type(self):
        if self.content_type:
            content_type = self.content_type
        else:
            raise ImproperlyConfigured('Provide content_type or override get_content_type().')
        return content_type

class SpreadsheetView(OpenOfficeDocumentView):
    response_class = OpenOfficeTemplateResponse
    content_type = 'application/vnd.oasis.opendocument.spreadsheet'
        
    def render_to_response(self, context, **kwargs):
        return super(SpreadsheetView, self).render_to_response(
            context, 
            content_type=self.get_content_type(), 
            **kwargs)





#from pyoo.documents import OOSpreadSheet
#from django.template import Context, Template
#import sys
#import re
#import os.path
#import getopt
#import getpass
#import gdata.docs.service
#import gdata.spreadsheet.service
#import tempfile




#from django.core.exceptions import ImproperlyConfigured
#from auth.oauth.views import OAuthMixin
#from django.http import HttpResponseRedirect


#class GoogleTemplateResponseMixin(OAuthMixin):
#    service_class = None
#    title = None
#    
#    def get_service_class(self):
#        if self.service_class:
#            service = self.service_class
#        else:
#            raise ImproperlyConfigured('Provide service_class or override get_service_class().')
#        return service
#    
#    def get_oauth_access_token(self):
#        raise ImproperlyConfigured('Override get_oauth_access_token().')

#    def get_title(self):
#        if self.title:
#            title = self.title
#        else:
#            raise ImproperlyConfigured('Provide title or override get_title().')
#        return title
#    
#    def get_template_name(self):
#        if self.template_name:
#            template_name = self.template_name
#        else:
#            raise ImproperlyConfigured('Provide template_name or override get_template_names().')
#        return template_name
#       
#    def render_template(self, context, filename):
#        oo = OOSpreadSheet.copy(self.get_template_name(), filename)
#        t = Template(oo.content)
#        rendered = t.render(Context(context))
#        oo.content = rendered
#        oo.close()
#        
#    def upload_document(self, filename):
#        service_class = self.get_service_class()
#        service = service_class()
#        service.SetOAuthInputParameters(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, self.get_oauth_consumer_key(), consumer_secret=self.get_oauth_secret_key())
#        token = gdata.auth.OAuthToken(
#            scopes=self.get_oauth_scopes(), 
#            oauth_input_params=service.GetOAuthInputParameters(),
#        )
#        token.set_token_string(self.get_oauth_access_token())
#        service.SetOAuthToken(token)
#        
#        file_name = os.path.basename(filename)
#        ext = file_name.split('.')[-1].upper()
#        content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
#        ms = gdata.MediaSource(file_path=filename, content_type=content_type)
#        
#        
#        ms = gdata.MediaSource(file_handle=None, content_type=None, content_length=None, )
#       
#        ms.file_name = 'JSELJLSJT'
#        entry = service.Upload(ms, self.get_title())
#        if not entry:
#            raise Exception('There was a problem uploading to Google')
#        return entry.content.src
#        
#    def render_to_response(self, context):
#        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ods')
#        self.render_template(context, temp_file.name)
#        temp_file.close()
#        url = self.upload_document(temp_file.name)
#        return HttpResponseRedirect(url)






#class GoogleSpreadSheetMixin(object):
#    def render_to_response(self, context):
#        title = context.get('title', '')
#        if len(self.get_template_names()):
#            template_name = self.get_template_names()[0]
#        else:
#            raise Exception('No template found')
#        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ods')
#        oo = OOSpreadSheet.copy(template_name, temp_file.name)
#        t = Template(oo.content)
#        rendered = t.render(Context(context))
#        oo.content = rendered
#        oo.close()
#        temp_file.close()
#        print temp_file.name
#        
#        gd_client = gdata.docs.service.DocsService()
#        gd_client.ClientLogin(USERNAME, PASSWORD, source='Test Upload')
#    
#        
#        file_path = temp_file.name
#        if not file_path:
#            return
#        elif not os.path.isfile(file_path):
#            print 'Not a valid file.'
#            return
#        file_name = os.path.basename(file_path)
#        ext = self._GetFileExtension(file_name)

#        if not ext or ext not in gdata.docs.service.SUPPORTED_FILETYPES:
#            print 'File type not supported. Check the file extension.'
#            return
#        else:
#            content_type = gdata.docs.service.SUPPORTED_FILETYPES[ext]
#        
#        
#        try:
#            ms = gdata.MediaSource(file_path=file_path, content_type=content_type)
#        except IOError:
#            print 'Problems reading file. Check permissions.'
#            return
#        if ext in ['CSV', 'ODS', 'XLS', 'XLSX']:
#            print 'Uploading spreadsheet...'
#        elif ext in ['PPT', 'PPS']:
#            print 'Uploading presentation...'
#        else:
#            print 'Uploading word processor document...'
#        entry = gd_client.Upload(ms, title)
#        if entry:
#            print 'Upload successful!'
#            print 'Document now accessible at:', entry.GetAlternateLink().href
#            return HttpResponseRedirect(entry.content.src)
#        else:
#            print 'Upload error.'
#            
#            
#    def _GetFileExtension(self, file_name):
#        match = re.search('.*\.([a-zA-Z]{3,}$)', file_name)
#        if match:
#          return match.group(1).upper()
#        return False
