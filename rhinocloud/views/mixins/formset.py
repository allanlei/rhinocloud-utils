from django.forms.models import modelformset_factory
from django.core.exceptions import ImproperlyConfigured


class ModelFormSetFactoryMixin(object):
    formset_fields = None
    formset_exclude = None
    formset_extra = 1
    
    def get_formset_model(self):
        if self.formset_model:
            model = self.formset_model
        else:
            raise ImproperlyConfigured('Provide formset_model or override get_formset_model().')
        return model
        
    def get_formset_fields(self):
        return self.formset_fields
    
    def get_formset_exclude(self):
        return self.formset_exclude
    
    def get_formset_class_kwargs(self):
        return {
            'fields': self.get_formset_fields(),
            'exclude': self.get_formset_exclude(),
            'extra': int(self.formset_extra),
        }
        
    def get_formset_class(self):
        return modelformset_factory(self.get_formset_model(),**self.get_formset_class_kwargs())

    def get_formset_queryset(self):
        return self.get_formset_model().objects.all()
    
    def get_formset_kwargs(self, **kwargs):
        if 'queryset' not in kwargs:
            kwargs['queryset'] = self.get_formset_queryset()
        return kwargs
        
    def get_formset(self, *args, **kwargs):
        if not hasattr(self, 'formset') or self.formset is None:
            self.formset = self.get_formset_class()(*args, **self.get_formset_kwargs(**kwargs))
        return self.formset

    def form_valid(self, form, **kwargs):
        formset = self.get_formset(self.request.POST, self.request.FILES)
        if formset.is_valid():
            response = super(ModelFormSetFactoryMixin, self).form_valid(form, **kwargs)
            self.formset_valid(formset, **kwargs)
            return response
        return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        self.get_formset(self.request.POST, self.request.FILES).is_valid()
        return super(ModelFormSetFactoryMixin, self).form_invalid(form, **kwargs)

    def formset_valid(self, formset, **kwargs):
        formset.save()
