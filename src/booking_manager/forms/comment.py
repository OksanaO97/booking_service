from django import forms
from account.models import Barber



class CommentForm(forms.Form):
    barber = forms.ModelChoiceField(queryset=Barber.objects.all(),label="Barber's Name")
    rating = forms.IntegerField(
        label="Rating",
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
    )
    text = forms.CharField(
        label="Comment Text",
        max_length=100,
        widget=forms.Textarea(
            attrs={
                'cols':50,
                'rows':5,
                'class': 'form-control'
            }
        )
    )
