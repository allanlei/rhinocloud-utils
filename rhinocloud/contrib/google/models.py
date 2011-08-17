from django.db import models
from django.conf import settings
from django.http import Http404

import managers

import gdata.docs.service
import gdata.auth



class Resource(models.Model):
    resource_id = models.CharField(max_length=128, primary_key=True)
    category = models.CharField(max_length=32)
    title = models.CharField(max_length=128)
    content_type = models.CharField(max_length=64)
    
    alternate_url = models.URLField(max_length=512, verify_exists=False, blank=True)
    download_url = models.URLField(max_length=512, verify_exists=False, blank=True)
    edit_url = models.URLField(max_length=512, verify_exists=False, blank=True)
    edit_media_url = models.URLField(max_length=512, verify_exists=False, blank=True)
    
    objects = models.Manager()
    docs = managers.ResourceManager(
        gdata.docs.service.DocsService,
        oauth_consumer_key=settings.OAUTH_CONSUMER_KEY,
        oauth_consumer_secret=settings.OAUTH_CONSUMER_SECRET,
        oauth_scopes=settings.OAUTH_SCOPES,
    )

    def delete(self, access_token_key=None, access_token_secret=None):
        if self.pk is None:
            raise Exception('Cannot update resource without resource_id')
        
#        ms = gdata.MediaSource(
#            file_name=self.title, 
#            file_handle=content,
#            content_length=len(content),
#            content_type=self.content_type,
#        )
        service = self.__class__.docs.service
        service.SetOAuthToken(gdata.auth.OAuthToken(
            key=access_token_key,
            secret=access_token_secret,
            scopes=self.__class__.docs.oauth_scopes, 
            oauth_input_params=service.GetOAuthInputParameters(),
        ))
        service.Delete(self.get_delete_url())
        
    def update(self, content, access_token_key=None, access_token_secret=None, new_revision=True):
        if self.pk is None:
            raise Exception('Cannot update resource without resource_id')
            
        ms = gdata.MediaSource(
            file_name=self.title, 
            file_handle=content,
            content_length=len(content),
            content_type=self.content_type,
        )
        service = self.__class__.docs.service
        service.SetOAuthToken(gdata.auth.OAuthToken(
            key=access_token_key,
            secret=access_token_secret,
            scopes=self.__class__.docs.oauth_scopes, 
            oauth_input_params=service.GetOAuthInputParameters(),
        ))
        url_params = {
            'new-revision': new_revision and 'true' or 'false',
        }
        service.Put(None, self.get_edit_media_url(), media_source=ms, url_params=url_params, extra_headers={'GData-Version': 3, 'If-Match': '*'})

    def get_absolute_url(self):
        return self.alternate_url
    
    def get_edit_url(self):
        return self.edit_url

    def get_edit_media_url(self):
        return self.edit_media_url.replace('%3A', ':')
        
    def get_delete_url(self):
        return self.edit_url
        
    def get_download_url(self):
        return self.download_url.replace('gd=true', '')

    def __unicode__(self):
        return '%s(%s)' % (self.title, self.resource_id)
