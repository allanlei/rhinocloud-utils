from django.db import models

from rhinocloud.db.models import managers

import gdata.auth



class OAuthMixin(object):
    def __init__(self, service_class, signature_method=gdata.auth.OAuthSignatureMethod.HMAC_SHA1,oauth_consumer_key=None, oauth_consumer_secret=None, oauth_scopes=None, *args, **kwargs):
        super(OAuthMixin, self).__init__(*args, **kwargs)
        self.oauth_scopes = oauth_scopes
        self.service = service_class()
        self.service.SetOAuthInputParameters(
            signature_method,
            oauth_consumer_key,
            consumer_secret=oauth_consumer_secret,
        )
        
    def get_access_token(self, access_token=None, access_token_key=None, access_token_secret=None):
        if access_token is None and (access_token_key is None or access_token_secret is None):
            raise Exception('Requires access_token')
        return gdata.auth.OAuthToken(
            key=access_token_key,
            secret=access_token_secret,
            scopes=self.oauth_scopes, 
            oauth_input_params=self.service.GetOAuthInputParameters(),
        )




class ResourceQueryset(models.query.QuerySet):
    pass
#    def trash(self):
#        for resource in self.all():
#            print 'DELETE', resource
#            self.service.Delete(resource.get_delete_url())

    
class ResourceManager(OAuthMixin, managers.CustomQuerysetManager):
    queryset_class = ResourceQueryset

    def upload(self, content, content_type=None, filename=None, access_token_key=None, access_token_secret=None):
        self.service.SetOAuthToken(self.get_access_token(
            access_token_key=access_token_key, 
            access_token_secret=access_token_secret
        ))
        ms = gdata.MediaSource(
            file_name=filename, 
            file_handle=content,
            content_length=len(content),
            content_type=content_type,
        )
        entry = self.service.Upload(ms, filename)
        
        if not entry:
            raise Exception('There was a problem uploading to Google')

        return self.create(
            resource_id = entry.resourceId.text,
            title = entry.title.text,
            category = entry.GetDocumentType(),
            content_type = entry.content.type,
            
            alternate_url = entry.GetAlternateLink().href,
            download_url = entry.content.src,
            edit_url = entry.GetEditLink().href,
            edit_media_url = entry.GetEditMediaLink().href,
        ), entry
