from django import forms

from .models import Allocation
from people.models import Person

class AllocationForm(forms.ModelForm):

    class Meta:
        model = Allocation
        fields = ('location', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(AllocationForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        form_person = Person.objects.get(user=self.user)
        self.instance.person = form_person
        return super(AllocationForm, self).save(commit)

    def clean(self):
        form_start_date = self.cleaned_data.get('start_date')
        form_end_date = self.cleaned_data.get('end_date')
        if form_end_date is not None and form_start_date is not None:
            if form_end_date <= form_start_date:
                errors_dict = {
                    'start_date': ['La data inizio deve essere minore della data fine.'],
                    'end_date': ['La data fine deve essere maggiore della data inizio.'],
                }
                raise forms.ValidationError(errors_dict)
        super(AllocationForm, self).clean()