from django import forms

from .models import Allocation


class AllocationForm(forms.ModelForm):

    class Meta:
        model = Allocation
        fields = ('location', 'person', 'start_date', 'end_date')

    def clean(self):
        form_start_date = self.cleaned_data.get('start_date')
        form_end_date = self.cleaned_data.get('end_date')
        condition = \
            form_end_date <= form_start_date and \
            form_end_date is not None and \
            form_start_date is not None
        if condition:
            errors_dict = {
                'start_date': ['La data inizio deve essere minore della data fine.'],
                'end_date': ['La data fine deve essere maggiore della data inizio.'],
            }
            raise forms.ValidationError(errors_dict)
        super(AllocationForm, self).clean()