import datetime

from django import forms

from .models import Allocation
from people.models import Person
from seasons.models import Season

class AllocationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label='data inizio',
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'datepicker'}),
        label='data fine',
        help_text="La data fine e` il primo giorno in cui la logistica imputata non sara` piu` valida.",
    )

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
        errors_dict = {}
        if form_end_date is not None and form_start_date is not None:
            if form_end_date <= form_start_date:
                self.add_error('end_date', forms.ValidationError('La data fine deve essere maggiore della data inizio.'))
            current_season = Season.objects.get_open_season()
            if form_start_date < current_season.start_date or \
               form_start_date > (current_season.end_date + datetime.timedelta(days=1)):
                self.add_error('start_date', forms.ValidationError('La data inizio deve essere compresa nella stagione aperta.'))
            if form_end_date < current_season.start_date or \
               form_end_date > (current_season.end_date + datetime.timedelta(days=1)):
               self.add_error('end_date', forms.ValidationError('La data fine deve essere compresa nella stagione aperta.'))
        super(AllocationForm, self).clean()