from django.views import generic
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.contrib.auth.models import User, Group
from django.core import serializers

from rhinocloud.contrib.datatables.views.mixins import ServerSideProcessingMixin


class UserMixin(object):
    model = User
    
class ListView(UserMixin, ServerSideProcessingMixin, generic.list.ListView):
    template_name = 'administration/user_list.html'

    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            return ServerSideProcessingMixin.render_to_response(self, context, **kwargs)
        return generic.list.ListView.render_to_response(self, context, **kwargs)
        
class DetailView(UserMixin, generic.detail.DetailView):
    pass
    
class CreateView(UserMixin, generic.edit.CreateView):
    pass

class UpdateView(UserMixin, generic.edit.UpdateView):
    pass

class DeleteView(UserMixin, generic.edit.DeleteView):
    pass
