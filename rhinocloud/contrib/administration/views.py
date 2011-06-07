from django.views import generic
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.contrib.auth.models import User, Group
from django.core import serializers


from rhinocloud.views.mixins.json import JSONQuerysetResponseMixin
from rhinocloud.contrib.jquery.views import DataTablesServerDataMixin


class UserMixin(object):
    model = User
    
class ListView(DataTablesServerDataMixin, UserMixin, JSONQuerysetResponseMixin, generic.list.ListView):
    searchable_fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser',)
    serialize_fields = tuple(searchable_fields)
    
    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        if self.request.is_ajax():
            iDisplayStart = int(self.request.GET.get('iDisplayStart', 0))
            iDisplayLength = int(self.request.GET.get('iDisplayLength', 10))
            iDisplayEnd = iDisplayStart + iDisplayLength if iDisplayLength != -1 else None
            
            context = {
                'iTotalRecords': self.object_list.count(),
                'iTotalDisplayRecords': self.object_list.exclude().count(),
                'sEcho': int(self.request.GET['sEcho']),
                'aaData': json.loads(JSONQuerysetResponseMixin.convert_to_json(self, self.object_list[iDisplayStart:iDisplayEnd])),
            }
        return context
        
    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            return HttpResponse(json.dumps(context), mimetype='application/json')
        return generic.list.ListView.render_to_response(self, context, **kwargs)

class DetailView(UserMixin, generic.detail.DetailView):
    pass
    
class CreateView(UserMixin, generic.edit.CreateView):
    pass

class UpdateView(UserMixin, generic.edit.UpdateView):
    pass

class DeleteView(generic.edit.DeleteView):
    pass

class DownloadView(UserMixin, generic.list.ListView):
    def render_to_response(self, context, **kwargs):
        emails = [user['email'] for user in self.object_list.order_by('pk').values('email')]
        response = HttpResponse(',\n'.join(emails), mimetype='text/plain')
        response['Content-Disposition'] = 'attachment;'
        return response
