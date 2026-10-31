# from booking_manager.models import Booking, BookingService, ProductBooking, Product
# from django import forms
# from django.utils import timezone
# from django.core.exceptions import ValidationError
#
#
# class CommentForm(forms.Form):
#     barber = forms.CharField(label="Barber's Name", max_length=20)
#     rating = forms.IntegerField(
#         label="Rating",
#         widget=forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
#     )
#     text = forms.CharField(
#         label="Comment Text",
#         max_length=100,
#         widget=forms.Textarea(
#             attrs={
#                 'cols':50,
#                 'rows':5,
#                 'class': 'form-control'
#             }
#         )
#     )
#
#
# class BookingForm(forms.ModelForm):
#     visit_time = forms.DateTimeField(
#         label="Booking Time",
#         input_formats=["%Y-%m-%dT%H:%M"],
#         widget=forms.DateTimeInput(
#             attrs={"type": "datetime-local", "class": "form-control"},
#             format="%Y-%m-%dT%H:%M",
#         ),
#     )
#
#
#     class Meta:
#         model = Booking
#         fields = ["name", "visit_time", "booking_service", "barber"]
#
#         labels = {
#             "name": "Booking Title",
#             "booking_service": "Service",
#             "barber": "Barber",
#         }
#
#
#
#     def clean(self):
#         cleaned_data = super().clean()
#         visit_time=cleaned_data.get('visit_time')
#         barber= cleaned_data.get('barber')
#
#         if visit_time and visit_time < timezone.now():
#             raise ValidationError(
#                 {"visit_time": "Booking time cannot be in the past!"}
#             )
#         if visit_time and barber:
#             chacked_time = Booking.objects.filter(visit_time=visit_time, barber=barber, is_active=True).exists()
#             if chacked_time:
#                 raise ValidationError(
#                     {"visit_time": "This barber is already busy at the specified time. Please choose another one!"}
#                 )
#         return cleaned_data
#
#
#
# class BookingServiceForm(forms.ModelForm):
#     class Meta:
#         model = BookingService
#         fields = ["name", "category", "description", "price", "duration_minute", "is_active"]
#         widgets = {
#             "description": forms.Textarea(
#                 attrs={"rows": 3, "class": "form-control"}
#             ),
#         }
#
#         labels = {
#             "name": "Booking Service Title",
#             "category": "Category",
#             "description": "Description",
#             "price": "Price",
#             "duration_minute": "Duration",
#             "is_active": "is_active"
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         price = cleaned_data.get('price')
#         duration_minute = cleaned_data.get('duration_minute')
#
#         if price is not None and price <= 0:
#             raise ValidationError(
#                 {"price": "The price cannot be negative or equal to 0"}
#             )
#         if duration_minute is not None and duration_minute <= 0:
#             raise ValidationError(
#                 {"duration_minute": "The duration of the service cannot be negative or equal to 0"}
#             )
#         return cleaned_data
#
#
#
# class ProductBookingForm(forms.ModelForm):
#     class Meta:
#         model = ProductBooking
#         fields = ["product", "quantity"]
#
#         labels = {
#             "product": "Product",
#             "quantity": "Quantity",
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         product = cleaned_data.get('product')
#         quantity = cleaned_data.get('quantity')
#
#         if quantity is not None and quantity <= 0:
#             raise ValidationError(
#                 {"quantity": "The quantity cannot be negative or equal to 0"}
#             )
#         if quantity and product:
#             actual_amount = getattr(product, 'amount', 0)
#             if quantity > actual_amount:
#                 raise ValidationError(
#                     {"quantity": f"Not enough stock! Only {actual_amount} items available in store"}
#                 )
#         return cleaned_data




















# class BookingForm(forms.ModelForm):
#     visit_time = forms.DateTimeField(
#         label="время записи",
#         input_formats=["%Y-%m-%dT%H:%M"],
#         widget=forms.DateTimeInput(
#             attrs={"type": "datetime-local", "class": "form-control"},
#             format="%Y-%m-%dT%H:%M",
#         ),
#     )
#
#     class Meta:
#         model = Booking
#         fields = ["name", "is_active", "visit_time", "description"]
#         widgets = {
#             "description": forms.Textarea(
#                 attrs={"rows": 3, "class": "form-control"}
#             ),
#         }



        # формы не привязанные к модели

# from django import forms
#
# from django.core.exceptions import ValidationError
#
#
# def validate_name(value):
#     if len(value) < 5:
#         raise ValidationError(f'{value} must be more than 5')
#
#
# class NameValidator:
#     message=' must be more than 5'
#
#     def __call__(self, value):
#         if len(value) < 5:
#             raise ValidationError(value + self.message)
#
#
#
#


#
