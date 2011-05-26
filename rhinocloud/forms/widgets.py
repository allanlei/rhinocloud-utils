from django import forms

class HiddenInput(forms.HiddenInput):
    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly', False)
        if readonly:
            attrs = kwargs.get('attrs', {})
            attrs.update({
                'readonly': 'readonly',
            })
            kwargs['attrs'] = attrs
        super(HiddenInput, self).__init__(*args, **kwargs)
