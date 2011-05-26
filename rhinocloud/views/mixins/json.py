from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)

    def is_json_request(self):
        return self.request.is_ajax() and 'application/json' in self.request.META['HTTP_ACCEPT']


class JSONQuerysetResponseMixin(object):
    serialize_fields = None
    serialize_relations = None
    serialize_extras = None
    serialize_excludes = None
    
    def get_serialize_fields(self):
        if self.serialize_fields:
            fields = self.serialize_fields
        else:
            fields = ()
#            raise ImproperlyConfigured('Provide serialize_fields or override get_serialize_fields().')
        return fields
    
    def get_serialize_relations(self):
        if self.serialize_relations:
            relations = self.serialize_relations
        else:
            relations = ()
#            raise ImproperlyConfigured('Provide serialize_relations or override get_serialize_relations().')
        return relations
    
    def get_serialize_extras(self):
        if self.serialize_extras:
            extras = self.serialize_extras
        else:
            extras = ()
#            raise ImproperlyConfigured('Provide serialize_extras or override get_serialize_extras().')
        return extras
    
    def get_serialize_excludes(self):
        if self.serialize_excludes:
            fields = self.serialize_excludes
        else:
            fields = ()
        return fields
        
    def render_to_response(self, context, serializer_kwargs={}, **kwargs):
        return self.get_json_response(self.convert_to_json(self.get_queryset(), **serializer_kwargs), **kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)
    
    def convert_to_json(self, queryset, **kwargs):  
        kwargs.update({
            'relations': self.get_serialize_relations(),
            'extras': self.get_serialize_extras(),
            'fields': self.get_serialize_fields(),
            'excludes': self.get_serialize_excludes(),
        })
        return serializers.serialize('json', queryset, **kwargs)
