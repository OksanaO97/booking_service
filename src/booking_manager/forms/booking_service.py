from django import forms
from django.core.exceptions import ValidationError
from ..models import BookingService

class BookingServiceForm(forms.ModelForm):
    class Meta:
        model = BookingService
        fields = ["name", "category", "description", "price", "duration_minute", "is_active"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 3, "class": "form-control"}
            ),
        }

        labels = {
            "name": "Booking Service Title",
            "category": "Category",
            "description": "Description",
            "price": "Price",
            "duration_minute": "Duration",
            "is_active": "is_active"
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        duration_minute = cleaned_data.get('duration_minute')

        if price is not None and price <= 0:
            raise ValidationError(
                {"price": "The price cannot be negative or equal to 0"}
            )
        if duration_minute is not None and duration_minute <= 0:
            raise ValidationError(
                {"duration_minute": "The duration of the service cannot be negative or equal to 0"}
            )
        return cleaned_data