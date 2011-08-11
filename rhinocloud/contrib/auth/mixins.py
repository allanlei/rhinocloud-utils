from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ImproperlyConfigured


class PermissionRequiredMixin(object):
    permissions_map = None
    
    def get_permissions_map(self):
        if self.permissions_map is None:
            self.permissions_map = {}
        return self.permissions_map
        
    def get_permission(self):
        permissions_map = self.get_permissions_map()
        for view, perm in permissions_map.items():
            if isinstance(self, view):
                return '%s.%s_%s' % (self.model._meta.app_label, perm, self.model._meta.module_name)
        return None

    def get_decorator_func(self):
        return permission_required
        
    def get_decorator_args(self):
        return [self.get_permission()]
    
    def get_decorator_kwargs(self):
        return {}
        
    def dispatch(self, request, *args, **kwargs):
        permission = self.get_permission()
        if permission:
            decorator_func = self.get_decorator_func()
            @decorator_func(*self.get_decorator_args(), **self.get_decorator_kwargs())
            def wrapper(request, *args, **kwargs):
                return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
            return wrapper(request, *args, **kwargs)
        return super(PermissionRequiredMixin, self).dispatch(request, *args, **kwargs)
