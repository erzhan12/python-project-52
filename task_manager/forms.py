from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        bs_cls = 'form-control bg-secondary bg-opacity-50 border-secondary'
        for field in self.fields.values():
            field.widget.attrs['class'] = bs_cls
            field.widget.attrs['placeholder'] = field.label