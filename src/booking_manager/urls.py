
from django.urls import path
from .views import services, home, specialists, bookings, new_booking, detail_view

urlpatterns = [
    path('services/', services, name = 'services'),
    path('home/', home, name = 'homepage'),
    path('specialists/', specialists, name = 'specialists'),
    path('bookings/', bookings, name = 'bookings'),
    path('newbooking/', new_booking, name = 'new_booking'),
    path('bookings/<int:booking_id>/', detail_view, name='booking_detail')

]

