# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Resource'
        db.create_table('google_resource', (
            ('resource_id', self.gf('django.db.models.fields.CharField')(max_length=128, primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('alternate_url', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
            ('download_url', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
            ('edit_url', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
            ('edit_media_url', self.gf('django.db.models.fields.URLField')(max_length=512, blank=True)),
        ))
        db.send_create_signal('google', ['Resource'])


    def backwards(self, orm):
        
        # Deleting model 'Resource'
        db.delete_table('google_resource')


    models = {
        'google.resource': {
            'Meta': {'object_name': 'Resource'},
            'alternate_url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'download_url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'edit_media_url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'edit_url': ('django.db.models.fields.URLField', [], {'max_length': '512', 'blank': 'True'}),
            'resource_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['google']
