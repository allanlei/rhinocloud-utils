from django.db.models import Q
from django.http import HttpResponse
from django.core.exceptions import ImproperlyConfigured
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode


class ServerSideProcessingMixin(object):
    datatable_columns = None
    
    def get_columns(self):
        if self.datatable_columns is not None:
            columns = self.datatable_columns
        else:
            raise ImproperlyConfigured('Provide columns')
        return columns
        
    def get_iDisplayStart(self):
        return int(self.request.GET.get('iDisplayStart', 0))
    
    def get_iDisplayLength(self):
        return int(self.request.GET.get('iDisplayLength', 0))
    
    def get_iColumns(self):
        return int(self.request.GET.get('iColumns', len(self.get_columns())))
    
    def get_sEcho(self):
        return int(self.request.GET.get('sEcho', 1))
    
    def get_sSearch(self, index=None):
        if index is not None:
            return self.request.GET.get('sSearch_%s' % index, None)
        return self.request.GET.get('sSearch', None)
    
    def get_bRegex(self, index=None):
        if index is not None:
            bRegex = self.request.GET.get('bRegex_%s' % index, None)
        bRegex = self.request.GET.get('bRegex', None)
        return bRegex.lower() in ['true', 't']

    def get_bSearchable(self, index):
        return self.request.GET.get('bSearchable_%s' % index, 'F').lower() in ['true', 't']
        
    def get_bSortable(self, index):
        return self.request.GET.get('bSortable_%s' % index, 'F').lower() in ['true', 't']
    
    def get_sSorting(self, index):
        sorting = self.request.GET.get('sSortDir_%s' % index, None)
        column = self.get_columns()[index]
        if sorting is None or sorting.lower() not in ['desc', 'asc'] or column is None:
            return None
        return '%s%s' % (sorting.lower() == 'desc' and '-' or '', column)
        
    def get_filtered_queryset(self):
        queryset = self.get_queryset()
        q = Q()
        for query in self.get_filters():
            q.add(query, Q.OR)
        return queryset.filter(q).order_by(*self.get_sorting())
    
    def get_sorting(self):
        sorting = []
        for i in range(int(self.request.GET.get('iSortingCols', len(self.get_columns())))):
            sorting.append(self.get_sSorting(i))
        return filter(None, sorting)
        
    def get_filters(self):
        columns = self.get_columns()
        filters = []
        
#        for i in range(self.get_iDisplayLength()):
#            if self.get_bSearchable(i):
#                filters.append(self.get_column_filter(columns[i], self.get_sSearch(), self.get_bRegex()))
#                filters.append(self.get_column_filter(columns[i], self.get_sSearch(i), self.get_bRegex(i)))
        return filter(None, filters)
        
    def get_column_filter(self, column, sSearch, bRegex=False):
        if not sSearch or not column:
            return None
        if bRegex:
            kwargs = {
                '%s__iregex' % column: sSearch,
            }
        else:
            kwargs = {
                '%s__icontains' % column: sSearch,
            }
        return Q(**kwargs)
        
    def get_item_data(self, item):
        data = []
        columns = self.get_columns()
        for i in range(self.get_iColumns()):
            if columns[i]:
                column = columns[i].rsplit('__', 1)[0].split('__')[-1]
                data.append(smart_unicode(getattr(item, column)) if hasattr(item, column) else None)
            else:
                data.append(None)
        return data
        
    def get_packaged_data(self, queryset):
        iDisplayStart = self.get_iDisplayStart()
        iDisplayLength = self.get_iDisplayLength()
        return {
            'iTotalRecords': self.get_queryset().count(),
            'iTotalDisplayRecords': queryset.count(),
            'sEcho': self.get_sEcho(),
            'aaData': self.get_aaData(queryset[iDisplayStart : iDisplayStart + iDisplayLength]),
        }
        
    def get_aaData(self, items):
        return [self.get_item_data(item) for item in items]

    def render_to_response(self, context, **kwargs):
        if self.request.is_ajax():
            items = self.get_filtered_queryset()
            return HttpResponse(json.dumps(self.get_packaged_data(items)), mimetype='application/json')
        return super(ServerSideProcessingMixin, self).render_to_response(context, **kwargs)
