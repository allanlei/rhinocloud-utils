from django.views import generic
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.contrib.auth.models import User, Group
from django.core import serializers

#from rhinocloud.views.mixins.json import JSONQuerysetResponseMixin
#from rhinocloud.contrib.jquery.views import DataTablesServerDataMixin
from rhinocloud.contrib.datatables.views.generic.mixins import ServerSideProcessingMixin

class UserMixin(object):
    model = User
    
class ListView(UserMixin, ServerSideProcessingMixin, generic.list.ListView):
    template_name = 'administration/user_list.html'
    searchable_fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_superuser',)
    serialize_fields = tuple(searchable_fields)
    
    def get_packaged_data(self, queryset):
        iDisplayStart = self.get_iDisplayStart()
        iDisplayLength = self.get_iDisplayLength()
        return {
            'iTotalRecords': self.get_queryset().count(),
            'iTotalDisplayRecords': queryset.count(),
            'sEcho': self.get_sEcho(),
            'aaData': self.get_aaData(queryset[iDisplayStart : iDisplayStart + iDisplayLength]),
        }
    
#    def get_context_data(self, **kwargs):
#        context = super(ListView, self).get_context_data(**kwargs)
#        if self.request.is_ajax():
#            pass
#            iDisplayStart = int(self.request.GET.get('iDisplayStart', 0))
#            iDisplayLength = int(self.request.GET.get('iDisplayLength', 10))
#            iDisplayEnd = iDisplayStart + iDisplayLength if iDisplayLength != -1 else None
#            
#            context = {
#                'iTotalRecords': self.object_list.count(),
#                'iTotalDisplayRecords': self.object_list.exclude().count(),
#                'sEcho': int(self.request.GET['sEcho']),
#                'aaData': json.loads(JSONQuerysetResponseMixin.convert_to_json(self, self.object_list[iDisplayStart:iDisplayEnd])),
#            }
#        return context

    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            pass
#            items = self.get_filtered_queryset()
#            return HttpResponse(json.dumps(self.get_packaged_data(items)), mimetype='application/json')
        return super(ListView, self).render_to_response({}, **kwargs)
        
class DetailView(UserMixin, generic.detail.DetailView):
    pass
    
class CreateView(UserMixin, generic.edit.CreateView):
    pass

class UpdateView(UserMixin, generic.edit.UpdateView):
    pass

class DeleteView(UserMixin, generic.edit.DeleteView):
    pass

class DownloadView(UserMixin, generic.list.ListView):
    def render_to_response(self, context, **kwargs):
        emails = [user['email'] for user in self.object_list.order_by('pk').values('email')]
        response = HttpResponse(',\n'.join(emails), mimetype='text/plain')
        response['Content-Disposition'] = 'attachment;'
        return response
