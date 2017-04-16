import datetime
from datetime import timedelta

from django import forms

from .models import Allocation
from people.models import Person
from seasons.models import Season


class AllocationForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'gg/mm/aaaa',
            'class': 'datepicker',
        }),
        label='data inizio',
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'placeholder': 'gg/mm/aaaa',
            'class': 'datepicker',
        }),
        label='data fine',
        help_text="Gli estremi sono inclusi.",
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
        today = datetime.date.today()
        errors_dict = {}
        if form_end_date is not None and form_start_date is not None:
            if form_end_date < form_start_date:
                self.add_error('end_date', forms.ValidationError('La data fine deve essere maggiore o uguale alla data inizio.'))
            current_season = Season.objects.get_open_season()
            if form_start_date < current_season.start_date or \
               form_start_date > current_season.end_date:
                self.add_error('start_date', forms.ValidationError('La data inizio deve essere inclusa nella stagione aperta.'))
            if form_end_date < current_season.start_date or \
               form_end_date > current_season.end_date:
               self.add_error('end_date', forms.ValidationError('La data fine deve essere inclusa nella stagione aperta.'))
            if form_start_date.month < today.month and \
               form_start_date.year == today.year:
               self.add_error('start_date', forms.ValidationError('La data inizio deve essere inclusa nel mese corrente.'))
            if form_end_date.month < today.month and \
               form_end_date.year == today.year:
               self.add_error('end_date', forms.ValidationError('La data fine deve essere inclusa nel mese corrente.'))
        super(AllocationForm, self).clean()


class AllocationPlainForm(AllocationForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'gg/mm/aaaa'}),
        label='data inizio',
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'placeholder': 'gg/mm/aaaa'}),
        label='data fine',
        help_text="Gli estremi sono inclusi.",
    )
