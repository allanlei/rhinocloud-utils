from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson as json

from rhinocloud.views.mixins.json import JSONQuerysetResponseMixin


class ServerSideProcessingMixin(JSONQuerysetResponseMixin):
    def get_sEcho(self):
        return int(self.request.GET.get('sEcho', 1))

    def get_iDisplayStart(self):
        return int(self.request.GET.get('iDisplayStart', 0))
    
    def get_iDisplayLength(self):
        return int(self.request.GET.get('iDisplayLength', 0))

    def get_iColumns(self):
        return int(self.request.GET.get('iColumns', 0))

    def get_iSorting(self):
        return int(self.request.GET.get('iSortingCols', 0))

    def get_sColumns(self):
        if not hasattr(self, 'sColumns'):
            self.sColumns = filter(lambda x: x is not None and len(x) > 0, self.request.GET.get('sColumns', '').split(','))
        return self.sColumns

    def get_abSearchable(self):
        if not hasattr(self, 'abSearchable'):
            self.abSearchable = [self.request.GET.get('bSearchable_%s' % i, 'false') == 'true' for i in range(len(self.get_sColumns()))]
        return self.abSearchable

    def get_abRegex(self):
        if not hasattr(self, 'abRegex'):
            bRegex = self.request.GET.get('bRegex', 'false')
            self.abRegex = [self.request.GET.get('bRegex_%s' % i, bRegex) == 'true' for i in range(len(self.get_sColumns()))]
        return self.abRegex
    
    def get_sSearch(self):
        return self.request.GET.get('sSearch', '')
        
    def get_asSearch(self):
        if not hasattr(self, 'asSearch'):
            sSearch = self.get_sSearch()
            asSearch = []
            for i in range(len(self.get_sColumns())):
                search = self.request.GET.get('sSearch_%s' % i, '')
                asSearch.append(search if search else sSearch)
            self.asSearch = asSearch
        return self.asSearch

    def get_asSorting(self):
        if not hasattr(self, 'asSorting'):
            sorting = []
            columns = self.get_sColumns()
            for i in range(self.get_iSorting()):
                index = int(self.request.GET['iSortCol_%s' % i])
                sorting.append('%s%s' % (self.request.GET['sSortDir_%s' % i] == 'desc' and '-' or '', columns[index]))
            self.asSorting = sorting
        return self.asSorting
        
    def get_datatable_queryset(self):
        queryset = self.get_queryset()
        columns = self.get_sColumns()
        searchable = self.get_abSearchable()
        search = self.get_asSearch()
        regex = self.get_abRegex()
        
        query = Q()
        for i in range(len(columns)):
            if searchable[i] and search[i]:
                query.add(Q(**{'%s__%s' % (columns[i], regex[i] and 'iregex' or 'icontains'): search[i]}), Q.OR)
        return queryset.filter(query)
        
    def render_to_response(self, context, **kwargs):
        iDisplayStart = self.get_iDisplayStart()
        
        queryset = self.get_queryset()
        filtered_queryset = self.get_datatable_queryset().order_by(*self.get_asSorting())
        aaData = self.convert_to_json(filtered_queryset[iDisplayStart: iDisplayStart+self.get_iDisplayLength()])
        
        data = {
            'iTotalRecords': queryset.count(),
            'iTotalDisplayRecords': filtered_queryset.count(),
            'sEcho': self.get_sEcho(),
            'aaData': json.loads(aaData),
        }
        return HttpResponse(json.dumps(data), mimetype='application/json')
