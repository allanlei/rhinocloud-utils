from django.core import serializers
from django.http import HttpResponse
from django.utils import simplejson as json

class JSONResponseMixin(object):
    def render_to_response(self, context, **kwargs):
        if self.is_json_request():
            return self.get_json_response(self.convert_context_to_json(context))
        return super(JSONResponseMixin, self).render_to_response(context, **kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        return json.dumps(context)

    def is_json_request(self):
        return self.request.is_ajax() and 'application/json' in self.request.META['HTTP_ACCEPT']


class QuerysetJSONResponseMixin(JSONResponseMixin):
    serialize_fields = ()
    serialize_relations = ()
    serialize_extras = ()
    
    def get_serialize_fields(self):
        return self.serialize_fields
    
    def get_serialize_relations(self):
        return self.serialize_relations
    
    def get_serialize_extras(self):
        return self.serialize_extras
        
    def render_to_response(self, context, serializer_kwargs={}, **kwargs):
        return self.get_json_response(self.convert_to_json(self.get_queryset(), **serializer_kwargs), **kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        return HttpResponse(content, content_type='application/json', **httpresponse_kwargs)
    
    def convert_to_json(self, queryset, **kwargs):
        kwargs.update({
            'relations': self.get_serialize_relations(),
            'extras': self.get_serialize_extras(),
            'fields': self.get_serialize_fields(),
        })
        return serializers.serialize('json', queryset, **kwargs)
