from django import forms


class SearchDayAllocationForm(forms.Form):
    date = forms.DateField(
        widget=forms.SelectDateWidget(),
        required=False,
    )