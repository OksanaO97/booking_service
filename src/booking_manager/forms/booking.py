from ..models import Booking, ProductBooking, Product, ProductBooking
from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError


class BookingForm(forms.ModelForm):
    visit_time = forms.DateTimeField(
        label="Booking Time",
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"},
            format="%Y-%m-%dT%H:%M",
        ),
    )


    class Meta:
        model = Booking
        fields = ["name", "visit_time", "booking_service", "barber"]

        labels = {
            "name": "Booking Title",
            "booking_service": "Service",
            "barber": "Barber",
        }



    def clean(self):
        cleaned_data = super().clean()
        visit_time=cleaned_data.get('visit_time')
        barber= cleaned_data.get('barber')

        if visit_time and visit_time < timezone.now():
            raise ValidationError(
                {"visit_time": "Booking time cannot be in the past!"}
            )
        if visit_time and barber:
            chacked_time = Booking.objects.filter(visit_time=visit_time, barber=barber, is_active=True).exists()
            if chacked_time:
                raise ValidationError(
                    {"visit_time": "This barber is already busy at the specified time. Please choose another one!"}
                )

        return cleaned_data



class ProductBookingForm(forms.ModelForm):
    class Meta:
        model = ProductBooking
        fields = ["product", "quantity"]

        labels = {
            "product": "Product",
            "quantity": "Quantity",
        }

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if quantity is not None and quantity <= 0:
            raise ValidationError(
                {"quantity": "The quantity cannot be negative or equal to 0"}
            )

        if quantity and product:
            actual_amount = getattr(product, 'amount', 0)
            if quantity > actual_amount:
                raise ValidationError(
                    {"quantity": f"Not enough stock! Only {actual_amount} items available in store"}
                )


        return cleaned_data

