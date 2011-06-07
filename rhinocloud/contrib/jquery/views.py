from django.views import generic
from django.db.models import Q
from django.core.exceptions import ImproperlyConfigured


class DataTablesServerDataMixin(object):
    query_class = Q
    initial_query_kwargs = {}
    searchable_fields = ()
    
    def get_searchable_fields(self):
        if self.searchable_fields is not None:
            fields = self.searchable_fields
        else:
            raise ImproperlyConfigured('Provide searchable_fields or override get_searchable_fields().')
        return fields

    def get_query_class(self):
        if self.query_class:
            qc = self.query_class
        else:
            raise ImproperlyConfigured('Provide query_class or override get_query_class().')
        return qc
        
    def get_initial_query_kwargs(self):
        if self.initial_query_kwargs is not None:
            kwargs = self.initial_query_kwargs
        else:
            raise ImproperlyConfigured('Provide initial_query_kwargs or override get_initial_query_kwargs().')
        return kwargs
        
    def get_initial_query(self):
        return self.get_query_class()(**self.get_initial_query_kwargs())
        
    def get_searchterm_query(self, field, value):
        return self.get_query_class()(**{'%s__contains' % field: value})
    
    def get_queryset(self, **kwargs):
        queryset = super(DataTablesServerDataMixin, self).get_queryset(**kwargs)
        iSortingCols = int(self.request.GET.get('iSortingCols', -1))
        sSearch = self.request.GET.get('sSearch', None)
        
        if sSearch is not None:
            query = self.get_initial_query()
            for field in self.get_searchable_fields():
                query.add(self.get_searchterm_query(field, sSearch), Q.OR)
            queryset = queryset.filter(query)
        
        ordering = []
        for i in range(iSortingCols):
            sSortDir = self.request.GET['sSortDir_%s' % i]
            iSortingCols = int(self.request.GET['iSortCol_%s' % i])
            ordering.append('%s%s' % (sSortDir == 'asc' and '-' or '', self.get_searchable_fields()[iSortingCols]))
        queryset = queryset.order_by(*ordering)
        return queryset
