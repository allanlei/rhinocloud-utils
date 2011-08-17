from django.core.exceptions import ImproperlyConfigured

import gdata.docs.service
import gdata.spreadsheet.service
import gdata.auth


class GoogleUploader(object):
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
        
    def get_oauth_access_token(self, access_token=None, access_token_key=None, access_token_secret=None, oauth_input_params=None):
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
        return {}
        
    def get_gdata_service(self):
        service = self.get_gdata_service_class()(**self.get_gdata_service_kwargs())
        service.SetOAuthInputParameters(
            self.get_gdata_signature_method(), 
            self.get_oauth_consumer_key(), 
            consumer_secret=self.get_oauth_consumer_secret()
        )
        return service
        
    def upload(self, access_token_key=None, access_token_secret=None, filename=None, **kwargs):
        service = self.get_gdata_service()
        token = self.get_oauth_access_token(
            access_token_key=access_token_key,
            access_token_secret=access_token_secret,
            oauth_input_params=service.GetOAuthInputParameters()
        )
        service.SetOAuthToken(token)

        gdata_ms = self.gdata.MediaSource(file_name=filename, **kwargs)
        entry = service.Upload(gdata_ms, filename)
        if not entry:
            raise Exception('There was a problem uploading to Google')
        return entry

class GoogleDocsUploader(GoogleUploader):
    gdata_service_class = gdata.docs.service.DocsService
