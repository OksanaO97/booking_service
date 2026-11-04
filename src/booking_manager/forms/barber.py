from django import forms
from account.models import Barber

class BarberForm(forms.Form):
    barber = forms.ModelChoiceField(
        queryset=Barber.objects.all(),
        label="Select New Barber",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )