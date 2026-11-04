from django import forms
from booking_manager.models import Product, Barbershop

class StockForm(forms.Form):
    product_id = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Select product to move",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    barbershop_from = forms.ModelChoiceField(
        queryset=Barbershop.objects.all(),
        label="Source barbershop (from)",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    barbershop_to = forms.ModelChoiceField(
        queryset=Barbershop.objects.all(),
        label="Destination barbershop (to)",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    quantity = forms.IntegerField(
        label="Quantity to transfer",
        required=True,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter number of items'})
    )
