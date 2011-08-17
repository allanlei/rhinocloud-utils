from django.core.exceptions import ImproperlyConfigured

import gdata.docs.service
import gdata.spreadsheet.service
import gdata.auth


class BaseGoogleUploadMixin(object):
    oauth_consumer_key = None
    oauth_consumer_secret = None
    oauth_scopes = None
    gdata_service_class = None
    gdata_signature_method = gdata.auth.OAuthSignatureMethod.HMAC_SHA1

    def get_oauth_consumer_key(self):
        if self.oauth_consumer_key:
            token = self.oauth_consumer_key
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_key.')
        return token

    def get_oauth_consumer_secret(self):
        if self.oauth_consumer_secret:
            token = self.oauth_consumer_secret
        else:
            raise ImproperlyConfigured('Provide oauth_consumer_secret.')
        return token

    def get_oauth_scopes(self):
        if self.oauth_scopes:
            scopes = self.oauth_scopes
        else:
            raise ImproperlyConfigured('Provide oauth_scopes.')
        return scopes

    def get_oauth_access_token_string(self):
        raise NotImplementedError('Override with access to access_token_string returning (key, secret) tuple')
        
    def get_oauth_access_token(self, oauth_input_params=None):
        access_token_key, access_token_secret = self.get_oauth_access_token_string()
        token = gdata.auth.OAuthToken(
            key=access_token_key,
            secret=access_token_secret,
            scopes=self.get_oauth_scopes(), 
            oauth_input_params=oauth_input_params,
        )
        return token

    def get_gdata_signature_method(self):
        if self.gdata_signature_method:
            signature_method = self.gdata_signature_method
        else:
            raise ImproperlyConfigured('Provide service_class or override get_service_class().')
        return signature_method

    def get_gdata_service_class(self):
        if self.gdata_service_class:
            service = self.gdata_service_class
        else:
            raise ImproperlyConfigured('Provide service_class or override get_service_class().')
        return service

    def get_gdata_service_kwargs(self):
        return {
#            'signature_method': self.get_gdata_signature_method(),
#            'consumer_key': self.get_oauth_consumer_key(),
#            'consumer_secret': self.get_oauth_consumer_secret(),
        }
    
    def get_gdata_content_type(self, extension):
        raise NotImplementedError()
        
    def get_gdata_service(self):
        service = self.get_gdata_service_class()(**self.get_gdata_service_kwargs())
        service.SetOAuthInputParameters(
            self.get_gdata_signature_method(), 
            self.get_oauth_consumer_key(), 
            consumer_secret=self.get_oauth_consumer_secret()
        )
        return service

    def get_filename(self):
        if self.filename:
            name = self.filename
        else:
            raise NotImplementedError('Provide filename')
        return name
    
    def get_gdata_media_source_kwargs(self):
        return {
            'file_name': self.get_filename(),
            'content_type': self.get_gdata_content_type(),
        }
        
    def get_gdata_media_source(self, content=None):
        kwargs = self.get_gdata_media_source_kwargs()
        if content:
            kwargs.update({
                'file_handle': content,
                'content_length': len(content),
            })
        return gdata.MediaSource(**kwargs)
        
    def upload(self, fileObject):
        service = self.get_gdata_service()
        token = self.get_oauth_access_token(
            oauth_input_params=service.GetOAuthInputParameters()
        )
        service.SetOAuthToken(token)

        gdata_ms = self.get_gdata_media_source(content=fileObject)
        entry = service.Upload(gdata_ms, self.get_filename())
        if not entry:
            raise Exception('There was a problem uploading to Google')
        return entry

class GoogleDocsUploadMixin(BaseGoogleUploadMixin):
    gdata_service_class = gdata.docs.service.DocsService
    
    def get_gdata_content_type(self):
        extension = self.get_filename().split('.')[-1].upper()
        return gdata.docs.service.SUPPORTED_FILETYPES[extension]
