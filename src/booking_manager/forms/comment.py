from django import forms
from booking_manager.models import Comment



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["barber", "rating", "text"]


        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
        }
        labels = {
            'barber': "Barber's Name",
            'rating': "Rating",
            'text': "Comment Text",
        }
